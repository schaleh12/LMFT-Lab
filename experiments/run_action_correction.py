from lmft_lab.action_policy import DEFS, SOURCE, message, preflight, prepare, proposal, receive, request, select, semantic, service_reply, step
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
EXPECTED = {
    'full': ['correction', 'gather', None, 'correction', None, None, None, 'correction', 'correction', None, None, 'gather'],
    'memory': ['correction', 'gather', None, 'correction', None, None, None, 'correction', 'correction', None, None, 'gather'],
    'ablated': ['correction', 'gather', None, 'correction', None, None, None, 'correction', 'gather', None, None, 'gather'],
    'gather-only': [None, 'gather', None, None, None, None, None, None, 'gather', None, None, 'gather'],
    'original': ['gather', 'gather', 'gather', 'gather', 'gather', None, None, 'gather', 'gather', None, 'gather', 'gather'],
}






















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
