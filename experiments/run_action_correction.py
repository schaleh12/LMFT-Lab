"""Standalone bounded action adapter; production correction receiver is unchanged."""
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

from lmft_lab import attention, consistent_attention as circuit, correction as repair
from lmft_lab import correction_fixture as fixture, contextual, preservation_context as preservation
from lmft_lab.runtime import initial_state, software_manifest, advance
from lmft_lab.runtime_store import atomic_json, digest

PROTOCOL = Path('experiments/ACTION_CORRECTION_PROTOCOL_V2.md')
MODES = ('full', 'memory', 'ablated', 'gather-only', 'original')
DEFS = {
    'r1': ('c1', None, 'c1-a', None, True),
    'r2': ('c4', 'c4-a', None, 'shielded', True),
    'r3': ('c5', None, 'c5-a', None, True),
    'r4': ('c6', None, 'c6-a', None, True),
    'r5': ('c7', None, 'c7-a', None, True),
    'r6': ('c10', 'c10-a', 'c10-b', None, True),
    'r7': ('c12', None, 'c12-a', None, True),
    'r8': ('c9', None, 'c9-a', None, True),
    'r9': ('c1', None, 'c1-a', 'payload_valid', True),
    'r10': ('c3', None, 'c3-a', None, True),
    'r11': ('c4', 'c4-a', None, 'shielded', False),
    'r12': ('c4', None, None, 'shielded', True),
}
EXPECTED = {
    'full': ['correction', 'gather', None, 'correction', None, None, None, 'correction', 'correction', None, None, 'gather'],
    'memory': ['correction', 'gather', None, 'correction', None, None, None, 'correction', 'correction', None, None, 'gather'],
    'ablated': ['correction', 'gather', None, 'correction', None, None, None, 'correction', 'gather', None, None, 'gather'],
    'gather-only': [None, 'gather', None, None, None, None, None, None, 'gather', None, None, 'gather'],
    'original': ['gather', 'gather', 'gather', 'gather', 'gather', None, None, 'gather', 'gather', None, 'gather', 'gather'],
}
SOURCE = 'authored-action-correction-gather-1'


def message(identifier, op, record):
    return {'schema_version': 1, 'id': identifier, 'sender': fixture.AUTHORITY,
            'source': fixture.SOURCE, 'type': 'observation',
            'content': {'text': 'Authored bounded experiment.', 'operation': op, 'record': record}}


def step(state, item):
    return advance(state, (state['cursor'] + 1, item, None, json.dumps(item)), None)


def proposal(key, cid):
    return next(r for r in fixture.corrections(key) if r['correction_id'] == cid)


def prepare(identifier):
    key, preparation, cid, gather, available = DEFS[identifier]
    state = initial_state('action-' + identifier, True, software_manifest(None, 'fixture'), 'correction-lmft')
    for trial in list(contextual.TRIALS)[:8]:
        state = step(state, message('prior-' + trial, 'outcome', contextual.outcome(trial)))
    for i, record in enumerate(fixture.initial_records(key)):
        if identifier == 'r9' and record['question'] == 'payload_valid':
            continue
        state = step(state, message('initial-' + str(i), 'evidence', record))
    if preparation:
        state = step(state, message('preparation', 'correction', proposal(key, preparation)))
    case = fixture.public_case(key)
    current = state['judgment']
    prediction = repair.predict(current, case)
    current['cases'][key] = {'input': case, 'request': None, 'evaluations': []}
    current['cache'][key] = {'key': repair.cache_key(current, case), 'result': prediction, 'selected': None}
    offers = []
    if cid:
        record = proposal(key, cid)
        # Offer describes operation capability, NEVER replacement truth/value.
        coordinate = {k: record['replacement'].get(k) for k in ('case_id', 'scope', 'question', 'part')}
        offers.append({'id': 'correct-' + cid, 'kind': 'correction', 'field': coordinate['question'],
                       'correction_id': cid, 'target_id': record['target_id'],
                       'expected_digest': record['expected_digest'], 'coordinate': coordinate,
                       'authority': record['authority'], 'payload_sha256': digest(record),
                       'available': True})
    if gather:
        support = prediction['support'][gather]
        parts = [p for p, values in support['part_values'].items() if not values]
        offers.append({'id': 'gather-' + gather, 'kind': 'gather', 'field': gather,
                       'case_id': key, 'scope': case['scope'], 'parts': parts, 'available': available})
    return {'state': state, 'case': case, 'offers': offers}


