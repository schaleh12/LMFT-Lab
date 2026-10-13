"""Frozen engineering comparison; no production policy or learned state changes."""
import argparse
from copy import deepcopy
import hashlib
from itertools import product
import json
from pathlib import Path
import shutil
import subprocess
import traceback

from lmft_lab import action_policy as policy, consistent_attention as circuit
from lmft_lab import correction as repair, correction_fixture as fixture
from lmft_lab.runtime_store import digest
from run_action_correction import finish

CASES = ('r2', 'r4', 'r8', 'r9', 'r10', 'r12')
POLICIES = ('current', 'target', 'final')
PROTOCOL = 'experiments/INVESTIGATION_PRIORITY_PROTOCOL.md'


def domain_error(current, case):
    """Inspect raw effective values before normalization, sets or priorities.

    Preserve the original conservative boundary: every active record in this
    case/scope must be Boolean, even for an unrelated field. Foreign scopes/cases
    and superseded records are outside the inspected effective domain.
    """
    for head in current['heads'].values():
        record = current['ledger'][head]['record']
        if (record['case_id'] == case['case_id'] and record['scope'] == case['scope']
                and type(record.get('value')) is not bool):
            return 'unsupported value domain'
    return None


def unknown_annotation(reason):
    return {'target': 'unknown', 'support_gate': 'unknown', 'final': 'unknown',
            'admission': 'unknown', 'witnesses': [], 'reason': reason}


def annotate(current, case, offer):
    """Boolean effect envelope, never an enumeration of authorized payloads."""
    unknown = unknown_annotation('unsupported operation or relation')
    error = domain_error(current, case)
    if error:
        return unknown_annotation(error)
    if offer.get('kind') not in ('gather', 'correction') or case.get('relation') not in ('equal', 'complement'):
        return {**unknown, 'reason': 'unsupported operation or relation'}
    reason = policy.preflight(current, case, offer)
    if reason:
        return {**unknown, 'reason': 'ineligible: ' + reason}
    view = repair.effective(current)
    parts = offer['parts'] if offer['kind'] == 'gather' else [offer['coordinate']['part']]
    witnesses = []
    for values in product((False, True), repeat=len(parts)):
        hypothetical = deepcopy(view)
        if offer['kind'] == 'correction':
            hypothetical['ledger'][offer['target_id']]['record']['value'] = values[0]
        else:
            for part, value in zip(parts, values):
                eid = '__effect__/' + part
                while eid in hypothetical['ledger']:
                    eid += '_'
                hypothetical['ledger'][eid] = {'record': {'case_id': case['case_id'],
                    'scope': case['scope'], 'question': offer['field'], 'part': part,
                    'value': value, 'evidence_id': eid}}
        prediction = circuit.predict(hypothetical, case)
        support = prediction['support']
        gate = support['shielded']['resolved'] and support['payload_valid']['resolved'] and support['payload_valid']['value'] is True
        witnesses.append({'values': list(values), 'target': support[offer['field']]['resolved'],
                          'support_gate': gate, 'final': prediction['decision'] != 'abstain'})
    return {**{k: 'possible' if any(w[k] for w in witnesses) else 'ruled_out'
               for k in ('target', 'support_gate', 'final')},
            'admission': 'unknown', 'witnesses': witnesses,
            'reason': 'complete Boolean public-effect envelope; admission and actual value unknown'}


def choose(bundle, objective, scalar=False):
    current, case, offers = bundle['state']['judgment'], bundle['case'], bundle['offers']
    before = digest(bundle)
    error = domain_error(current, case)
    if error:
        trace = {'questions': [], 'domain': 'unknown', 'reason': error,
                 'actions': [{'offer': deepcopy(o), 'rejection': error, 'score': None,
                              'feasibility': unknown_annotation(error)} for o in offers]}
        assert digest(bundle) == before
        return None, trace
    _, trace = policy.select(current, case, offers, 'memory' if scalar else 'full')
    annotations = {o['id']: annotate(current, case, o) for o in offers}
    ranked = []
    for row in trace['actions']:
        row['feasibility'] = annotations[row['offer']['id']]
        if row['rejection'] is None and objective != 'current' and row['feasibility'][objective] != 'possible':
            row['rejection'] = objective + ' feasibility: ' + row['feasibility'][objective]
        if row['rejection'] is None:
            ranked.append((row['score'], row['offer']['id'], row['offer']))
    ranked.sort(key=lambda item: (-item[0], item[1]))
    assert digest(bundle) == before
    return (deepcopy(ranked[0][2]) if ranked else None), trace


def pending(bundle, objective, scalar=False):
    state = deepcopy(bundle['state'])
    if 'episode' in state:
        return state
    selected, trace = choose(bundle, objective, scalar)
    state['episode'] = {'selected': selected, 'trace': trace, 'charged': int(selected is not None),
                        'status': 'pending' if selected else 'closed', 'reply_digest': None}
    if selected:
        state['questions']['action-request'] = {'case_id': bundle['case']['case_id'],
            'question': selected['field'], 'status': 'open', 'closed_by': None}
    return state


