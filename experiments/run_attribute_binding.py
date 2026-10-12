"""Frozen attribute-binding experiment; coordinator alone owns oracle mappings."""
import argparse
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import uuid
import attribute_binding_contract as contract
import attribute_binding_engine as engine
import attribute_binding_oracle as oracle
from lmft_lab import preservation_context as preservation
from lmft_lab.runtime_store import atomic_json

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT/'experiments/ATTRIBUTE_BINDING_PROTOCOL.md'
PROTOCOL_SHA256 = 'b1724989ab0c92bf6d78050f056702c3e811d96dfd9ac829d4e6a3bde48f40e7'


def item(record, receipt):
    return {'record': deepcopy(record), 'verified_digest': receipt}


def training_items(mapping, supported):
    records = oracle.training(mapping, supported)
    first = records[0]
    malformed = {**first, 'outcome': int(first['outcome'])}
    unverified = {**first, 'outcome': not first['outcome']}
    wrong_source = {**first, 'source': 'self-asserted'}
    result = [item(malformed, oracle.verify(mapping, malformed)),
              item(unverified, oracle.verify(mapping, unverified)), item(wrong_source, None)]
    result += [item(record, oracle.verify(mapping, record)) for record in records]
    result += [item(first, oracle.verify(mapping, first)), item(unverified, None)]
    return result


def acquisition_items(mapping, selected, first_training):
    # Boundary probes do not request extra oracle observations.
    result = [item(first_training, contract.digest(first_training))]
    if selected is None:
        return result
    record = oracle.record(mapping, selected['id'], 'acquisition', selected['channels'])
    malformed = {**record, 'outcome': int(record['outcome'])}
    false_label = {**record, 'outcome': not record['outcome']}
    unrelated = {**record, 'id': 'q999'}
    # A valid local attestation cannot authorize the wrong selected identity.
    result += [item(malformed, None), item(false_label, None),
               item(unrelated, oracle.verify(mapping, unrelated)),
               item(record, oracle.verify(mapping, record)), item(record, contract.digest(record)),
               item(false_label, None)]
    return result


