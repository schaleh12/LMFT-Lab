from lmft_lab.late_evidence import late_record, LateRegistry
"""Chained process-restart study using the existing correction ledger and adapter."""
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import run_action_correction as action
from lmft_lab import correction as repair, correction_fixture as fixture
from lmft_lab import preservation_context as preservation
from lmft_lab.runtime_store import atomic_json, digest

PROTOCOL = Path('experiments/SEQUENTIAL_CORRECTION_PROTOCOL.md')
CASES = ('r1', 'r8')
CONTROLS = ('late', 'no-later', 'frozen')
MODES = ('full', 'memory')






def canonical(value):
    result = deepcopy(value)
    def visit(item):
        if isinstance(item, dict):
            for key, val in item.items():
                if key == 'outbox':
                    for message in val:
                        message.pop('timestamp', None)
                else:
                    visit(val)
        elif isinstance(item, list):
            for val in item:
                visit(val)
    visit(result)
    return json.loads(json.dumps(result))  # Compare the persisted JSON representation (tuples become arrays).


def probe(state, case):
    before = digest(state)
    result = repair.predict(state['judgment'], case)
    current = state['judgment']
    report = {'prediction': result, 'effective': repair.effective_ref(current),
              'stored_records': len(current['ledger']), 'heads': deepcopy(current['heads']),
              'questions': deepcopy(state['questions']), 'charged': state['episode']['charged'],
              'corrections': len(current['corrections']), 'hypothesis_survivors': None,
              'validation_acceptance': None}
    if digest(state) != before:
        raise AssertionError('probe changed persistent state')
    return report


def intake(state, identifier, operation, record, registry=None, sender=None):
    changed = deepcopy(state)
    item = action.message(identifier, operation, record)
    if sender is not None:
        item['sender'] = sender
    receipt = {'message_id': identifier}
    repair.handle(changed, item, None, receipt, evidence_registry=registry)
    return changed, receipt


def inputs():
    bundles = {key: action.prepare(key) for key in CASES}
    return {f'{key}/{mode}/{control}': {
        'case': bundle['case'], 'offers': bundle['offers'], 'mode': mode,
        'control': control, 'state': action.request(bundle, mode), 'audit': []}
        for key, bundle in bundles.items() for mode in MODES for control in CONTROLS}


def transition(row, stage):
    row = deepcopy(row); state = row['state']; case = row['case']; audit = row['audit']
    old_ledger = deepcopy(state['judgment']['ledger'])
    if stage == 'corrected':
        reply = action.service_reply(state['episode']['selected'])
        state, receipt = action.receive(state, case, reply)
        audit.append({'operation': 'action-correction', 'receipt': receipt})
    elif stage == 'late':
        record = late_record(case)
        if row['control'] == 'late':
            registry = LateRegistry()
            state, receipt = intake(state, 'late-report', 'evidence', record, registry)
            audit.append({'operation': 'late-evidence', 'receipt': receipt,
                          'registration_checks': registry.calls, 'record': record})
        else:
            audit.append({'operation': 'late-evidence', 'status': 'withheld' if row['control'] == 'frozen' else 'not-sent',
                          'registration_checks': 0, 'record': record if row['control'] == 'frozen' else None})
    elif stage == 'final':
        baseline = probe(state, case)
        selected_reply = action.service_reply(state['episode']['selected'])
        replay, receipt = action.receive(state, case, selected_reply)
        if digest(replay) != digest(state):
            raise AssertionError('closed episode reply replay changed state')
        retried = action.request({'state': state, 'case': case, 'offers': row['offers']}, row['mode'])
        if digest(retried) != digest(state):
            raise AssertionError('episode reset')
        audit.append({'operation': 'episode-replay', 'receipt': receipt, 'new_charge': 0})
        challenges = []
        if row['control'] == 'late':
            record = late_record(case)
            challenges.append(('late-retransmission', 'evidence', record, 'duplicate_evidence'))
            conflicting = deepcopy(record); conflicting['value'] = True
            challenges.append(('conflicting-evidence-id', 'evidence', conflicting, 'rejected'))
        challenges.append(('correction-retransmission', 'correction', selected_reply, 'duplicate_correction'))
        unauthorized = deepcopy(selected_reply); unauthorized['correction_id'] = 'unpermitted-new-operation'
        challenges.append(('unauthorized-operation', 'correction', unauthorized, 'correction_rejected'))
        malformed = deepcopy(selected_reply); malformed.pop('correction_id')
        challenges.append(('malformed-operation', 'correction', malformed, 'correction_rejected'))
        conflicting = deepcopy(selected_reply); conflicting['reason'] = 'changed payload'
        challenges.append(('conflicting-operation-id', 'correction', conflicting, 'correction_rejected'))
        for name, operation, record, expected in challenges:
            before = probe(state, case); registry = LateRegistry()
            state, receipt = intake(state, name, operation, record, registry if operation == 'evidence' else None)
            after = probe(state, case)
            if receipt['status'] != expected:
                raise AssertionError((name, receipt))
            for field in ('prediction', 'effective', 'stored_records', 'heads', 'questions', 'charged'):
                if before[field] != after[field]:
                    raise AssertionError('challenge changed scientific state: ' + name)
            audit.append({'operation': name, 'receipt': receipt, 'registration_checks': registry.calls})
        if baseline['prediction'] != probe(state, case)['prediction']:
            raise AssertionError('replay/rejection altered prediction')
    else:
        raise ValueError(stage)
    if any(state['judgment']['ledger'][k] != v for k, v in old_ledger.items()):
        raise AssertionError('original ledger record changed')
    row['state'] = state; row['probe'] = probe(state, case)
    return row