def preflight(current, case, offer):
    if not offer['available']:
        return 'service unavailable'
    if offer['field'] not in case['decision_questions']:
        return 'irrelevant question'
    status = circuit.support(repair.effective(current), case, offer['field'])
    if status['resolved']:
        return 'already resolved'
    if offer['kind'] == 'gather':
        missing = [p for p, values in status['part_values'].items() if not values]
        if offer['case_id'] != case['case_id'] or offer['scope'] != case['scope']:
            return 'wrong gather scope'
        if not offer['parts'] or offer['parts'] != missing:
            return 'gather must request exactly missing parts'
        return None
    if not status['inconsistent']:
        return 'no inconsistent support to correct'
    permit = current['policy']['permits'].get(offer['correction_id'])
    if not permit or permit['authority'] != offer['authority'] or permit['payload_sha256'] != offer['payload_sha256']:
        return 'no matching operation permit'
    if offer['correction_id'] in current['correction_index']:
        return 'correction ID already used'
    target = current['ledger'].get(offer['target_id'])
    root = current['roots'].get(offer['target_id'])
    if target is None or current['heads'].get(root) != offer['target_id']:
        return 'inactive or missing target'
    if digest(target['record']) != offer['expected_digest']:
        return 'stale target digest'
    if target['record']['case_id'] != case['case_id'] or target['record']['scope'] != case['scope'] or target['record']['question'] != offer['field']:
        return 'target outside requested question scope'
    if any(offer['coordinate'].get(k) != target['record'][k] for k in ('case_id', 'scope', 'question', 'part')):
        return 'wrong correction coordinate'
    return None


def select(current, case, offers, mode):
    view = repair.effective(current)
    view['mode'] = 'consistent-no-clarity' if mode == 'ablated' else 'consistent-full'
    if mode == 'original':
        selected, traces = circuit.select(view, case)  # Unchanged original algorithm, no action filter.
        if selected is None:
            return None, {'questions': traces, 'actions': []}
        availability = next((o['available'] for o in offers if o['kind'] == 'gather' and o['field'] == selected['field']), True)
        action = {'id': 'original-' + selected['id'], 'kind': 'gather', 'field': selected['field'],
                  'case_id': case['case_id'], 'scope': case['scope'],
                  'parts': list(circuit.PARTS[selected['field']]), 'available': availability}
        return action, {'questions': traces, 'actions': [{'offer': action, 'rejection': None, 'policy': 'original unfiltered question request'}]}
    if mode == 'memory':
        question_traces = []
        for candidate in case['candidates']:
            if candidate['field'] not in case['decision_questions']:
                continue
            status = circuit.support(view, case, candidate['field'])
            conflict, _ = attention.appraisal(case, candidate)
            if not conflict:
                continue
            score = max(0., min(1., .25 * (view['weights'][candidate['route']] + .3125
                         - status['coverage'] - int(status['resolved']) + int(status['inconsistent']))))
            question_traces.append({'candidate': candidate, 'support': status, 'score': score})
    else:
        _, question_traces = circuit.select(view, case)
    scores = {row['candidate']['field']: row['score'] for row in question_traces if 'score' in row}
    traces = []; eligible = []
    for offer in offers:
        reason = preflight(current, case, offer)
        if mode == 'gather-only' and offer['kind'] == 'correction':
            reason = 'gather-only control'
        score = scores.get(offer['field'], 0.)
        if reason is None and score <= 0:
            reason = 'no positive question priority'
        traces.append({'offer': deepcopy(offer), 'rejection': reason, 'score': score})
        if reason is None:
            eligible.append((score, offer['id'], offer))
    eligible.sort(key=lambda x: (-x[0], x[1]))
    return (deepcopy(eligible[0][2]) if eligible else None), {'questions': question_traces, 'actions': traces}


def request(bundle, mode):
    state = deepcopy(bundle['state'])
    if 'episode' in state:
        return state  # Pending and closed episodes retain their original spent budget.
    original = digest(state)
    selected, traces = select(state['judgment'], bundle['case'], bundle['offers'], mode)
    if digest(state) != original:
        raise AssertionError('selection mutated state')
    state['episode'] = {'selected': selected, 'trace': traces, 'charged': int(selected is not None),
                        'status': 'pending' if selected else 'closed', 'reply_digest': None}
    if selected:
        state['questions']['action-request'] = {'case_id': bundle['case']['case_id'],
            'question': selected['field'], 'status': 'open', 'closed_by': None}
    return state


def service_reply(selected):
    if selected['kind'] == 'correction':
        return proposal(selected['coordinate']['case_id'], selected['correction_id'])
    if not selected['available']:
        return {'unavailable': True}
    return {'records': [{'evidence_id': 'gather/' + selected['case_id'] + '/' + selected['field'] + '/' + part,
        'case_id': selected['case_id'], 'scope': selected['scope'], 'question': selected['field'],
        'part': part, 'value': True, 'source': SOURCE} for part in selected['parts']]}


