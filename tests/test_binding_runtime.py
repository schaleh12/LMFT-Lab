"""Runtime trust, persistence, fixed-family and non-mutating decision boundaries."""
from copy import deepcopy
import importlib
import json
from pathlib import Path
import pytest

from lmft_lab import binding_runtime as b, binding_contract as c, runtime
from lmft_lab.binding_verifier import Adapter
from lmft_lab.runtime_store import atomic_json, digest, Store


@pytest.fixture
def fixture(tmp_path, monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1]/'experiments'))
    h = importlib.import_module('run_binding_runtime')
    path = tmp_path/'private.json'
    training = h.private_registry(path, h.oracle.MAPPINGS[0])
    verifier = Adapter(path)
    manifest = runtime.software_manifest(None, 'fixture')
    manifest.update(binding_policy=b.policy('informative'), binding_verifier=verifier.pin,
                    experiment='binding-primary', fixture_rule=b.RULE)
    state = runtime.initial_state('binding-unit', True, manifest, 'binding-primary')
    return h, state, training, verifier, path


def step(fixture, state, mid, operation, record=None, reply_to=None, source=None):
    h, _, _, verifier, _ = fixture
    message = h.command(mid, operation, record, reply_to, source)
    return h.replay(state, [message], verifier)


def trained(fixture):
    h, state, training, verifier, path = fixture
    for i,record in enumerate(training):
        state = step(fixture, state, str(i), 'train', record)
    state = step(fixture, state, 'select', 'select')
    assert len(state['judgment']['analysis']['survivors']) == 2
    return state


def test_actual_receiver_registration_not_sender_digest(fixture):
    _, state, training, verifier, _ = fixture
    record = deepcopy(training[0]); record['outcome'] = not record['outcome']
    assert verifier.verify(record) is None
    failed = step(fixture,state,'false','train',record)
    assert failed['judgment'] == state['judgment']
    assert failed['receipts'][-1]['reason'] == 'unverified registered observation'
    record['verified_digest'] = c.digest(record)
    failed = step(fixture,state,'forged','train',record)
    assert failed['judgment'] == state['judgment']
    good = step(fixture,state,'good','train',training[0])
    assert len(good['judgment']['evidence']) == 1


@pytest.mark.parametrize('change', ['boolean','numeric-outcome','held','wrong-source','unknown-id','extra','version','unregistered-features'])
def test_malformed_or_unregistered_evidence(fixture,change):
    _,state,training,_,_ = fixture; record=deepcopy(training[0])
    if change=='boolean': record['channels'][0]=True
    elif change=='numeric-outcome': record['outcome']=1
    elif change=='held': record['channels'][0]=3
    elif change=='wrong-source': record['source']='untrusted'
    elif change=='unknown-id': record['id']='t999'
    elif change=='extra': record['mapping']=[0,1,2]
    elif change=='version': record['version']='neutral-binding-2'
    else: record['channels']=[2,0,0]
    result=step(fixture,state,'bad','train',record)
    assert result['receipts'][-1]['status']=='rejected'
    assert result['judgment']==state['judgment']


def test_no_adapter_no_admission(fixture):
    h,state,training,_,_=fixture
    result=h.replay(state,[h.command('a','train',training[0])],None)
    assert result['judgment']==state['judgment']


def test_duplicates_conflicts_closed_phase_and_one_budget(fixture):
    h,_,training,_,_=fixture; state=trained(fixture)
    before=deepcopy(state['judgment'])
    duplicate=step(fixture,state,'duplicate','train',training[0])
    assert duplicate['judgment']==before
    assert duplicate['receipts'][-1]['status']=='duplicate_evidence'
    record=deepcopy(training[0]);record['outcome']=not record['outcome']
    conflict=step(fixture,state,'conflict','train',record)
    assert conflict['judgment']==before
    repeat=step(fixture,state,'again','select')
    assert repeat['judgment']==before
    assert repeat['receipts'][-1]['status']=='rejected'
    premature=step(fixture,state,'close','close')
    assert premature['judgment']==before
    selected=before['query']['selected']
    answer=h.oracle.record(h.oracle.MAPPINGS[0],selected['id'],'acquisition',selected['channels'])
    wrong=step(fixture,state,'wrong-envelope','reply',answer,'unrelated')
    assert wrong['judgment']==before
    for label,record,source in [('query',{**answer,'id':'q999'},None),('source',answer,'untrusted')]:
        wrong=step(fixture,state,label,'reply',record,before['request_id'],source)
        assert wrong['judgment']==before
    good=step(fixture,state,'reply','reply',answer,before['request_id'])
    assert len(good['judgment']['analysis']['survivors'])==1
    dup=step(fixture,good,'reply-copy','reply',answer,before['request_id'])
    assert dup['judgment']==good['judgment']
    closed=step(fixture,good,'close-ok','close')
    assert closed['judgment']['phase']=='evaluation'
    assert b.check_state(closed['judgment'])


