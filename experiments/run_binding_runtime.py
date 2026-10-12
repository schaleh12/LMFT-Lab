"""Real supervised runtime binding integration; oracle remains harness-private."""
import argparse
from copy import deepcopy
import json
import os
from pathlib import Path
import secrets
import shutil
import subprocess
import sys
import uuid

import attribute_binding_oracle as oracle
from lmft_lab import binding_contract as contract, binding_runtime as binding
from lmft_lab import preservation_context as preservation, runtime
from lmft_lab.binding_verifier import Adapter, RULE as VERIFIER_RULE
from lmft_lab.runtime_store import Store, atomic_json, digest
from run_comparative import start, halt, send, check_boundary

ROOT = Path(__file__).resolve().parents[1]
PROTOCOL = ROOT/'experiments/BINDING_RUNTIME_PROTOCOL.md'
PROTOCOL_HASH = '9bc68f69b135890e64cdc56ec4321c0a35d75fc4aa4d434166cfccdf56ffe13e'


def command(identifier, operation, record=None, reply_to=None, source=None):
    value = {'schema_version': 1, 'id': identifier, 'sender': 'fixture-operator',
             'source': source or contract.SOURCE, 'type': 'teacher_reply' if reply_to else 'observation',
             'content': {'text': operation, 'operation': operation, 'record': deepcopy(record or {})}}
    if reply_to:
        value['reply_to'] = reply_to
    return value


def private_registry(path, mapping, supported=False):
    train = oracle.training(mapping, supported)
    queries = [oracle.record(mapping, q['id'], 'acquisition', q['channels']) for q in contract.query_pool('informative')]
    atomic_json(path, {'version': VERIFIER_RULE, 'identity': uuid.uuid4().hex,
                      'nonce': secrets.token_hex(32), 'records': {r['id']: r for r in train+queries}})
    return train


def science(current):
    return {key: deepcopy(value) for key, value in current.items() if key != 'mode'}


def semantic(state):
    value = deepcopy(state)
    for item in value['outbox']:
        item.pop('timestamp', None)
    for item in value['receipts']:
        item.pop('processing_seconds', None)
    # Birth dataclasses contain tuples in memory; JSON checkpoints contain lists.
    return json.loads(json.dumps(value))


def emitted(state, prefix):
    return [item['content']['result'] for item in state['outbox']
            if (item.get('reply_to') or '').startswith(prefix) and 'result' in item['content']]


def replay(previous, messages, verifier):
    state = deepcopy(previous)
    class NoModels:
        def complete(self, *a, **k):
            raise AssertionError('model inference forbidden')
    for item in messages:
        state = runtime.advance(state, (state['cursor']+1, item, None, json.dumps(item)),
                                NoModels(), binding_verifier=verifier)
    return state


