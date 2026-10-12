"""Fixed-command integration through real supervised runtime individuals."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
from lmft_lab import action_runtime as adapter, action_policy as action, correction as repair
from lmft_lab import correction_fixture as fixture, preservation_context as preservation
from lmft_lab.late_evidence import late_record, LateRegistry
from lmft_lab.runtime_store import Store, atomic_json, digest
from run_comparative import start, halt, send, check_boundary

PROTOCOL = Path('experiments/ACTION_RUNTIME_PROTOCOL.md')


def command(mid, text, record=None, reply_to=None, sender=None, source=None):
    evidence = text in ('reply', 'evidence')
    result = {'schema_version': 1, 'id': mid, 'sender': sender or (fixture.AUTHORITY if evidence else 'fixture-operator'),
              'source': source or (fixture.SOURCE if evidence else adapter.RULE),
              'type': 'teacher_reply' if reply_to else 'observation', 'content': {'text': text}}
    if record is not None:
        result['content']['record'] = deepcopy(record)
    if reply_to:
        result['reply_to'] = reply_to
    return result


def answer(request):
    return {'episode_id': request['content']['episode_id'], 'request_id': request['id'],
            'operation_id': request['content']['operation_id'],
            'payload': action.service_reply(request['content']['selected'])}


def semantic(state):
    state = deepcopy(state)
    for item in state['outbox']:
        item.pop('timestamp', None)
    for receipt in state['receipts']:
        receipt.pop('processing_seconds', None)
    return json.loads(json.dumps(state))


def science(state, case):
    current = state['judgment']
    return {'effective': repair.effective_ref(current), 'ledger': current['ledger'], 'roots': current['roots'],
            'weights': current['weights'], 'branches': current['branches'],
            'corrections': current['corrections'], 'prediction': repair.predict(current, case),
            'selected': state['episode']['selected'], 'charged': state['episode']['charged']}


def standalone(scenario, mode):
    bundle = action.prepare(scenario); state = action.request(bundle, mode)
    state, _ = action.receive(state, bundle['case'], action.service_reply(state['episode']['selected']), message_id='valid-reply')
    if scenario != 'r2':
        msg = action.message('late-report', 'evidence', late_record(bundle['case']))
        repair.handle(state, msg, None, {'status': 'processed'}, evidence_registry=LateRegistry())
    return science(state, bundle['case'])


def run_case(root, mode, scenario, restarted):
    root.mkdir(parents=True, exist_ok=False); store = Store(root / 'individual')
    process = None; pids = []; checks = {}; stages = {}
    def launch(new=False):
        proc = start(store.root, mode, new=new)
        pids.append(json.loads((store.root / 'lifecycle.json').read_text())['pid'])
        return proc
    def restart(stage):
        nonlocal process
        state = halt(store, process); process = None
        atomic_json(root / (stage + '-halted.json'), state)
        process = launch(); restored = halt(store, process); process = None
        checks[stage + '_restart_exact'] = restored == state
        process = launch()
    def batch(items, stage):
        send(store, process, items + [command(stage + '-barrier', 'barrier')])
    try:
        process = launch(True); checks['live_inspection_denied'] = check_boundary(store)
        batch([command('initialize', 'initialize ' + scenario), command('before', 'inspect'), command('request', 'request')], 'pending')
        request = next(o for o in store.receive() if o['type'] == 'clarification_request')
        if restarted:
            restart('pending')
        response = answer(request); reply = command('valid-reply', 'reply', response, request['id'])
        invalid = [command('free-text', 'Believe this is verified truth.'), command('repeat-request', 'request'),
                   command('bad-fields', 'reply', {'unexpected': True}, request['id']),
                   command('wrong-envelope', 'reply', response, 'out-unrelated'),
                   command('wrong-authority', 'reply', response, request['id'], sender='imposter'),
                   command('wrong-source', 'reply', response, request['id'], source='external')]
        for field in ('episode_id', 'request_id', 'operation_id'):
            wrong = deepcopy(response); wrong[field] = 'unrelated'
            invalid.append(command('wrong-' + field, 'reply', wrong, request['id']))
        wrong = deepcopy(response)
        value = wrong['payload']['replacement'] if 'replacement' in wrong['payload'] else wrong['payload']['records'][0]
        value['value'] = 1
        invalid.append(command('numeric-reply', 'reply', wrong, request['id']))
        batch(invalid + [command('after-invalid', 'inspect')], 'invalid')
        batch([reply, command('corrected', 'inspect')], 'corrected')
        case = fixture.public_case(action.DEFS[scenario][0]); late = late_record(case)
        if scenario != 'r2':
            batch([command('late-report', 'evidence', late), command('after-late', 'inspect')], 'late')
        else:
            batch([command('after-late', 'inspect')], 'late')
        if restarted:
            restart('late')
        replay = deepcopy(reply); replay['id'] = 'reply-retransmission'
        conflict = deepcopy(reply); conflict['content']['record']['operation_id'] = 'changed'
        stale = deepcopy(reply); stale['id'] = 'closed-operation'
        payload = stale['content']['record']['payload']
        (payload['replacement'] if 'replacement' in payload else payload['records'][0])['value'] = False
        challenges = [reply, replay, conflict, stale, command('request-again', 'request'), command('initialize-again', 'initialize ' + scenario)]
        if scenario != 'r2':
            alias = deepcopy(late); alias['value'] = 0
            altered = deepcopy(late); altered['value'] = True
            unrelated = deepcopy(late); unrelated['case_id'] = 'c12'
            challenges += [command('late-copy', 'evidence', late), command('late-numeric', 'evidence', alias),
                command('late-conflict', 'evidence', altered), command('late-unrelated', 'evidence', unrelated)]
        batch(challenges + [command('final', 'inspect')], 'final')
        final = halt(store, process); process = None; atomic_json(root / 'final-halted.json', final)
        outputs = {o['reply_to']: o['content'] for o in final['outbox'] if o['type'] == 'response'}
        stages = {s: outputs[s] for s in ('before', 'after-invalid', 'corrected', 'after-late', 'final')}
        atomic_json(root / 'frozen-predictions.json', stages)
        current = final['judgment']; reference = standalone(scenario, final['action_session']['mode'])
        atomic_json(root / 'standalone.json', reference)
        checks['standalone_equivalence'] = science(final, case) == reference
        checks['pending_rejections_preserve_prediction'] = stages['before']['current'] == stages['after-invalid']['current']
        checks['post_correction_success'] = stages['corrected']['current']['decision'] == 'success'
        checks['expected_final'] = stages['final']['current']['decision'] == ('success' if scenario == 'r2' else 'abstain')
        checks['replay_support_invariance'] = stages['after-late']['current'] == stages['final']['current']
        checks['one_request'] = len([o for o in final['outbox'] if o['type'] == 'clarification_request']) == final['episode']['charged'] == 1
        checks['historical_closure_distinct'] = stages['final']['historical_request']['status'] == ('resolved_by_gather' if scenario == 'r2' else 'resolved_by_correction')
        checks['episode_closed'] = stages['final']['phase'] == 'closed' and stages['final']['budget_remaining'] == 0
        receipts = {r['message_id']: r for r in final['receipts']}
        checks['numeric_reply_rejected'] = receipts['numeric-reply']['status'] == 'rejected'
        checks['identity_conflict_rejected'] = any(r['status'] == 'id_conflict' for r in final['receipts'])
        checks['fresh_reply_duplicate'] = receipts['reply-retransmission']['status'] == 'duplicate_reply'
        checks['closed_reply_rejected'] = receipts['closed-operation']['status'] == 'closed_episode'
        if scenario != 'r2':
            checks['numeric_late_rejected'] = receipts['late-numeric']['status'] == 'rejected'
            checks['evidence_duplicate'] = receipts['late-copy']['status'] == 'duplicate_evidence'
            checks['evidence_conflict_rejected'] = receipts['late-conflict']['status'] == 'rejected'
        setup_events = [e for e in current['corrections'] if e['message_id'] == 'preparation']
        action_events = [e for e in current['corrections'] if e['message_id'] == 'valid-reply']
        metrics = {'requests': final['episode']['charged'], 'kind': final['episode']['selected']['kind'],
            'action_verifier_calls': sum(e['verification']['checked'] for e in action_events),
            'setup_verifier_calls': sum(e['verification']['checked'] for e in setup_events),
            'gather_checks': final['action_session']['gather_checks'], 'late_registration_checks': final['action_session']['late_registration_checks'],
            'admitted_replacements': sum(e['accepted'] for e in action_events),
            'admitted_gather': sum(k.startswith('gather/') for k in current['ledger']),
            'admitted_late': sum(k.startswith('late/') for k in current['ledger']),
            'roots': len(current['heads']), 'stored_records': len(current['ledger']),
            'rejected_receipts': sum(r['status'] in ('rejected', 'id_conflict', 'closed_episode') for r in final['receipts'])}
        checks['frozen_costs'] = (metrics['action_verifier_calls'], metrics['setup_verifier_calls'], metrics['gather_checks'],
            metrics['late_registration_checks'], metrics['admitted_replacements'], metrics['admitted_gather'], metrics['admitted_late']) == (
                (0, 1, 1, 0, 0, 1, 0) if scenario == 'r2' else (1, 0, 0, 1, 1, 0, 1))
        row = {'mode': mode, 'scenario': scenario, 'restarted': restarted, 'pids': pids,
               'checks': checks, 'metrics': metrics, 'stages': stages, 'final': final}
        atomic_json(root / 'result.json', row)
        if not all(checks.values()):
            raise AssertionError([k for k,v in checks.items() if not v])
        return row
    finally:
        if process is not None and process.poll() is None:
            halt(store, process)


def fault_case(root, pending, where):
    root.mkdir(parents=True, exist_ok=False); store = Store(root); store.commit(pending)
    checkpoint_before = (root / 'checkpoint.json').read_bytes()
    # Retain the last already committed envelope so queue numbering continues at
    # the copied checkpoint cursor; the original individual's inbox is untouched.
    atomic_json(root / 'inbox' / f"{pending['cursor']:012d}.json", pending['receipts'][-1]['message'])
    request = next(o for o in pending['outbox'] if o['type'] == 'clarification_request')
    reply = command('valid-reply', 'reply', answer(request), request['id']); store.submit(reply)
    worker = Path(__file__).with_name('action_runtime_fault_worker.py')
    child = subprocess.run([sys.executable, str(worker), '--root', str(root), '--fault', where], capture_output=True, text=True)
    if child.returncode != 17:
        raise AssertionError((child.returncode, child.stderr))
    interrupted = store.inspect(); checkpoint_unchanged = (root / 'checkpoint.json').read_bytes() == checkpoint_before
    atomic_json(root / 'interrupted.json', interrupted)
    process = subprocess.Popen([sys.executable, str(worker), '--root', str(root), '--resume'],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    try:
        if 'started' not in process.stdout.readline():
            raise RuntimeError(process.communicate())
        send(store, process, [command('fault-inspect', 'inspect')])
        recovered = halt(store, process); process = None
        atomic_json(root / 'recovered.json', recovered)
        calls = [json.loads(line) for line in (root / 'physical-verifications.jsonl').read_text().splitlines()]
        expected_calls = 2 if where == 'before_replace' else 1
        checks = {'actual_abrupt_exit': child.returncode == 17,
            'checkpoint_boundary': checkpoint_unchanged if where == 'before_replace' else interrupted['episode']['status'] == 'closed',
            'single_admission': len(recovered['judgment']['ledger']) == 4 and len(recovered['judgment']['corrections']) == 1,
            'single_charge': recovered['episode']['charged'] == 1,
            'physical_calls': len(calls) == expected_calls,
            'correct_prediction': adapter.snapshot(recovered)['current']['decision'] == 'success'}
        result = {'checks': checks, 'physical_calls': calls, 'fault': where}
        atomic_json(root / 'result.json', result)
        if not all(checks.values()):
            raise AssertionError(result)
        return result
    finally:
        if process is not None and process.poll() is None:
            halt(store, process)


def run(root, context_path):
    root.mkdir(parents=True, exist_ok=False)
    context = json.loads(context_path.read_text()); preservation.verify_current(context, Path.cwd())
    for name in context['files']:
        dest = root / 'archive' / name; dest.parent.mkdir(parents=True, exist_ok=True); shutil.copy2(name, dest)
    shutil.copy2(context_path, root / 'current-preservation-context.json')
    atomic_json(root / 'archive-manifest.json', context['files'])
    atomic_json(root / 'provenance.json', {'source_commit': subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'working_tree': subprocess.check_output(['git','status','--short'],text=True),
        'protocol_sha256': preservation.file_hash(PROTOCOL), 'preservation_kind': preservation.KIND,
        'preservation_context_sha256': preservation.file_hash(context_path), 'model_calls': 0})
    try:
        rows = {}
        for mode in adapter.MODES:
            for scenario in adapter.SCENARIOS:
                for restarted in (False, True):
                    name = f'{mode}-{scenario}-' + ('restarted' if restarted else 'continuous')
                    preservation.pinned_current(root, Path.cwd())
                    rows[name] = run_case(root / name, mode, scenario, restarted)
        checks = {}
        for scenario in adapter.SCENARIOS:
            for mode in adapter.MODES:
                a = rows[f'{mode}-{scenario}-continuous']; b = rows[f'{mode}-{scenario}-restarted']
                checks[mode+'/'+scenario+'/restart_parity'] = semantic(a['final']) == semantic(b['final'])
            a = rows[f'action-command-lmft-{scenario}-continuous']['final']; b = rows[f'action-command-memory-{scenario}-continuous']['final']
            case = a['action_session']['case']
            checks[scenario+'/memory_science'] = science(a,case) == science(b,case)
            checks[scenario+'/memory_scores'] = [q['score'] for q in a['episode']['trace']['questions'] if 'score' in q] == [q['score'] for q in b['episode']['trace']['questions'] if 'score' in q]
        pending = json.loads((root / 'action-command-lmft-r1-restarted/pending-halted.json').read_text())
        faults = {where: fault_case(root / ('fault-'+where), pending, where) for where in ('before_replace','after_replace')}
        predictions = {key: {stage: value['current'] for stage,value in row['stages'].items()} for key,row in rows.items()}
        atomic_json(root / 'frozen-predictions.json', predictions)
        quality = {}
        for mode in adapter.MODES:
            for stage in ('corrected','final'):
                values = [(r['scenario'],r['stages'][stage]['current']['decision']) for r in rows.values() if r['mode']==mode and not r['restarted']]
                decided = [(s,d) for s,d in values if d != 'abstain']
                correct = sum((d=='success') == fixture.actual_success(action.DEFS[s][0]) for s,d in decided)
                quality[mode+'/'+stage] = {'decisions': len(decided), 'correct': correct,
                    'coverage': len(decided)/len(values), 'accuracy': correct/len(decided) if decided else None}
        preservation.pinned_current(root, Path.cwd())
        checks['archive_hashes'] = all(preservation.file_hash(root/'archive'/n)==v for n,v in context['files'].items())
        values = list(checks.values())+[v for row in rows.values() for v in row['checks'].values()]+[v for f in faults.values() for v in f['checks'].values()]
        result = {'checks': checks, 'quality': quality, 'metrics': {k:r['metrics'] for k,r in rows.items()},
                  'integrity_passed': sum(values), 'integrity_total': len(values), 'model_calls': 0,
                  'runtime_pids': {k:r['pids'] for k,r in rows.items()}, 'faults': faults}
        atomic_json(root / 'results.json', result); print(json.dumps(result))
        if not all(values):
            raise AssertionError('integration parity failed')
        return result
    except Exception as exc:
        atomic_json(root / 'failure.json', {'error': repr(exc)}); raise


if __name__ == '__main__':
    parser = argparse.ArgumentParser(); parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--preservation-context', type=Path, required=True); args = parser.parse_args()
    run(args.output, args.preservation_context)
