"""Scientific and actual-boundary checks for the isolated neutral binding study."""
from copy import deepcopy
import importlib
import json
from pathlib import Path
import subprocess
import sys
import pytest


@pytest.fixture
def modules(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1]/'experiments'))
    names = ('contract','primary','memory','engine','oracle')
    return {name: importlib.import_module('attribute_binding_'+name) for name in names} | {
        'harness': importlib.import_module('run_attribute_binding')}


def trained(m, implementation='primary', policy='informative', permutation=0):
    request = {'stage':'training','implementation':implementation,'policy':policy,
               'items':m['harness'].training_items(m['oracle'].MAPPINGS[permutation], policy=='already-supported')}
    state, predictions = m['engine'].transition(request)
    return state, predictions, request


def test_equivalence_classes_have_auditable_reverse_pairs(modules):
    p, memory, c = (modules[n] for n in ('primary','memory','contract'))
    assert len(c.representations()) == 36
    assert len(p.catalog()) == 18 and all(len(row['members']) == 2 for row in p.catalog().values())
    assert p.catalog() == memory.catalog()
    for entry in p.catalog().values():
        assert all([p.evaluate(rep,point) for point in c.DOMAIN] == entry['truth_vector'] for rep in entry['members'])


def test_memory_does_not_call_primary_decision_functions(modules,monkeypatch):
    primary, memory, oracle = (modules[n] for n in ('primary','memory','oracle'))
    def forbidden(*args,**kwargs):raise AssertionError('primary implementation called')
    for name in ('evaluate','catalog','analyze','choose','predict'):monkeypatch.setattr(primary,name,forbidden)
    memory.tables.cache_clear()
    records = {r['id']:r for r in oracle.training(oracle.MAPPINGS[0])}
    analysis = memory.analyze(records)
    assert len(analysis['survivors']) == 2
    choice = memory.choose(analysis['survivors'],modules['contract'].query_pool('informative'),'informative')
    assert choice['selected'] is not None
    assert memory.predict(analysis['survivors'],choice['selected'])['reason'] == 'ambiguous'


@pytest.mark.parametrize('permutation',range(6))
def test_primary_operand_ambiguity_not_operator_ambiguity(modules,permutation):
    state, before, _ = trained(modules,permutation=permutation)
    catalog = modules['primary'].catalog()
    assert len(state['analysis']['survivors']) == 2
    assert all({rep['op'] for rep in catalog[key]['members']} == {'le','ge'} for key in state['analysis']['survivors'])
    assert state['query']['selected'] is not None and state['budget_spent'] == 1
    scores = state['query']['scored']
    assert max(row['score'] for row in scores) == 1  # classes, not four representation votes
    selected = next(row for row in scores if row['case'] == state['query']['selected'])
    assert selected['score'] == 1
    first = next(e['record'] for e in state['evidence'].values())
    items = modules['harness'].acquisition_items(modules['oracle'].MAPPINGS[permutation],state['query']['selected'],first)
    after, predictions = modules['engine'].transition({'stage':'acquisition','implementation':'primary','policy':'informative','items':items},state)
    assert len(after['analysis']['survivors']) == 1
    assert all(type(row['prediction']) is bool for row in predictions)
    score = modules['oracle'].score(modules['oracle'].MAPPINGS[permutation],predictions)
    assert score['overall']['correct'] == score['overall']['total'] == 37
    assert score['distractor_invariant'] and score['equality']['total'] > 0
    assert score['success']['total'] > 0 and score['failure']['total'] > 0
    assert before != predictions