def run_arm(directory, mode, condition, mapping, registry_path):
    directory.mkdir(parents=True, exist_ok=False)
    training = private_registry(registry_path, mapping, condition == 'already-supported')
    verifier = Adapter(registry_path)
    store = Store(directory/'individual'); checks = {}; stages = {}; processes = []; process = None
    extra = ['--binding-condition', condition, '--binding-registry', str(registry_path)]
    def launch(new=False):
        proc = start(store.root, mode, new=new, extra_args=extra)
        processes.append(proc.pid)
        return proc
    def stage(messages, name):
        nonlocal process
        items = messages + [command(name+'-barrier', 'barrier')]
        atomic_json(directory/(name+'-inputs.json'), items)
        send(store, process, items)
        state = halt(store, process); process = None
        atomic_json(directory/(name+'-state.json'), state)
        stages[name] = state
        return state, items
    try:
        process = launch(True)
        checks['live_inspection_denied'] = check_boundary(store)
        first = training[0]
        false_record = {**first, 'outcome': not first['outcome']}
        forged = {**false_record, 'verified_digest': contract.digest(false_record)}
        messages = [command('bad-boolean', 'train', {**first, 'outcome': int(first['outcome'])}),
                    command('bad-unverified', 'train', false_record), command('bad-digest', 'train', forged),
                    command('bad-source', 'train', first, source='self-asserted')]
        messages += [command('train-'+r['id'], 'train', r) for r in training]
        messages += [command('duplicate-record','train',first), command('bad-conflict','train',false_record)]
        messages += [command('select', 'select')]
        messages += [command('before-'+case['id'], 'evaluate', case) for case in contract.held_features()]
        before, items1 = stage(messages, 'pending')
        continuous = runtime.initial_state(before['individual_id'], True, before['manifest'], mode)
        continuous = replay(continuous, items1, verifier)
        checks['pending_direct_parity'] = semantic(continuous) == semantic(before)
        checks['pending_state_valid'] = binding.check_state(before['judgment'])
        rejected = {r.get('message_id') for r in before['receipts'] if r['status'] == 'rejected'}
        checks['inbox_training_rejections'] = {'bad-boolean','bad-unverified','bad-digest','bad-source','bad-conflict'} <= rejected
        checks['inbox_duplicate_no_learning'] = len(before['judgment']['evidence']) == len(training)
        selected = before['judgment']['query']['selected']; reply_to = before['judgment']['request_id']
        process = launch()
        messages = [command('bad-repeat-select','select'), command('bad-closed-training','train',{**first,'id':'t099'})]
        if selected:
            record = oracle.record(mapping, selected['id'], 'acquisition', selected['channels'])
            messages += [command('bad-correlation','reply',record,'unrelated'),
                         command('bad-query','reply',{**record,'id':'q999'},reply_to),
                         command('bad-reply-source','reply',record,reply_to,source='self-asserted'),
                         command('bad-reply-value','reply',{**record,'outcome':not record['outcome']},reply_to),
                         command('bad-premature-close','close')]
            messages.append(command('reply', 'reply', record, reply_to))
            messages.append(command('duplicate-reply','reply',record,reply_to))
        messages.append(command('close', 'close'))
        after, items2 = stage(messages, 'acquired')
        continuous = replay(continuous, items2, verifier)
        checks['acquired_direct_parity'] = semantic(continuous) == semantic(after)
        checks['acquired_state_valid'] = binding.check_state(after['judgment'])
        rejected = {r.get('message_id') for r in after['receipts'] if r['status'] == 'rejected'}
        expected_rejected = {'bad-repeat-select','bad-closed-training'}
        if selected:
            expected_rejected |= {'bad-correlation','bad-query','bad-reply-source','bad-reply-value','bad-premature-close'}
        checks['inbox_acquisition_rejections'] = expected_rejected <= rejected
        process = launch()
        final, items3 = stage([command('bad-evaluation-label','evaluate',{**contract.held_features()[0],'outcome':True})]
                             + [command('after-'+case['id'], 'evaluate', case) for case in contract.held_features()], 'evaluated')
        continuous = replay(continuous, items3, verifier)
        checks['evaluation_direct_parity'] = semantic(continuous) == semantic(final)
        checks['evaluation_learning_immutable'] = final['judgment'] == after['judgment']
        checks['evaluation_label_rejected'] = any(r.get('message_id')=='bad-evaluation-label' and r['status']=='rejected' for r in final['receipts'])
        checks['actual_process_restarts'] = len(set(processes)) == 3 and os.getpid() not in processes
        checks['model_calls_zero'] = final['diagnostics'] == []
        checks['outbox_kernel_parity'] = emitted(final, 'after-') == [binding.predict(final['judgment'], c) for c in contract.held_features()]
        checks['frozen_snapshot_persisted'] = before['judgment']['prediction_snapshot'] == final['judgment']['prediction_snapshot']
        checks['birth_unchanged'] = before['birth'] == final['birth']
        checks['public_mapping_absent'] = all('mapping' not in json.dumps(v) and str(registry_path) not in json.dumps(v) for v in stages.values())
        result = {'mode': mode, 'condition': condition, 'process_ids': processes, 'checks': checks,
                  'before': before['judgment'], 'after': final['judgment'],
                  'before_predictions': emitted(before, 'before-'), 'after_predictions': emitted(final, 'after-')}
        atomic_json(directory/'result.json', result)
        return result
    finally:
        if process is not None and process.poll() is None:
            halt(store, process)