def worker_stage(directory, request, prior=None):
    directory.mkdir(parents=True, exist_ok=False)
    atomic_json(directory/'request.json', request)
    if prior is not None:
        atomic_json(directory/'input-checkpoint.json', prior)
    env = dict(os.environ)
    env['PYTHONPATH'] = str(ROOT/'src') + os.pathsep + str(ROOT/'experiments')
    result = subprocess.run([sys.executable, str(ROOT/'experiments/attribute_binding_worker.py')],
        cwd=directory, env=env, capture_output=True, text=True, timeout=30,
        creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    atomic_json(directory/'process.json', {'returncode': result.returncode, 'stdout': result.stdout,
                                         'stderr': result.stderr, 'parent_pid': os.getpid()})
    if result.returncode:
        error = (directory/'error.json').read_text() if (directory/'error.json').exists() else result.stderr
        raise AssertionError('worker failed: '+error)
    return (json.loads((directory/'output-checkpoint.json').read_text()),
            json.loads((directory/'result.json').read_text()))


def begin_arm(directory, implementation, policy, items):
    request = {'stage': 'training', 'implementation': implementation, 'policy': policy, 'items': items}
    checkpoint, report = worker_stage(directory/'stage1', request)
    continuous, predicted = engine.transition(deepcopy(request))
    checks = {'training_restart_equivalent': checkpoint['state'] == continuous and predicted == report['predictions'],
              'training_predictions_readonly': contract.digest(continuous) == report['state_digest'],
              'no_oracle_import_stage1': not report['oracle_imported']}
    return {'directory': directory, 'checkpoint': checkpoint, 'before': deepcopy(checkpoint['state']),
            'before_predictions': deepcopy(report['predictions']), 'continuous': continuous,
            'reports': [report], 'checks': checks, 'training_request_digest': contract.digest(request)}


def end_arm(arm, items):
    previous = deepcopy(arm['checkpoint'])
    state = previous['state']
    request = {'stage': 'acquisition', 'implementation': state['implementation'], 'policy': state['policy'], 'items': items}
    acquired, report = worker_stage(arm['directory']/'stage2', request, previous)
    continuous, predicted = engine.transition(deepcopy(request), arm['continuous'])
    arm['checks'].update(acquisition_restart_equivalent=acquired['state'] == continuous and predicted == report['predictions'],
                         pending_loaded_exactly=report['loaded_digest'] == previous['state_digest'],
                         no_oracle_import_stage2=not report['oracle_imported'])
    request = {'stage': 'evaluate', 'implementation': state['implementation'], 'policy': state['policy'], 'items': []}
    evaluated, final = worker_stage(arm['directory']/'stage3', request, acquired)
    continuous, predicted = engine.transition(deepcopy(request), continuous)
    checks = arm['checks']
    checks.update(evaluation_restart_equivalent=evaluated['state'] == continuous and predicted == final['predictions'],
                  evaluation_loaded_exactly=final['loaded_digest'] == acquired['state_digest'],
                  evaluation_state_unchanged=evaluated == acquired,
                  no_oracle_import_stage3=not final['oracle_imported'],
                  three_distinct_child_pids=len({r['pid'] for r in arm['reports']+[report, final]}) == 3,
                  children_not_parent=all(r['pid'] != os.getpid() for r in arm['reports']+[report, final]),
                  budget_not_reset=evaluated['state']['budget_spent'] == previous['state']['budget_spent'],
                  evidence_survives=all(evaluated['state']['evidence'][key] == entry for key, entry in previous['state']['evidence'].items()),
                  query_preserved=evaluated['state']['query'] == previous['state']['query'],
                  rejection_history_survives=evaluated['state']['events'][:len(previous['state']['events'])] == previous['state']['events'],
                  duplicate_and_rejection_exercised={r['status'] for r in evaluated['state']['events']} >= {'accepted','duplicate','rejected'})
    arm.update(after=deepcopy(evaluated['state']), after_predictions=deepcopy(final['predictions']),
               reports=arm['reports']+[report, final])
    atomic_json(arm['directory']/'checks.json', checks)
    if not all(checks.values()):
        raise AssertionError([key for key, value in checks.items() if not value])
    return arm


def archive_current(root, context_path):
    context = json.loads(context_path.read_text())
    preservation.verify_current(context, ROOT)
    if preservation.file_hash(PROTOCOL) != PROTOCOL_SHA256:
        raise ValueError('frozen protocol hash changed')
    for name in context['files']:
        dest = root/'archive'/name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT/name, dest)
    shutil.copy2(context_path, root/'current-preservation-context.json')
    atomic_json(root/'archive-manifest.json', context['files'])
    atomic_json(root/'provenance.json', {'source_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'working_tree': subprocess.check_output(['git','status','--short'],cwd=ROOT,text=True),
        'protocol_sha256': PROTOCOL_SHA256, 'code_pin': contract.code_pin(),
        'preservation_kind': preservation.KIND, 'preservation_context_sha256': preservation.file_hash(context_path),
        'model_calls': 0, 'randomization': 'none in science; opaque UUIDs only for learner directories'})
    return context