def stale_companion():
    bundle = action.prepare('r6')  # Existing c10-a preparation; no new permit.
    state = bundle['state']; before = repair.effective_ref(state['judgment']); rows = []
    for cid, expected in [('c10-b', 'stale target: a newer accepted head exists'), ('c10-c', 'stale target digest')]:
        state, receipt = intake(state, cid, 'correction', action.proposal('c10', cid))
        event = state['judgment']['corrections'][-1]
        if event['reason'] != expected or event['verification']['checked'] or repair.effective_ref(state['judgment']) != before:
            raise AssertionError('stale companion failed')
        rows.append({'receipt': receipt, 'event': event})
    return {'state': state, 'checks': rows, 'preparation_verifier_calls': 1, 'challenge_verifier_calls': 0}


def worker(root, stage, input_path, expected_hash):
    preservation.pinned_current(root, Path.cwd())
    if preservation.file_hash(input_path) != expected_hash:
        raise ValueError('restart input hash mismatch')
    rows = json.loads(input_path.read_text())
    result = {key: transition(row, stage) for key, row in rows.items()}
    atomic_json(root / f'restarted-{stage}.json', result)
    atomic_json(root / f'process-{stage}.json', {'pid': os.getpid(), 'parent_pid': os.getppid(),
                'input_sha256': expected_hash, 'input_digest': digest(rows), 'stage': stage})
    preservation.pinned_current(root, Path.cwd())


