"""Frozen isolated context-applicability matrix; private coordinator, never learner."""
import argparse
from copy import deepcopy
from collections import defaultdict
import hashlib
import json
import os
from pathlib import Path
import queue
import shutil
import subprocess
import sys
import threading
import time
import uuid

import context_applicability_contract as c
import context_applicability_device as device
import context_applicability_engine as engine
from lmft_lab.runtime_store import Store, atomic_json

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL_SHA256 = '8b16c1e2f43d5593dea56de3bfc0f25c761ba461d3d5490cb3e636defb0223a2'
DRAFT_SHA256 = '33d7dfcc5daee064b8508f0d02b2cd99a35cfe658493e8e4310c263d5d51b8b2'


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def archive_source(output):
    names = subprocess.check_output(['git', 'ls-files', '-z', '--cached', '--others', '--exclude-standard'],
                                    cwd=ROOT).decode().split('\0')[:-1]
    hashes = {}
    for name in names:
        source = ROOT / name
        if not source.is_file():
            continue
        target = output / 'source' / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        hashes[name] = file_hash(source)
        assert file_hash(target) == hashes[name]
    atomic_json(output / 'source-hashes.json', hashes)
    (output / 'git-status.txt').write_bytes(subprocess.check_output(['git', 'status', '--short'], cwd=ROOT))
    return hashes


def registry_verifier(records, transcript):
    """Receiver-side exact registry, independent of primary/memory computations."""
    allowed = [r for r in records if r is not None]

    def verify(record):
        accepted = any(c.exact(record, r) for r in allowed)
        transcript.append({'record': deepcopy(record), 'accepted': accepted})
        return accepted
    return verify