def run(output, context_path, permutations):
    assert preservation.file_hash(PROTOCOL) == PROTOCOL_HASH, 'protocol changed'
    context = json.loads(Path(context_path).read_text())
    preservation.verify_current(context, ROOT)
    output.mkdir(parents=True, exist_ok=False)
    for name in context['files']:
        target = output/'archive'/name; target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT/name, target)
    shutil.copyfile(context_path, output/'current-preservation-context.json')
    atomic_json(output/'provenance.json', {'protocol_sha256': PROTOCOL_HASH,
        'preservation_kind': preservation.KIND, 'preservation_context_sha256': preservation.file_hash(context_path),
        'source_commit': subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        'source_inventory_digest': context['inventory_digest'], 'model_calls': 0})
    results = {}; index = {}; checks = {}
    (output/'private').mkdir()
    for permutation in permutations:
        for condition in binding.POLICIES:
            for mode in binding.MODES:
                key = f'{permutation}:{condition}:{mode}'; opaque = uuid.uuid4().hex
                directory = output/'arms'/opaque; registry_path = output/'private'/(uuid.uuid4().hex+'.json')
                result = run_arm(directory, mode, condition, oracle.MAPPINGS[permutation], registry_path)
                results[key] = result; index[key] = directory.relative_to(output).as_posix()
                checks.update({key+':'+name: passed for name,passed in result['checks'].items()})
                print(json.dumps({'completed_arm': key, 'checks_passed': all(result['checks'].values())}), flush=True)
    # All decisions are committed to disk before held-out oracle scoring begins.
    frozen = {key: {stage: row[stage+'_predictions'] for stage in ('before','after')} for key,row in results.items()}
    atomic_json(output/'frozen-predictions.json', frozen)
    frozen_hash = preservation.file_hash(output/'frozen-predictions.json')
    scores = {}
    for key,row in results.items():
        permutation, condition, mode = key.split(':')
        scores[key] = {stage: oracle.score(oracle.MAPPINGS[int(permutation)], frozen[key][stage]) for stage in ('before','after')}
        before, after = (scores[key][stage]['overall'] for stage in ('before','after'))
        expected = 37 if condition in ('informative','already-supported') else 25
        checks[key+':expected_quality'] = (after['correct'] == after['decided'] == expected and not after['wrong']
            and before['correct'] == before['decided'] == (37 if condition == 'already-supported' else 25))
        checks[key+':expected_budget'] = row['after']['budget_spent'] == int(condition in ('informative','informative-frozen','noninformative'))
        checks[key+':expected_classes'] = len(row['after']['analysis']['survivors']) == (1 if condition in ('informative','informative-frozen','already-supported') else 2)
    for permutation in permutations:
        for condition in binding.POLICIES:
            a,b = [results[f'{permutation}:{condition}:{mode}'] for mode in binding.MODES]
            checks[f'{permutation}:{condition}:memory_parity'] = all(science(a[s]) == science(b[s]) for s in ('before','after')) and all(a[s+'_predictions'] == b[s+'_predictions'] for s in ('before','after'))
        for mode in binding.MODES:
            learned,frozen_row = [results[f'{permutation}:{c}:{mode}'] for c in ('informative','informative-frozen')]
            checks[f'{permutation}:{mode}:causal_twelve_decisions'] = sum(a['decision'] != b['decision'] for a,b in zip(learned['after_predictions'],frozen_row['after_predictions'])) == 12
            checks[f'{permutation}:{mode}:same_acquired_evidence'] = learned['after']['evidence'] == frozen_row['after']['evidence']
    # Compare the three symmetry pairs sharing exactly the same ambiguous history.
    for a,b in ((0,5),(1,3),(2,4)):
        if a not in permutations or b not in permutations: continue
        for condition in binding.POLICIES:
            if condition == 'already-supported': continue
            for mode in binding.MODES:
                left,right = [results[f'{p}:{condition}:{mode}'] for p in (a,b)]
                checks[f'{a}-{b}:{condition}:{mode}:indistinguishable'] = left['before'] == right['before'] and left['before_predictions'] == right['before_predictions']
    preservation.verify_current(context, ROOT)
    summary = {'checks_passed': sum(checks.values()), 'checks_total': len(checks), 'checks': checks,
               'arms': len(results), 'runtime_processes': sum(len(r['process_ids']) for r in results.values()),
               'frozen_predictions_sha256': frozen_hash, 'source_files': len(context['files']), 'scores': scores}
    atomic_json(output/'private/arm-index.json', index)
    atomic_json(output/'results.json', summary)
    atomic_json(output/'artifact-hashes.json', {p.relative_to(output).as_posix(): preservation.file_hash(p) for p in output.rglob('*') if p.is_file()})
    print(json.dumps({k:v for k,v in summary.items() if k not in ('checks','scores')}))
    if not all(checks.values()): raise AssertionError('integration checks failed; original retained')
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True); parser.add_argument('--preservation-context', required=True)
    parser.add_argument('--permutation', type=int, choices=range(6))
    args = parser.parse_args()
    return run(Path(args.output).resolve(), args.preservation_context,
               range(6) if args.permutation is None else [args.permutation])


if __name__ == '__main__': main()