def x2_probe():
    # Decision-only view: preserve archived x2 observations/prior; never a service fixture.
    archived = json.loads(Path('outputs/seed-contribution-003/results.json').read_text())
    row = next(r for r in archived['conditions']['intact'] if r['case_id'] == 'x2')
    current = repair.newborn('correction-lmft')
    for record in row['initial_records']:
        eid = record['evidence_id']
        current['ledger'][eid] = {'record': deepcopy(record), 'root': eid, 'parent': None}
        current['roots'][eid] = eid; current['heads'][eid] = eid
    prior = json.loads(Path('outputs/seed-contribution-003/frozen-prior.json').read_text())
    current['weights'] = deepcopy(prior['weights'])
    current['branches'] = deepcopy(prior['branches'])
    case = row['case']
    offers = [{'id': 'gather-' + field, 'kind': 'gather', 'field': field,
               'case_id': case['case_id'], 'scope': case['scope'], 'available': True,
               'parts': [p for p, v in circuit.support(repair.effective(current), case, field)['part_values'].items() if not v]}
              for field in ('shielded', 'payload_valid')]
    return {'state': {'judgment': current}, 'case': case, 'offers': offers}


def vector(row):
    before, after = row['before']['support'], row['after']['support']
    selected = row['selected']; kind = selected['kind'] if selected else None
    return {'selected': selected['id'] if selected else None,
        'newly_covered': [f + '/' + p for f in before for p in before[f]['part_values']
                          if not before[f]['part_values'][p] and after[f]['part_values'][p]],
        'coverage_gain': row['coverage_gain'], 'admitted_records': row['admitted_records'],
        'target_resolved': bool(selected and not before[selected['field']]['resolved'] and after[selected['field']]['resolved']),
        'questions_resolved': row['new_resolved'], 'decision': row['after']['decision'],
        'requests': int(selected is not None), 'gather_service_attempts': int(kind == 'gather'),
        'correction_service_attempts': int(kind == 'correction'),
        'returned_records': len(row['reply'].get('records', [])) if kind == 'gather' else 0,
        'returned_proposals': int(kind == 'correction'),
        'gather_checks': int(row['receipt'].get('verification_checked', False)),
        'correction_checks': sum(e['verification']['checked'] for e in row['action_events']),
        'remaining': {f: {'missing': [p for p, v in s['part_values'].items() if not v],
                           'inconsistent': s['inconsistent'], 'resolved': s['resolved'],
                           'part_values': s['part_values']} for f, s in after.items()}}


def write(root, name, value):
    (root / name).write_text(json.dumps(value, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--protocol-pin', type=Path, required=True); args = parser.parse_args()
    pin = json.loads(args.protocol_pin.read_text())
    if hashlib.sha256(Path(PROTOCOL).read_bytes()).hexdigest() != pin['sha256']:
        raise ValueError('protocol pin mismatch')
    root = args.output; root.mkdir(parents=True, exist_ok=False)
    try:
        files = sorted(set(subprocess.check_output(['git', 'ls-files', '-c', '-o', '--exclude-standard'], text=True).splitlines()))
        hashes = {}
        for name in files:
            p = Path(name)
            if p.is_file():
                hashes[name] = hashlib.sha256(p.read_bytes()).hexdigest()
                dest = root / 'source' / name; dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(p, dest)
        write(root, 'source-hashes.json', hashes); write(root, 'protocol-pin.json', pin)
        bundles = {key: policy.prepare(key) for key in CASES}
        write(root, 'inputs.json', bundles)
        frozen = {obj + ('-scalar' if scalar else '-circuit'): {key: pending(b, obj, scalar) for key, b in bundles.items()}
                  for obj in POLICIES for scalar in (False, True)}
        probes = {}
        x2 = x2_probe()
        for name, offers in [('both', x2['offers']), ('shield-only', x2['offers'][:1])]:
            b = {**x2, 'offers': offers}
            probes[name] = {obj + ('-scalar' if scalar else '-circuit'): choose(b, obj, scalar)
                            for obj in POLICIES for scalar in (False, True)}
        write(root, 'x2-decision-only-input.json', x2); write(root, 'x2-decision-only-results.json', probes)
        write(root, 'pending.json', frozen)  # All selections precede every selected service call.
        rows = {mode: {key: finish(state, bundles[key]['case']) for key, state in states.items()} for mode, states in frozen.items()}
        write(root, 'predictions.json', {m: {k: r['after'] for k, r in rr.items()} for m, rr in rows.items()})
        vectors = {m: {k: vector(r) for k, r in rr.items()} for m, rr in rows.items()}
        for rr in vectors.values():
            for key, v in rr.items():
                v['correct'] = None if v['decision'] == 'abstain' else (v['decision'] == 'success') == fixture.actual_success(policy.DEFS[key][0])
        checks = {m + '/' + k + '/' + n: ok for m, rr in rows.items() for k, r in rr.items() for n, ok in r['checks'].items()}
        for obj in POLICIES:
            checks[obj + '/scalar-vectors'] = vectors[obj + '-circuit'] == vectors[obj + '-scalar']
            checks[obj + '/scalar-selection'] = all(rows[obj+'-circuit'][k]['selected'] == rows[obj+'-scalar'][k]['selected'] for k in CASES)
        checks['sources_unchanged'] = all(hashlib.sha256(Path(p).read_bytes()).hexdigest() == h for p, h in hashes.items())
        write(root, 'results.json', {'vectors': vectors, 'rows': rows, 'checks': checks,
            'checks_passed': sum(checks.values()), 'checks_total': len(checks), 'model_calls': 0,
            'preparation_corrections_shared': sum(len(b['state']['judgment']['corrections']) for b in bundles.values())})
        print(json.dumps({'checks': [sum(checks.values()), len(checks)], 'sources': len(hashes), 'vectors': vectors['current-circuit']}))
        if not all(checks.values()):
            raise AssertionError('integrity failure; preserve this run')
    except Exception:
        write(root, 'failure.json', {'traceback': traceback.format_exc()}); raise


if __name__ == '__main__':
    main()
