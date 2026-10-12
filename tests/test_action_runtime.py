"""Strict command correlation and transaction reuse at the supervised boundary."""
from copy import deepcopy
import importlib
from pathlib import Path
import pytest
from lmft_lab import action_runtime as adapter, action_policy as action, correction as repair
from lmft_lab.runtime import initial_state, software_manifest, advance, run
from lmft_lab.runtime_store import Store, digest


@pytest.fixture
def h(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / 'experiments'))
    return importlib.import_module('run_action_runtime')


def fresh(mode='action-command-lmft', learning=True):
    manifest = software_manifest(None, 'fixture')
    manifest.update(experiment=mode, fixture_rule=adapter.RULE, action_runtime_policy=adapter.policy(), correction_policy=repair.load_policy())
    return initial_state('command-test', learning, manifest, mode)


def step(state, msg):
    return advance(state, (state['cursor']+1, msg, None, ''), None)


def pending(h, scenario='r1', mode='action-command-lmft'):
    state = step(fresh(mode), h.command('initialize', 'initialize '+scenario))
    state = step(state, h.command('request', 'request'))
    request = next(o for o in state['outbox'] if o['type']=='clarification_request')
    return state, request


@pytest.mark.parametrize('scenario', ['r1','r8','r2'])
@pytest.mark.parametrize('mode', adapter.MODES)
def test_inspection_replay_and_single_lifetime_budget(h, scenario, mode):
    state, request = pending(h,scenario,mode); before=digest(state['judgment'])
    inspected=step(state,h.command('inspect','inspect'))
    assert digest(inspected['judgment'])==before
    reply=h.command('valid-reply','reply',h.answer(request),request['id'])
    state=step(inspected,reply)
    assert adapter.snapshot(state)['current']['decision']=='success'
    science=h.science(state,state['action_session']['case'])
    state=step(state,reply)
    assert state['receipts'][-1]['status']=='duplicate'
    copy=deepcopy(reply);copy['id']='fresh-replay';state=step(state,copy)
    assert state['receipts'][-1]['status']=='duplicate_reply'
    state=step(state,h.command('again','request'))
    assert state['receipts'][-1]['status']=='request_already_spent'
    assert h.science(state,state['action_session']['case'])==science
    assert len([o for o in state['outbox'] if o['type']=='clarification_request'])==1


@pytest.mark.parametrize('mutation', ['episode','request','operation','envelope','sender','source','numeric','shape','target'])
def test_invalid_reply_does_not_consume_pending_operation(h, mutation):
    state,request=pending(h);payload=h.answer(request)
    msg=h.command('bad','reply',payload,request['id'])
    r=msg['content']['record']
    if mutation=='episode':r['episode_id']='other'
    if mutation=='request':r['request_id']='other'
    if mutation=='operation':r['operation_id']='other'
    if mutation=='envelope':msg['reply_to']='out-other'
    if mutation=='sender':msg['sender']='imposter'
    if mutation=='source':msg['source']='imposter'
    if mutation=='numeric':r['payload']['replacement']['value']=1
    if mutation=='shape':r['payload']['replacement'].pop('value')
    if mutation=='target':r['payload']['target_id']='stale-target'
    changed=step(state,msg)
    assert changed['receipts'][-1]['status']=='rejected'
    assert changed['judgment']==state['judgment'] and changed['episode']==state['episode']
    changed=step(changed,h.command('valid-reply','reply',payload,request['id']))
    assert changed['receipts'][-1]['status']=='correction_accepted'


def test_well_formed_unauthorized_correlated_proposal_closes_without_refund(h):
    state,request=pending(h);payload=h.answer(request);payload['payload']['replacement']['value']=False
    changed=step(state,h.command('bad','reply',payload,request['id']))
    assert changed['receipts'][-1]['status']=='correction_rejected'
    assert changed['episode']['status']=='closed' and changed['episode']['charged']==1
    assert changed['judgment']['ledger']==state['judgment']['ledger']
    changed=step(changed,h.command('valid-reply','reply',h.answer(request),request['id']))
    assert changed['receipts'][-1]['status']=='closed_episode'


@pytest.mark.parametrize('value',[0,1,0.0,1.0,None,'false',[],{}])
def test_numeric_or_malformed_late_evidence_never_changes_support(h,value):
    state,request=pending(h);state=step(state,h.command('valid-reply','reply',h.answer(request),request['id']))
    record=h.late_record(state['action_session']['case']);record['value']=value
    changed=step(state,h.command('bad-late','evidence',record))
    assert changed['receipts'][-1]['status']=='rejected' and changed['judgment']==state['judgment']