def run(root, context_path):
    root.mkdir(parents=True, exist_ok=False)
    context = json.loads(context_path.read_text()); preservation.verify_current(context, Path.cwd())
    for name in context['files']:
        dest = root / 'archive' / name; dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(name, dest)
    shutil.copy2(context_path, root / 'current-preservation-context.json')
    atomic_json(root / 'archive-manifest.json', context['files'])
    atomic_json(root / 'provenance.json', {'source_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], text=True).strip(),
        'working_tree': subprocess.check_output(['git', 'status', '--short'], text=True),
        'protocol_sha256': preservation.file_hash(PROTOCOL), 'preservation_kind': preservation.KIND,
        'preservation_context_sha256': preservation.file_hash(context_path), 'parent_pid': os.getpid(), 'model_calls': 0})
    try:
        pending = inputs(); atomic_json(root / 'pending.json', pending)
        continuous = pending; prior = root / 'pending.json'; stages = {}; checks = {}; pids = []
        for stage in ('corrected', 'late', 'final'):
            continuous = {key: transition(row, stage) for key, row in continuous.items()}
            atomic_json(root / f'continuous-{stage}.json', continuous)
            child = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), '--reload', str(root),
                            '--stage', stage, '--input', str(prior), '--input-sha256', preservation.file_hash(prior)])
            if child.wait() != 0:
                raise RuntimeError('restart child failed: ' + stage)
            restarted = json.loads((root / f'restarted-{stage}.json').read_text())
            process = json.loads((root / f'process-{stage}.json').read_text()); pids.append(process['pid'])
            # Windows venv redirector may launch the actual interpreter as its child.
            checks[stage + '_actual_child'] = process['pid'] != os.getpid() and (process['pid'] == child.pid or process['parent_pid'] == child.pid)
            atomic_json(root / f'launch-{stage}.json', {'launcher_pid': child.pid, 'orchestrator_pid': os.getpid()})
            checks[stage + '_input_digest'] = process['input_digest'] == digest(json.loads(prior.read_text()))
            checks[stage + '_complete_semantic_parity'] = canonical(continuous) == canonical(restarted)
            stages[stage] = {key: row['probe'] for key, row in continuous.items()}
            prior = root / f'restarted-{stage}.json'
        checks['distinct_restart_processes'] = len(set(pids)) == 3
        atomic_json(root / 'frozen-predictions.json', stages)
        metrics = {}
        for mode in MODES:
            for control in CONTROLS:
                name = mode + '/' + control; metrics[name] = {}
                for stage, rows in stages.items():
                    selected = [rows[f'{key}/{name}'] for key in CASES]
                    decisions = [r['prediction']['decision'] for r in selected]
                    decided = [i for i, d in enumerate(decisions) if d != 'abstain']
                    correct = sum((decisions[i] == 'success') == fixture.actual_success(action.DEFS[CASES[i]][0]) for i in decided)
                    metrics[name][stage] = {'decisions': decisions, 'coverage': len(decided)/2,
                         'correct': correct, 'accuracy': correct/len(decided) if decided else None,
                         'roots': [r['effective']['independent_count'] for r in selected],
                         'stored_records': [r['stored_records'] for r in selected]}
                    expected = 'abstain' if stage != 'corrected' and control == 'late' else 'success'
                    checks[name + '/' + stage + '/expected_decision'] = decisions == [expected]*2
                finals = [continuous[f'{key}/{name}'] for key in CASES]
                events = [e for row in finals for e in row['state']['judgment']['corrections']]
                metrics[name]['costs'] = {'policy_requests': sum(row['state']['episode']['charged'] for row in finals),
                    'service_proposals': sum(a['operation'] == 'action-correction' for row in finals for a in row['audit']),
                    'correction_verifier_calls': sum(e['verification']['checked'] for e in events),
                    'accepted_replacements': sum(e['accepted'] for e in events),
                    'rejected_correction_events': sum(not e['accepted'] for e in events),
                    'late_reports_admitted': sum(late_record(row['case'])['evidence_id'] in row['state']['judgment']['ledger'] for row in finals),
                    'late_registration_checks': sum(a.get('registration_checks', 0) for row in finals for a in row['audit']),
                    'duplicate_admissions': 0, 'preparation_corrections': 0}
        for key in CASES:
            for control in CONTROLS:
                full = continuous[f'{key}/full/{control}']; memory = continuous[f'{key}/memory/{control}']
                checks[key + '/' + control + '/memory_evidence_prediction'] = full['probe'] == memory['probe']
                checks[key + '/' + control + '/memory_ledger'] = full['state']['judgment'] == memory['state']['judgment']
                checks[key + '/' + control + '/memory_action'] = full['state']['episode']['selected'] == memory['state']['episode']['selected']
                ftrace = full['state']['episode']['trace']['questions']; mtrace = memory['state']['episode']['trace']['questions']
                checks[key + '/' + control + '/memory_scores'] = [r['score'] for r in ftrace if 'score' in r] == [r['score'] for r in mtrace if 'score' in r]
        for key, row in continuous.items():
            initial = pending[key]['state']['judgment']; final = row['state']['judgment']; late = row['control'] == 'late'
            checks[key + '/originals'] = all(final['ledger'][k] == v for k,v in initial['ledger'].items())
            checks[key + '/roots'] = len(final['heads']) == len(initial['heads']) + int(late)
            checks[key + '/stored'] = len(final['ledger']) == len(initial['ledger']) + 1 + int(late)
            checks[key + '/fixed_numerics'] = all(final[k] == initial[k] for k in ('weights', 'branches', 'policy'))
            checks[key + '/single_charge'] = row['state']['episode']['charged'] == 1
            accepted = next(e for e in final['corrections'] if e['accepted'])
            target = accepted['proposal']['target_id']; replacement = accepted['proposal']['replacement']['evidence_id']
            checks[key + '/lineage'] = final['heads'][target] == replacement and final['ledger'][replacement]['parent'] == target
        atomic_json(root / 'stale-companion.json', stale_companion())
        checks['stale_companion'] = True
        preservation.pinned_current(root, Path.cwd())
        checks['archive_hashes'] = all(preservation.file_hash(root / 'archive' / n) == h for n,h in context['files'].items())
        result = {'checks': checks, 'integrity_passed': sum(checks.values()), 'integrity_total': len(checks),
                  'metrics': metrics, 'model_calls': 0, 'restart_pids': pids}
        atomic_json(root / 'results.json', result)
        print(json.dumps({k:v for k,v in result.items() if k != 'checks'}))
        if not all(checks.values()):
            raise AssertionError('sequential study checks failed')
        return result
    except Exception as exc:
        atomic_json(root / 'failure.json', {'error': repr(exc)}); raise


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path)
    parser.add_argument('--preservation-context', type=Path); parser.add_argument('--reload', type=Path)
    parser.add_argument('--stage'); parser.add_argument('--input', type=Path); parser.add_argument('--input-sha256')
    args = parser.parse_args()
    if args.reload:
        worker(args.reload, args.stage, args.input, args.input_sha256)
    elif args.output and args.preservation_context:
        run(args.output, args.preservation_context)
    else:
        parser.error('fresh output and preservation context required')


if __name__ == '__main__':
    main()