def worker(root, controller, schedule, stage, events, cases, registered, artifact):
    root = Path(root).resolve(); root.mkdir(parents=True, exist_ok=True)
    artifact = Path(artifact); artifact.parent.mkdir(parents=True, exist_ok=True)
    request = {'events': events, 'cases': cases}
    atomic_json(artifact.with_suffix('.input.json'), request)
    env = dict(os.environ, PYTHONPATH=str(ROOT / 'src'), PYTHONDONTWRITEBYTECODE='1')
    command = [sys.executable, str(ROOT / 'experiments/context_applicability_worker.py'),
               '--controller', controller, '--schedule', schedule, '--stage', stage]
    process = subprocess.Popen(command, cwd=root, env=env, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                               creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    lines = queue.Queue()

    def drain():
        for line in process.stdout:
            lines.put(line)
        lines.put(None)

    thread = threading.Thread(target=drain, daemon=True); thread.start()
    transcript = []; result = None; error = None
    verify = registry_verifier(registered, transcript)
    try:
        process.stdin.write(c.canonical(request) + '\n'); process.stdin.flush()
        deadline = time.monotonic() + 45
        while True:
            line = lines.get(timeout=max(.01, deadline - time.monotonic()))
            if line is None:
                break
            reply = json.loads(line)
            if reply.get('kind') == 'verify' and set(reply) == {'kind', 'record'}:
                accepted = verify(reply['record'])
                process.stdin.write(c.canonical({'accepted': accepted}) + '\n'); process.stdin.flush()
            elif reply.get('kind') == 'result' and result is None:
                result = reply
            else:
                raise ValueError('invalid worker output')
        process.wait(timeout=5)
    except Exception as exc:
        error = repr(exc)
        process.kill(); process.wait(timeout=5)
    finally:
        process.stdin.close(); thread.join(timeout=5)
        stderr = process.stderr.read()
        process.stdout.close(); process.stderr.close()
    record = {'returncode': process.returncode, 'stderr': stderr, 'error': error,
              'verification': transcript, 'result': result}
    atomic_json(artifact.with_suffix('.json'), record)
    if error or process.returncode or result is None:
        raise RuntimeError(f'worker failed; retained {artifact.with_suffix(".json")}')
    return record


def behavior(row):
    return {key: deepcopy(row[key]) for key in ('mapping', 'cross_by_mapping', 'prediction',
            'reasons', 'normalized_second', 'cross_part_disagreement')} | {
            'support': {k: deepcopy(row['support'][k]) for k in
                        ('first', 'second', 'within_part', 'complete', 'error')}}


def staged_events(initial, follow):
    pre = [engine.event(initial), engine.event(initial)]
    post = [engine.event(initial), engine.event(operation='opportunity')]
    if follow is not None:
        post += [engine.event(follow), engine.event(follow)]
    return pre, post


def run_individual(root, controller, schedule, initial, follow, cases, artifacts):
    pre_events, post_events = staged_events(initial, follow)
    registered = [initial, follow]
    pre = worker(root, controller, schedule, 'initial', pre_events, cases, registered, artifacts / 'pre')
    before = (root / 'checkpoint.json').read_bytes()
    (artifacts / 'pre-checkpoint.json').write_bytes(before)
    post = worker(root, controller, schedule, 'followup', post_events, cases, registered, artifacts / 'post')
    after = (root / 'checkpoint.json').read_bytes()
    (artifacts / 'post-checkpoint.json').write_bytes(after)
    reload = worker(root, controller, schedule, 'reload', [], cases, registered, artifacts / 'reload')
    checks = {'reload_bytes_unchanged': after == (root / 'checkpoint.json').read_bytes(),
              'restart_state_exact': c.exact(post['result']['state'], reload['result']['state']),
              'restart_predictions_exact': c.exact(post['result']['predictions'], reload['result']['predictions']),
              'initial_checks': len(pre['verification']) == 1,
              'followup_checks': len(post['verification']) == int(follow is not None),
              'reload_no_checks': not reload['verification'],
              'single_charge': post['result']['state']['charged'] == 1}
    # Uninterrupted independent lifecycle, identical public events and verifier inputs.
    state = engine.newborn(controller, schedule); verification = []
    verify = registry_verifier(registered, verification)
    continuous = {}
    for stage, events in (('pre', pre_events), ('post', post_events)):
        for item in events:
            state = engine.advance(state, item, verify)
        predictions = engine.evaluate(state, cases)
        continuous[stage] = {'state': deepcopy(state), 'predictions': predictions}
        actual = (pre if stage == 'pre' else post)['result']
        checks[stage+'_continuous_state'] = c.exact(state, actual['state'])
        checks[stage+'_continuous_predictions'] = c.exact(predictions, actual['predictions'])
        checks[stage+'_identity_invariance'] = c.exact(list(map(behavior, actual['predictions'])),
                                                      list(map(behavior, actual['renamed'])))
        checks[stage+'_raw_preserved'] = all(c.exact(row['support']['raw_records'], case['records'])
                                            for row, case in zip(actual['predictions'], cases))
        # The scientific grid has target0/target1 blocks within each context.
        # Other integrity-only case lists deliberately do not use this ordering.
        if len(cases) == 56:
            pairs = [(actual['predictions'][ci*14+ti], actual['predictions'][ci*14+7+ti])
                     for ci in range(4) for ti in range(7)]
            checks[stage+'_support_value_flip'] = all(
                a['mapping'] == b['mapping'] and a['reasons'] == b['reasons']
                and ((a['prediction'] is None and b['prediction'] is None)
                     or (a['prediction'] is not None and b['prediction'] == 1-a['prediction']))
                and a['support']['within_part'] == b['support']['within_part']
                and a['cross_part_disagreement'] == b['cross_part_disagreement'] for a, b in pairs)
    atomic_json(artifacts / 'uninterrupted.json', {'stages': continuous, 'verification': verification})
    atomic_json(artifacts / 'checks.json', checks)
    return {'pre': pre['result'], 'post': post['result'], 'reload': reload['result'], 'checks': checks}


def counts(predictions, labels, selected):
    correct = wrong = abstained = unsafe = 0
    for prediction, label in zip(predictions, labels):
        if not selected(label):
            continue
        emitted = prediction['prediction']
        if emitted is None:
            abstained += 1
        else:
            correct += int(emitted == label['target']); wrong += int(emitted != label['target'])
            unsafe += int(not label['oracle_resolved'])
    total = correct + wrong + abstained
    return {'total': total, 'correct': correct, 'wrong': wrong, 'abstained': abstained,
            'unsafe': unsafe, 'coverage': (correct+wrong)/total if total else None,
            'accuracy': correct/(correct+wrong) if correct+wrong else None}


def summarize(arms):
    rows = []; mapping_rows = []
    for arm in arms:
        cases, labels = device.evaluation(arm['world'])
        calibrated = [[0, 0]] + ([c.SCHEDULES[arm['schedule']][0]] if arm['schedule'] != 'U10' else [])
        groups = {'all': lambda label: True,
                  'retention': lambda label: label['context'] == [0, 0],
                  'transfer': lambda label: label['context'] not in calibrated,
                  'followup_context': lambda label: label['context'] != [0, 0] and label['context'] in calibrated}
        for controller, individual in arm['individuals'].items():
            for stage in ('pre', 'post'):
                output = individual[stage]
                for category, select in groups.items():
                    rows.append({'world': arm['world'], 'schedule': arm['schedule'], 'flip': arm['flip'],
                                 'controller': controller, 'stage': stage, 'category': category,
                                 **counts(output['predictions'], labels, select)})
                for template in device.TEMPLATES:
                    rows.append({'world': arm['world'], 'schedule': arm['schedule'], 'flip': arm['flip'],
                                 'controller': controller, 'stage': stage, 'category': 'template:'+template,
                                 **counts(output['predictions'], labels, lambda label: label['template'] == template)})
                correct = wrong = ambiguous = unsupported = 0
                for ctx, prediction in zip(c.CONTEXTS, output['mappings']):
                    raw, z = device.measure(arm['world'], ctx, 0)
                    if prediction['mapping'] is None:
                        ambiguous += int(prediction['status'] == 'mapping_ambiguous')
                        unsupported += int(prediction['status'] == 'unsupported')
                    else:
                        correct += int(prediction['mapping'] == (raw ^ z))
                        wrong += int(prediction['mapping'] != (raw ^ z))
                mapping_rows.append({'world': arm['world'], 'schedule': arm['schedule'], 'flip': arm['flip'],
                                     'controller': controller, 'stage': stage, 'total': 4,
                                     'correct': correct, 'wrong': wrong, 'ambiguous': ambiguous,
                                     'unsupported': unsupported,
                                     'survivor_count': len(output['state']['decision_analysis']['survivors'])})
    aggregates = []
    for controller in c.CONTROLLERS:
        for stage in ('pre', 'post'):
            for category in ('all', 'retention', 'transfer', 'followup_context'):
                selected = [r for r in rows if (r['controller'], r['stage'], r['category']) == (controller, stage, category)]
                sums = {key: sum(r[key] for r in selected) for key in ('total', 'correct', 'wrong', 'abstained', 'unsafe')}
                sums['coverage'] = (sums['correct']+sums['wrong'])/sums['total'] if sums['total'] else None
                sums['accuracy'] = sums['correct']/(sums['correct']+sums['wrong']) if sums['correct']+sums['wrong'] else None
                aggregates.append({'controller': controller, 'stage': stage, 'category': category, **sums})
    return {'per_arm': rows, 'mapping_per_arm': mapping_rows, 'aggregate': aggregates}


def cross_checks(arms):
    checks = {}; groups = defaultdict(list)
    for index, arm in enumerate(arms):
        for controller, item in arm['individuals'].items():
            for stage in ('pre', 'post'):
                output = item[stage]
                key = (controller, arm['schedule'], stage, c.digest(output['state']['events']))
                groups[key].append((index, output))
        for stage in ('pre', 'post'):
            p = arm['individuals']['primary'][stage]; m = arm['individuals']['memory'][stage]
            checks[f'{index}/{stage}/memory-state'] = c.exact(engine.scientific(p['state']), engine.scientific(m['state']))
            for key in ('predictions', 'renamed', 'probes', 'mappings'):
                checks[f'{index}/{stage}/memory-{key}'] = c.exact(p[key], m[key])
    paired = []
    for key, members in groups.items():
        first = members[0][1]
        valid = all(c.exact(engine.scientific(first['state']), engine.scientific(other['state']))
                    and c.exact(first['mappings'], other['mappings'])
                    and c.exact(first['probes'], other['probes']) for _, other in members)
        group = {'controller': key[0], 'schedule': key[1], 'stage': key[2], 'history_sha256': key[3],
                 'arm_indices': [i for i, _ in members], 'equal': valid}
        paired.append(group)
        checks['indistinguishable/'+str(len(paired))] = valid
    # Flip changes raw/reference calibration bits together, preserving all inferred mappings.
    lookup = {(a['world'], a['schedule'], a['flip']): a for a in arms}
    for world in device.WORLDS:
        for schedule in c.SCHEDULES:
            first = lookup[world, schedule, 0]; flipped = lookup[world, schedule, 1]
            for controller in c.CONTROLLERS:
                for stage in ('pre', 'post'):
                    a = first['individuals'][controller][stage]; b = flipped['individuals'][controller][stage]
                    checks[f'flip/{world}/{schedule}/{controller}/{stage}'] = (
                        c.exact(a['mappings'], b['mappings']) and c.exact(a['predictions'], b['predictions'])
                        and c.exact(a['state']['analysis'], b['state']['analysis']))
    return checks, paired


def run(output, pin_path):
    output = Path(output).resolve(); output.mkdir(parents=True, exist_ok=False)
    pin = json.loads(Path(pin_path).read_text(encoding='utf-8'))
    if (pin['protocol_sha256'] != PROTOCOL_SHA256 or file_hash(ROOT / c.PROTOCOL) != PROTOCOL_SHA256
            or file_hash(ROOT / 'experiments/CONTEXT_APPLICABILITY_PROTOCOL_DRAFT.md') != DRAFT_SHA256):
        raise ValueError('protocol/draft pin mismatch')
    atomic_json(output / 'protocol-pin.json', pin)
    hashes = archive_source(output)
    # Allocate opaque worker roots first; assignments never enter workers or directory names.
    allocations = [[uuid.uuid4().hex for _ in c.CONTROLLERS] for _ in range(48)]
    atomic_json(output / 'allocations.json', allocations)
    arms = []; all_checks = {}; predictions_pin = {}
    try:
        for world in device.WORLDS:
            for schedule in c.SCHEDULES:
                for flip in (0, 1):
                    index = len(arms); initial, follow = device.calibrations(world, schedule, flip)
                    cases, _ = device.evaluation(world)
                    arm = {'world': world, 'schedule': schedule, 'flip': flip, 'individuals': {}}
                    for ci, controller in enumerate(c.CONTROLLERS):
                        token = allocations[index][ci]
                        root = output / 'workers' / token
                        artifacts = output / 'traces' / token
                        artifacts.mkdir(parents=True, exist_ok=False)
                        result = run_individual(root, controller, schedule, initial, follow, cases, artifacts)
                        arm['individuals'][controller] = result
                        for name, ok in result['checks'].items():
                            all_checks[f'{index}/{controller}/{name}'] = ok
                        for stage in ('pre', 'post'):
                            path = artifacts / (stage+'.json')
                            predictions_pin[path.relative_to(output).as_posix()] = file_hash(path)
                    arms.append(arm)
                    print(f'Completed arm {len(arms)}/48', flush=True)
        # All primary predictions across all arms/stages are frozen before scoring.
        atomic_json(output / 'prediction-hashes.json', predictions_pin)
        atomic_json(output / 'assignment.json', [{'world': a['world'], 'schedule': a['schedule'], 'flip': a['flip'],
                                                'tokens': allocations[i]} for i, a in enumerate(arms)])
        additional, paired = cross_checks(arms); all_checks.update(additional)
        atomic_json(output / 'indistinguishable-history.json', paired)
        results = summarize(arms)
        for row in results['per_arm']:
            if row['controller'] in ('primary', 'memory'):
                name = c.digest({k: row[k] for k in ('world', 'schedule', 'flip', 'controller', 'stage', 'category')})
                all_checks['sound/'+name] = row['wrong'] == row['unsafe'] == 0
        for name, digest in predictions_pin.items():
            all_checks['prediction_pin/'+name] = file_hash(output/name) == digest
        for name, digest in hashes.items():
            all_checks['source/'+name] = file_hash(ROOT/name) == digest and file_hash(output/'source'/name) == digest
        results.update({'protocol_sha256': PROTOCOL_SHA256, 'arm_count': 48, 'controllers': list(c.CONTROLLERS),
                        'individuals': 240, 'worker_invocations': 720, 'support_cases_per_stage': 56,
                        'model_calls': 0, 'costs': {
                            'physical_initial_reference_generations': 48, 'physical_followup_reference_generations': 36,
                            'logical_initial_per_controller': 48, 'logical_followup_opportunities_per_controller': 48,
                            'logical_followup_admissions_per_controller': 36,
                            'actual_worker_verification_checks': 420,
                            'uninterrupted_reference_checks': 420},
                        'integrity_checks': len(all_checks), 'integrity_passed': sum(all_checks.values())})
        atomic_json(output / 'results.json', results)
        atomic_json(output / 'integrity.json', all_checks)
        if not all(all_checks.values()):
            raise AssertionError('integrity gate failed')
        return results
    except Exception as exc:
        atomic_json(output / 'failure.json', {'error': repr(exc), 'completed_arms': len(arms)})
        raise


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--protocol-pin', type=Path, required=True)
    args = parser.parse_args()
    results = run(args.output, args.protocol_pin)
    print(c.canonical({'checks': results['integrity_checks'], 'passed': results['integrity_passed']}))


if __name__ == '__main__':
    main()