@pytest.mark.parametrize('policy',['no-acquisition','noninformative','unavailable','already-supported'])
def test_controls_cannot_pass_by_blanket_abstention(modules,policy):
    state, before, _ = trained(modules,policy=policy)
    expected = 1 if policy == 'already-supported' else 2
    assert len(state['analysis']['survivors']) == expected
    assert state['budget_spent'] == int(policy == 'noninformative')
    first = next(e['record'] for e in state['evidence'].values())
    items = modules['harness'].acquisition_items(modules['oracle'].MAPPINGS[0],state['query']['selected'],first)
    _,after = modules['engine'].transition({'stage':'acquisition','implementation':'primary','policy':policy,'items':items},state)
    assert before == after
    if policy == 'already-supported':assert all(type(row['prediction']) is bool for row in after)
    else:assert any(row['prediction'] is None for row in after) and any(type(row['prediction']) is bool for row in after)


@pytest.mark.parametrize('implementation',['primary','memory'])
def test_strict_admission_idempotence_and_empty_set(modules,implementation):
    c,e = modules['contract'],modules['engine']
    state=e.new(implementation,'informative')
    record=modules['oracle'].training(modules['oracle'].MAPPINGS[0])[0]
    for changed in ({**record,'outcome':1},{**record,'channels':[False,0,0]},
                    {**record,'source':'claimed'},{**record,'mapping':[0,1,2]}):
        assert e.admit(state,changed,None)=='rejected'
    assert e.admit(state,record,None)=='rejected'
    held={**record,'channels':[3,0,0]}
    assert e.admit(state,held,c.digest(held))=='rejected'
    assert e.admit(state,record,c.digest(record))=='accepted'
    old=deepcopy(state['analysis']);count=len(state['evidence'])
    assert e.admit(state,record,c.digest(record))=='duplicate'
    assert old==state['analysis'] and count==len(state['evidence']) and state['budget_spent']==0
    conflict={**record,'outcome':not record['outcome']}
    assert e.admit(state,conflict,c.digest(conflict))=='rejected'
    # Deliberately inconsistent TRUSTED unit fixture, not a primary oracle outcome.
    contrary={**conflict,'id':'t099'}
    assert e.admit(state,contrary,c.digest(contrary))=='accepted'
    assert state['analysis']['survivors']==[]
    assert all(p['prediction'] is None and p['reason']=='unsupported' for p in e.predictions(state))
    assert e.KERNELS[implementation].choose([],c.query_pool('informative'),'noninformative')['selected'] is None


def test_unverified_unselected_and_closed_acquisition_preserve_learning(modules):
    c,e,o=modules['contract'],modules['engine'],modules['oracle']
    state,_,_=trained(modules)
    selected=state['query']['selected'];r=o.record(o.MAPPINGS[0],selected['id'],'acquisition',selected['channels'])
    original=deepcopy(state['analysis']);evidence=deepcopy(state['evidence'])
    assert e.admit(state,r,None)=='rejected'
    other={**r,'id':'q999'}
    assert e.admit(state,other,c.digest(other))=='rejected'
    assert state['analysis']==original and state['evidence']==evidence and state['budget_spent']==1
    assert e.admit(state,r,o.verify(o.MAPPINGS[0],r))=='accepted'
    e.finish_acquisition(state)
    assert e.admit(state,other,c.digest(other))=='rejected'
    with pytest.raises(ValueError):e.select(state)
    with pytest.raises(ValueError):e.finish_acquisition(state)


def test_query_pool_and_held_features_have_no_oracle_dependency(modules,monkeypatch):
    def forbidden(*args,**kwargs):raise AssertionError('oracle accessed')
    monkeypatch.setattr(modules['oracle'],'label',forbidden)
    c=modules['contract']
    assert len(c.query_pool('informative'))==27 and len(c.held_features())==37
    assert not {tuple(r['channels']) for r in c.query_pool('informative')} & {tuple(r['channels']) for r in c.held_features()}
    for impl in ('primary','memory'):
        kernel=modules[impl]
        kernel.choose(list(kernel.catalog()),c.query_pool('informative'),'informative')
        kernel.predict(list(kernel.catalog()),c.held_features()[0])