def receive(state, case, reply, sender=fixture.AUTHORITY):
    changed = deepcopy(state); episode = changed['episode']; selected = episode['selected']
    if episode['status'] != 'pending':
        return changed, {'status': 'duplicate_reply' if episode['reply_digest'] == digest(reply) else 'closed_episode'}
    receipt = {}
    if selected['kind'] == 'correction':
        # Correlate the selected operation before delegating all substantive checks.
        if reply.get('correction_id') != selected['correction_id'] or reply.get('target_id') != selected['target_id']:
            receipt['status'] = 'uncorrelated_reply'
        else:
            item = message('action-reply', 'correction', reply); item['sender'] = sender
            repair.correct(changed, item, receipt)
    elif not selected['available']:
        receipt.update(status='gather_unavailable', verification_checked=False)
    elif sender != fixture.AUTHORITY or digest(reply) != digest(service_reply(selected)):
        receipt['status'] = 'unverified_gather_reply'
    else:
        current = changed['judgment']
        for record in reply['records']:
            eid = record['evidence_id']
            if eid in current['ledger']:
                raise ValueError('gather identity collision')
            current['ledger'][eid] = {'record': deepcopy(record), 'source': SOURCE,
                'verification': 'exact authored selected-coordinate reference', 'root': eid, 'parent': None}
            current['roots'][eid] = eid; current['heads'][eid] = eid
        current['cache'].pop(case['case_id'], None)
        question = changed['questions']['action-request']
        if circuit.support(repair.effective(current), case, selected['field'])['resolved']:
            question.update(status='resolved_by_gather', closed_by='action-reply')
        receipt.update(status='gather_accepted', verification_checked=True)
    episode.update(status='closed', reply_digest=digest(reply), receipt=receipt)
    return changed, receipt


def semantic(state):
    current = state['judgment']
    return {'effective': repair.effective_ref(current), 'cache': current['cache'], 'questions': state['questions']}


def finish(pending, case):
    selected = pending['episode']['selected']; before = repair.predict(pending['judgment'], case)
    originals = deepcopy(pending['judgment']['ledger']); old_events = len(pending['judgment']['corrections'])
    reply = service_reply(selected) if selected else None
    final, receipt = receive(pending, case, reply) if selected else (deepcopy(pending), {'status': 'no_action'})
    result = repair.predict(final['judgment'], case)
    replay, _ = receive(final, case, reply) if selected else (deepcopy(final), {})
    checks = {
        'originals_immutable': all(final['judgment']['ledger'][k] == v for k, v in originals.items()),
        'fixed_birth': final['birth'] == pending['birth'],
        'fixed_weights': final['judgment']['weights'] == pending['judgment']['weights'],
        'fixed_counters': final['judgment']['branches'] == pending['judgment']['branches'],
        'single_charge': final['episode']['charged'] <= 1,
        'duplicate_semantic_noop': digest(replay) == digest(final),
        'rejection_invariance': receipt['status'] not in ('correction_rejected', 'unverified_gather_reply', 'gather_unavailable', 'uncorrelated_reply') or semantic(final) == semantic(pending),
    }
    events = final['judgment']['corrections'][old_events:]
    checks['same_correction_roots'] = not events or len(final['judgment']['heads']) == len(pending['judgment']['heads'])
    checks['gather_admission_roots'] = not selected or selected['kind'] != 'gather' or (
        len(final['judgment']['heads']) - len(pending['judgment']['heads']) == len(final['judgment']['ledger']) - len(originals))
    return {'selected': selected, 'trace': pending['episode']['trace'], 'reply': reply, 'receipt': receipt,
            'before': before, 'after': result, 'final': final, 'action_events': events, 'checks': checks,
            'new_resolved': sum(result['support'][f]['resolved'] and not before['support'][f]['resolved'] for f in before['support']),
            'coverage_gain': sum(result['support'][f]['coverage'] - before['support'][f]['coverage'] for f in before['support']),
            'admitted_records': len(final['judgment']['ledger']) - len(originals),
            'initial_roots': len(pending['judgment']['heads']), 'final_roots': len(final['judgment']['heads']),
            'initial_stored_records': len(originals), 'final_stored_records': len(final['judgment']['ledger']),
            'duplicate_additional_admissions': len(replay['judgment']['ledger']) - len(final['judgment']['ledger']),
            'duplicate_additional_corrections': len(replay['judgment']['corrections']) - len(final['judgment']['corrections'])}