def run(root, context_path, permutations=None):
    root = root.resolve(); root.mkdir(parents=True, exist_ok=False)
    try:
        context = archive_current(root, context_path.resolve())
        atomic_json(root/'public-configuration.json', contract.configuration())
        catalog = engine.primary.catalog()
        atomic_json(root/'public-classes.json', catalog)
        checks = {'36_representations': len(contract.representations()) == 36,
                  '18_behavioral_classes': len(catalog) == 18,
                  'equivalence_members_retained': sum(len(c['members']) for c in catalog.values()) == 36,
                  'independent_catalog_agreement': catalog == engine.memory.catalog()}
        indices = list(range(6)) if permutations is None else permutations
        (root/'evaluator').mkdir()
        atomic_json(root/'evaluator/mappings.json', {str(i): list(oracle.MAPPINGS[i]) for i in indices})
        arms, index = {}, []
        for number in indices:
            mapping = oracle.MAPPINGS[number]
            for policy in contract.POLICIES:
                supplied = training_items(mapping, policy == 'already-supported')
                first = next(item['record'] for item in supplied if item['verified_digest'] is not None)
                for implementation in ('primary', 'memory'):
                    preservation.pinned_current(root, ROOT)
                    # Directory names have no mapping/condition encoding. Workers get
                    # fixed local filenames and a strictly public request, not this key.
                    identity = uuid.uuid4().hex
                    directory = root/'learners'/identity
                    key = f'{number}/{policy}/{implementation}'
                    arm = begin_arm(directory, implementation, policy, deepcopy(supplied))
                    selected = arm['before']['query']['selected']
                    replies = acquisition_items(mapping, selected, first)
                    end_arm(arm, replies)
                    arms[key] = arm
                    index.append({'key': key, 'directory': f'learners/{identity}'})
        atomic_json(root/'evaluator/arm-index.json', index)
        # Freeze the ENTIRE prediction set before ANY held-out outcome scoring.
        frozen = {key: {'before': arm['before_predictions'], 'after': arm['after_predictions']} for key, arm in arms.items()}
        atomic_json(root/'frozen-predictions.json', frozen)
        prediction_hash = preservation.file_hash(root/'frozen-predictions.json')
        state_hashes = {key: contract.digest(arm['after']) for key, arm in arms.items()}
        evaluations, summaries = {}, []
        for key, arm in arms.items():
            number, policy, implementation = key.split('/')
            mapping = oracle.MAPPINGS[int(number)]
            before, after = oracle.score(mapping, frozen[key]['before']), oracle.score(mapping, frozen[key]['after'])
            evaluations[key] = {'before': before, 'after': after}
            summaries.append({'permutation': int(number), 'policy': policy, 'implementation': implementation,
                              'before_classes': arm['before']['analysis']['survivors'],
                              'after_classes': arm['after']['analysis']['survivors'],
                              'selected': arm['before']['query']['selected'], 'spent': arm['after']['budget_spent'],
                              'before': before['overall'], 'after': after['overall'],
                              'after_distractor_invariant': after['distractor_invariant']})
            checks[key+'/read_only_scoring'] = contract.digest(arm['after']) == state_hashes[key]
        atomic_json(root/'evaluator/scores.json', evaluations)
        for number in indices:
            for policy in contract.POLICIES:
                a, b = arms[f'{number}/{policy}/primary'], arms[f'{number}/{policy}/memory']
                checks[f'{number}/{policy}/independent_memory_parity'] = all(
                    engine.science(a[phase]) == engine.science(b[phase]) and a[phase+'_predictions'] == b[phase+'_predictions']
                    for phase in ('before','after'))
        leakage = []
        for policy in contract.POLICIES[:-1]:
            for implementation in ('primary','memory'):
                groups = {}
                for key, arm in arms.items():
                    if key.split('/')[1:] == [policy, implementation]:
                        groups.setdefault(arm['training_request_digest'], []).append((key, arm))
                for digest, rows in groups.items():
                    if len(rows) > 1:
                        same = all(r[1]['before'] == rows[0][1]['before'] and
                                   r[1]['before_predictions'] == rows[0][1]['before_predictions'] for r in rows)
                        leakage.append({'policy': policy, 'implementation': implementation,
                                        'request_digest': digest, 'coordinator_keys': [r[0] for r in rows], 'identical_public_state': same})
                if len(indices) == 6:
                    checks[policy+'/'+implementation+'/indistinguishable_pairs'] = sorted(map(len, groups.values())) == [2,2,2]
        checks['indistinguishable_history_no_mapping_leak'] = all(row['identical_public_state'] for row in leakage)
        checks['frozen_predictions_unchanged'] = preservation.file_hash(root/'frozen-predictions.json') == prediction_hash
        checks['source_archive_intact'] = all(preservation.file_hash(root/'archive'/name) == h for name,h in context['files'].items())
        preservation.pinned_current(root, ROOT)
        atomic_json(root/'leakage-checks.json', leakage)
        values = list(checks.values()) + [v for arm in arms.values() for v in arm['checks'].values()]
        scientific = all(row['after']['coverage'] == 1 and row['after']['accuracy'] == 1 and row['after_distractor_invariant']
                         for row in summaries if row['policy'] in ('informative','already-supported'))
        result = {'integrity_passed': sum(values), 'integrity_total': len(values), 'checks': checks,
                  'scientific_positive_informative_and_supported': scientific, 'summaries': summaries,
                  'permutations': indices, 'model_calls': 0, 'logical_queries': sum(row['spent'] for row in summaries),
                  'frozen_predictions_sha256': prediction_hash,
                  'indistinguishable_pair_comparisons': len(leakage)}
        atomic_json(root/'results.json', result)
        if not all(values):
            raise AssertionError('integrity failure; retain this run')
        hashes = {p.relative_to(root).as_posix(): preservation.file_hash(p) for p in root.rglob('*') if p.is_file()}
        atomic_json(root/'artifact-hashes.json', hashes)
        print(json.dumps({k:v for k,v in result.items() if k not in ('checks','summaries')}))
        return result
    except Exception as exc:
        atomic_json(root/'failure.json', {'error': repr(exc)})
        raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--preservation-context', required=True, type=Path)
    parser.add_argument('--permutation', type=int, choices=range(6), help='Deterministic targeted rerun: same frozen policies and cases')
    args = parser.parse_args()
    run(args.output, args.preservation_context, None if args.permutation is None else [args.permutation])