def test_actual_worker_rejects_mapping_and_evaluation_labels(modules,tmp_path):
    state,_,request=trained(modules)
    for i,extra in enumerate(({'hidden_mapping':[0,1,2]},{'held_labels':[True]*37})):
        with pytest.raises(AssertionError,match='invalid public request fields'):
            modules['harness'].worker_stage(tmp_path/str(i),request|extra)
        assert not (tmp_path/str(i)/'output-checkpoint.json').exists()
    # Unknown fields inside a record are rejected before any learning.
    malformed={**request['items'][3]['record'],'hidden_mapping':[0,1,2]}
    fresh=modules['engine'].new('primary','informative')
    assert modules['engine'].admit(fresh,malformed,None)=='rejected'
    assert fresh['evidence']=={}
    nested=deepcopy(request)
    nested['items'].insert(0,{'record':malformed,'verified_digest':None})
    with pytest.raises(AssertionError,match='invalid public evidence fields'):
        modules['harness'].worker_stage(tmp_path/'nested',nested)
    assert not (tmp_path/'nested/output-checkpoint.json').exists()


def test_actual_serialized_indistinguishable_histories_and_restart(modules,tmp_path):
    o,h,e,c=(modules[n] for n in ('oracle','harness','engine','contract'))
    a=o.MAPPINGS[0];b=(a[2],a[1],a[0])
    ia=h.training_items(a,False);ib=h.training_items(b,False)
    assert ia==ib
    arms=[]
    for index,mapping in enumerate((a,b)):
        arm=h.begin_arm(tmp_path/str(index),'primary','informative',ia)
        first=next(entry['record'] for entry in arm['before']['evidence'].values())
        arms.append(h.end_arm(arm,h.acquisition_items(mapping,arm['before']['query']['selected'],first)))
    assert arms[0]['before']==arms[1]['before']
    assert arms[0]['before_predictions']==arms[1]['before_predictions']
    assert arms[0]['after']['analysis']['survivors']!=arms[1]['after']['analysis']['survivors']
    assert all(all(arm['checks'].values()) for arm in arms)
    assert all(not r['oracle_imported'] for arm in arms for r in arm['reports'])
    checkpoint=deepcopy(arms[0]['checkpoint']);checkpoint['state']['budget_spent']=0
    with pytest.raises(ValueError,match='integrity'):e.load_checkpoint(checkpoint)


def test_evaluation_cannot_admit_labels_or_mutate_checkpoint(modules,tmp_path):
    state,_,_=trained(modules,policy='no-acquisition')
    e,c=modules['engine'],modules['contract'];e.finish_acquisition(state)
    saved=e.checkpoint(state)
    request={'stage':'evaluate','implementation':'primary','policy':'no-acquisition','items':[]}
    checkpoint,report=modules['harness'].worker_stage(tmp_path/'readonly',request,saved)
    assert checkpoint==saved and report['loaded_digest']==saved['state_digest']
    assert (tmp_path/'readonly/input-checkpoint.json').read_bytes()==(tmp_path/'readonly/output-checkpoint.json').read_bytes()
    record=modules['oracle'].training(modules['oracle'].MAPPINGS[0])[0]
    bad={**request,'items':[{'record':record,'verified_digest':c.digest(record)}]}
    with pytest.raises(AssertionError,match='read-only'):modules['harness'].worker_stage(tmp_path/'labels',bad,saved)


def test_independent_memory_scientific_parity_across_every_policy(modules):
    e,h,o=modules['engine'],modules['harness'],modules['oracle']
    for mapping_index in range(6):
        for policy in modules['contract'].POLICIES:
            finals=[]
            for impl in ('primary','memory'):
                state,_,_=trained(modules,impl,policy,mapping_index)
                first=next(v['record'] for v in state['evidence'].values())
                request={'stage':'acquisition','implementation':impl,'policy':policy,
                         'items':h.acquisition_items(o.MAPPINGS[mapping_index],state['query']['selected'],first)}
                result,predictions=e.transition(request,state)
                finals.append((e.science(result),predictions))
            assert finals[0]==finals[1]