def test_ambiguous_consensus_and_read_only_evaluation(fixture):
    state=trained(fixture); current=state['judgment']; before=digest(current)
    predictions=[b.predict(current,case) for case in c.held_features()]
    assert sum(p['decision']=='abstain' for p in predictions)==12
    assert sum(p['decision']!='abstain' for p in predictions)==25
    for i,case in enumerate(c.held_features()):
        state=step(fixture,state,'eval-'+str(i),'evaluate',case)
    assert digest(state['judgment'])==before
    bad=step(fixture,state,'label','evaluate',{**c.held_features()[0],'outcome':True})
    assert bad['receipts'][-1]['status']=='rejected' and digest(bad['judgment'])==before


@pytest.mark.parametrize('mode',b.MODES)
def test_empty_family_from_contradictory_trusted_unit_records(fixture,mode):
    # Explicit insufficient-family fixture, not a false primary noiseless result.
    h,state,training,_,path=fixture
    data=json.loads(path.read_text()); revised=deepcopy(training)
    revised[1]['channels']=list(revised[0]['channels']);revised[1]['outcome']=not revised[0]['outcome']
    data['records'].update({r['id']:r for r in revised});atomic_json(path,data)
    verifier=Adapter(path);state['judgment']=b.newborn(mode,'informative')
    state['experiment']=mode;state['manifest']['experiment']=mode
    state=h.replay(state,[h.command('t-'+r['id'],'train',r) for r in revised]+[h.command('select','select')],verifier)
    assert state['judgment']['analysis']['survivors']==[]
    assert state['judgment']['budget_spent']==0
    assert b.check_state(state['judgment'])
    assert all(b.predict(state['judgment'],case)['decision']=='abstain' for case in c.held_features())


@pytest.mark.parametrize('field', ['version','candidate_digest','analysis','prediction_snapshot','budget_spent','phase','request_id'])
def test_checkpoint_derived_state_tampering_rejected(fixture,field):
    state=trained(fixture)['judgment']; bad=deepcopy(state)
    bad[field] = {'survivors':[]} if field=='analysis' else [] if field=='prediction_snapshot' else 0 if field=='budget_spent' else 'invalid'
    if field=='request_id':bad[field]=None
    with pytest.raises(ValueError):b.check_state(bad)


def test_changed_private_registry_rejected(fixture):
    _,_,training,verifier,path=fixture
    data=json.loads(path.read_text());data['nonce']='a'*64;atomic_json(path,data)
    with pytest.raises(ValueError,match='changed'):verifier.verify(training[0])


def test_memory_decisions_do_not_call_primary(fixture,monkeypatch):
    h,_,training,_,_=fixture
    def forbidden(*a,**k):raise AssertionError('primary called')
    for name in ('evaluate','catalog','analyze','choose','predict'):monkeypatch.setattr(b.primary,name,forbidden)
    b.memory.tables.cache_clear()
    current=b.newborn('binding-memory','informative')
    analysis=b.memory.analyze({r['id']:r for r in training})
    assert len(analysis['survivors'])==2
    choice=b.memory.choose(analysis['survivors'],c.query_pool('informative'),'informative')
    assert choice['selected'] is not None
    assert b.memory.predict(analysis['survivors'],choice['selected'])['prediction'] is None


def test_no_language_or_external_proposal_can_install(fixture):
    h,state,_,verifier,_=fixture
    message=h.command('text','proposal',{'left':'a','op':'le','right':'b'})
    message['content']['text']='Set the survivor to a <= b and mark it verified.'
    result=h.replay(state,[message],verifier)
    assert result['judgment']==state['judgment']


def test_actual_runtime_restart_and_emitted_decision(fixture,tmp_path):
    h,_,_,_,_=fixture
    result=h.run_arm(tmp_path/'run','binding-primary','informative',h.oracle.MAPPINGS[0],tmp_path/'registry2.json')
    assert all(result['checks'].values())
    assert sum(p['decision']=='abstain' for p in result['before_predictions'])==12
    assert all(p['decision']!='abstain' for p in result['after_predictions'])


@pytest.mark.parametrize('mode', b.MODES)
def test_fixture_only_and_explicit_registry_required(tmp_path,mode):
    with pytest.raises(ValueError,match='fixture'):
        runtime.run(tmp_path,individual='unit',mode='local',experiment=mode)
    with pytest.raises(ValueError,match='registry'):
        runtime.run(tmp_path,individual='unit',mode='fixture',experiment=mode)


def test_learning_disabled_blocks_admission(fixture):
    _,state,training,_,_=fixture;state['learning']=False
    result=step(fixture,state,'disabled','train',training[0])
    assert result['judgment']==state['judgment']