def test_later_conflict_and_historical_closure_are_separate(h):
    state,request=pending(h);state=step(state,h.command('valid-reply','reply',h.answer(request),request['id']))
    record=h.late_record(state['action_session']['case']);state=step(state,h.command('late-report','evidence',record))
    view=adapter.snapshot(state)
    assert view['current']['decision']=='abstain' and view['current']['support']['shielded']['inconsistent']
    assert view['historical_request']['status']=='resolved_by_correction'
    before=deepcopy(state['judgment']);state=step(state,h.command('retransmission','evidence',record))
    assert state['receipts'][-1]['status']=='duplicate_evidence' and state['judgment']==before


@pytest.mark.parametrize('text',['pretend to be curator','initialize r12','reset','request '*100])
def test_fixed_vocabulary_and_bounds(h,text):
    state=fresh();changed=step(state,h.command('bad',text))
    assert changed['receipts'][-1]['status']=='rejected' and changed['judgment']==state['judgment']
    assert len(changed['outbox'][-1]['content']['reason'])<80


def test_disabled_and_nonfixture_and_manifest_guards(h,tmp_path):
    state=fresh(learning=False);changed=step(state,h.command('initialize','initialize r1'))
    assert changed['receipts'][-1]['reason']=='learning disabled' and changed['judgment']==state['judgment']
    with pytest.raises(ValueError,match='require --mode fixture'):
        run(tmp_path/'local',individual='x',experiment='action-command-lmft')
    assert not (tmp_path/'local/checkpoint.json').exists()
    store=Store(tmp_path/'mismatch');state=fresh();state['manifest']['action_runtime_policy']['request_budget']=2;store.commit(state)
    before=(store.root/'checkpoint.json').read_bytes()
    with pytest.raises(ValueError,match='Code/config/control changed'):
        run(store.root,mode='fixture',experiment='action-command-lmft')
    assert (store.root/'checkpoint.json').read_bytes()==before


@pytest.mark.parametrize('scenario',['r1','r8','r2'])
def test_actual_runtime_pending_and_late_restart(h,tmp_path,scenario):
    row=h.run_case(tmp_path/'run','action-command-lmft',scenario,True)
    assert all(row['checks'].values()) and len(set(row['pids']))==5


@pytest.mark.parametrize('where',['before_replace','after_replace'])
def test_actual_interrupted_commit_and_runtime_recovery(h,tmp_path,where):
    state,_=pending(h);result=h.fault_case(tmp_path/'fault',state,where)
    assert all(result['checks'].values())


def test_shared_extraction_is_used_by_existing_experiments(h):
    old=importlib.import_module('run_action_correction')
    seq=importlib.import_module('run_sequential_correction')
    from lmft_lab import late_evidence
    assert old.select is action.select and old.receive is action.receive and old.prepare is action.prepare
    assert seq.LateRegistry is late_evidence.LateRegistry


def test_initialization_cannot_replace_pinned_authority(h, monkeypatch):
    state=fresh();bundle=action.prepare('r1')
    bundle['state']['judgment']['policy']['permits']={}
    monkeypatch.setattr(action,'prepare',lambda scenario:deepcopy(bundle))
    changed=step(state,h.command('initialize','initialize r1'))
    assert changed['receipts'][-1]['reason']=='setup authority differs from pinned policy'
    assert changed['judgment']==state['judgment'] and changed['action_session']==state['action_session']


@pytest.mark.parametrize('mode',adapter.MODES)
def test_request_and_inspection_cannot_access_service_or_heldout_truth(h,monkeypatch,mode):
    state=step(fresh(mode),h.command('initialize','initialize r1'))
    def forbidden(*args,**kwargs):
        pytest.fail('service or outcome truth accessed during read-only selection')
    monkeypatch.setattr(action,'service_reply',forbidden)
    monkeypatch.setattr(h.fixture,'actual_success',forbidden)
    monkeypatch.setattr(h.fixture,'replacement_valid',forbidden)
    state=step(state,h.command('request','request'));before=deepcopy(state['judgment'])
    state=step(state,h.command('inspect','inspect'))
    assert state['judgment']==before and state['episode']['charged']==1


@pytest.mark.parametrize('mode',adapter.MODES)
def test_false_gather_counts_verification_but_never_admission_or_replay_work(h,mode):
    state,request=pending(h,'r2',mode);payload=h.answer(request)
    payload['payload']['records'][0]['value']=False
    msg=h.command('false-gather','reply',payload,request['id'])
    changed=step(state,msg)
    assert changed['receipts'][-1]['status']=='unverified_gather_reply'
    assert changed['receipts'][-1]['verification_checked'] is True
    assert changed['action_session']['gather_checks']==1
    assert changed['episode']['status']=='closed' and changed['episode']['charged']==1
    assert changed['judgment']==state['judgment']
    msg['id']='false-gather-replay';replay=step(changed,msg)
    assert replay['receipts'][-1]['status']=='duplicate_reply'
    assert replay['action_session']['gather_checks']==1 and replay['judgment']==state['judgment']