def worker(root):
    frozen = json.loads((root / 'pending-snapshots.json').read_text())
    rows = {mode: [finish(item['pending'], item['case']) for item in frozen['conditions'][mode]] for mode in MODES}
    atomic_json(root / 'restarted-results.json', {'pid': os.getpid(), 'input_digest': digest(frozen), 'conditions': rows})


def comparison_digest(rows):
    # Runtime emit timestamps are wall-clock provenance, not semantic restart state.
    normalized = deepcopy(rows)
    for values in normalized.values():
        for row in values:
            for out in row['final']['outbox']:
                out.pop('timestamp', None)
    return digest(normalized)


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path)
    parser.add_argument('--preservation-context', type=Path); parser.add_argument('--reload', type=Path)
    args = parser.parse_args()
    if args.reload:
        preservation.pinned_current(args.reload, Path.cwd()); worker(args.reload); return
    if not args.output or not args.preservation_context:
        parser.error('fresh output and complete current preservation context required')
    root = args.output; root.mkdir(parents=True, exist_ok=False)
    context = json.loads(args.preservation_context.read_text()); preservation.verify_current(context, Path.cwd())
    for name in context['files']:
        dest = root / 'archive' / name; dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(name, dest)
    shutil.copy2(args.preservation_context, root / 'current-preservation-context.json')
    atomic_json(root / 'archive-manifest.json', context['files'])
    atomic_json(root / 'provenance.json', {'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'working_tree': subprocess.check_output(['git', 'status', '--short'], text=True), 'protocol_sha256': preservation.file_hash(PROTOCOL),
        'preservation_kind': preservation.KIND, 'preservation_context_sha256': preservation.file_hash(args.preservation_context), 'model_calls': 0})
    try:
        bundles = {key: prepare(key) for key in DEFS}; atomic_json(root / 'frozen-inputs.json', {'order': list(DEFS), 'bundles': bundles})
        conditions = {mode: [{'case': bundles[key]['case'], 'pending': request(bundles[key], mode)} for key in DEFS] for mode in MODES}
        frozen = {'order': list(DEFS), 'conditions': conditions}; atomic_json(root / 'pending-snapshots.json', frozen)
        continuous = {mode: [finish(item['pending'], item['case']) for item in conditions[mode]] for mode in MODES}
        subprocess.run([sys.executable, str(Path(__file__).resolve()), '--reload', str(root)], check=True)
        restarted = json.loads((root / 'restarted-results.json').read_text())
        checks = {'actual_child': restarted['pid'] != os.getpid(), 'loaded_pending_snapshot': restarted['input_digest'] == digest(frozen),
                  'restart_semantic_parity': comparison_digest(continuous) == comparison_digest(restarted['conditions'])}
        atomic_json(root / 'frozen-predictions.json', {m: [r['after'] for r in rows] for m, rows in continuous.items()})
        metrics = {}
        for mode, rows in continuous.items():
            checks[mode + '_actions'] = [r['selected']['kind'] if r['selected'] else None for r in rows] == EXPECTED[mode]
            decided = [i for i, r in enumerate(rows) if r['after']['decision'] != 'abstain']
            correct = sum((rows[i]['after']['decision'] == 'success') == fixture.actual_success(DEFS[list(DEFS)[i]][0]) for i in decided)
            metric = {'requests': sum(r['selected'] is not None for r in rows), 'decided': len(decided), 'correct': correct,
                      'new_resolved': sum(r['new_resolved'] for r in rows), 'coverage_gain': sum(r['coverage_gain'] for r in rows),
                      'accepted_corrections': sum(e['accepted'] for r in rows for e in r['action_events']),
                      'rejected_corrections': sum(not e['accepted'] for r in rows for e in r['action_events']),
                      'decision_coverage': len(decided) / len(rows), 'decision_accuracy': correct / len(decided),
                      'preparation_corrections': sum(len(b['state']['judgment']['corrections']) for b in bundles.values())}
            metric.update(correction_requests=sum(bool(r['selected'] and r['selected']['kind'] == 'correction') for r in rows),
                gather_requests=sum(bool(r['selected'] and r['selected']['kind'] == 'gather') for r in rows),
                correction_receiver_checks=sum(e['verification']['checked'] for r in rows for e in r['action_events']),
                gather_receiver_checks=sum(r['receipt'].get('verification_checked', False) for r in rows),
                gather_service_attempts=sum(bool(r['selected'] and r['selected']['kind'] == 'gather') for r in rows),
                correction_service_attempts=sum(bool(r['selected'] and r['selected']['kind'] == 'correction') for r in rows),
                gather_returned_records=sum(len(r['reply'].get('records', [])) for r in rows if r['selected'] and r['selected']['kind'] == 'gather'),
                correction_returned_proposals=sum(bool(r['selected'] and r['selected']['kind'] == 'correction') for r in rows),
                admitted_gather_records=sum(r['admitted_records'] for r in rows if r['selected'] and r['selected']['kind'] == 'gather'),
                admitted_replacement_records=sum(r['admitted_records'] for r in rows if r['selected'] and r['selected']['kind'] == 'correction'),
                non_resolving_requests=sum(bool(r['selected'] and not (not r['before']['support'][r['selected']['field']]['resolved'] and r['after']['support'][r['selected']['field']]['resolved'])) for r in rows),
                contradiction_gathers_unresolved=sum(bool(r['selected'] and r['selected']['kind'] == 'gather' and r['before']['support'][r['selected']['field']]['inconsistent'] and not r['after']['support'][r['selected']['field']]['resolved']) for r in rows),
                already_resolved_requests=sum(bool(r['selected'] and r['before']['support'][r['selected']['field']]['resolved']) for r in rows),
                newly_enabled_decisions=sum(r['before']['decision'] == 'abstain' and r['after']['decision'] != 'abstain' for r in rows),
                initial_roots=sum(r['initial_roots'] for r in rows), final_roots=sum(r['final_roots'] for r in rows),
                initial_stored_records=sum(r['initial_stored_records'] for r in rows), final_stored_records=sum(r['final_stored_records'] for r in rows),
                preparation_receiver_checks=sum(e['verification']['checked'] for b in bundles.values() for e in b['state']['judgment']['corrections']),
                preparation_admitted_replacements=sum(e['accepted'] for b in bundles.values() for e in b['state']['judgment']['corrections']),
                duplicate_additional_admissions=sum(r['duplicate_additional_admissions'] for r in rows),
                duplicate_additional_corrections=sum(r['duplicate_additional_corrections'] for r in rows))
            metrics[mode] = metric
            expected = (9, 4, 3, 1, 0, 0) if mode == 'original' else (3, 4, 3, 2, 0, 0) if mode == 'gather-only' else (6, 6, 4, 4, 2 if mode == 'ablated' else 3, 1)
            checks[mode + '_metrics'] = tuple(metric[k] for k in ('requests', 'decided', 'correct', 'new_resolved', 'accepted_corrections', 'rejected_corrections')) == expected
            costs = {'full': (2, 0, 2, 2, 2, 4, 2, 3, 1., 3), 'memory': (2, 0, 2, 2, 2, 4, 2, 3, 1., 3),
                     'ablated': (2, 0, 3, 3, 3, 3, 3, 2, 2., 3), 'gather-only': (1, 0, 3, 3, 3, 0, 3, 0, 2., 1),
                     'original': (8, 6, 9, 16, 8, 0, 16, 0, 1., 1)}
            checks[mode + '_costs'] = tuple(metric[k] for k in ('non_resolving_requests', 'contradiction_gathers_unresolved',
                'gather_service_attempts', 'gather_returned_records', 'gather_receiver_checks', 'correction_receiver_checks',
                'admitted_gather_records', 'admitted_replacement_records', 'coverage_gain', 'newly_enabled_decisions')) == costs[mode]
            checks[mode + '_preparation_and_no_resolved_requests'] = metric['already_resolved_requests'] == 0 and all(metric[k] == 3 for k in ('preparation_corrections', 'preparation_receiver_checks', 'preparation_admitted_replacements'))
        checks['memory_action_prediction_parity'] = all(l['selected'] == r['selected'] and l['after'] == r['after']
             and l['action_events'] == r['action_events'] for l, r in zip(continuous['full'], continuous['memory']))
        preservation.pinned_current(root, Path.cwd())
        checks['archive_hashes'] = all(preservation.file_hash(root / 'archive' / name) == h for name, h in context['files'].items())
        values = list(checks.values()) + [v for rows in continuous.values() for r in rows for v in r['checks'].values()]
        result = {'checks': checks, 'integrity_passed': sum(values), 'integrity_total': len(values), 'metrics': metrics,
                  'conditions': continuous, 'model_calls': 0}
        atomic_json(root / 'results.json', result); print(json.dumps({k: result[k] for k in ('integrity_passed', 'integrity_total', 'metrics')}))
        if not all(values):
            raise AssertionError('frozen action-aware expectations failed; preserve evidence')
    except Exception as exc:
        atomic_json(root / 'failure.json', {'error': repr(exc)}); raise


if __name__ == '__main__':
    main()
