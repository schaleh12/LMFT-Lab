"""Synthetic contract/transport tests; no model or natural corpus access."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

import pytest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'experiments'))
import slm_representation as c
import run_slm_representation as runner
from lmft_lab.local_models import load_config
from lmft_lab.model_assets import ModelError
from lmft_lab.runtime_store import Store,digest


def source():
    return {'tokens':['Please','order','blue widgets','.'],
            'target':{'start':1,'end':2,'quote':'order'}}


def proposal():
    return {'schema_version':1,'status':'one_reading','target':source()['target'],
            'readings':[{'gloss':'Synthetic request to obtain objects.',
                         'anchors':[{'start':0,'end':3,'quote':'Please order blue widgets'}],
                         'relations':[],'conditions':[]}],'uncertainties':[]}


def trace(raw):
    config=load_config(c.ROOT/'config/local_models.json')
    req=c.request(source(),config['generation'])
    return {'model':config['models']['qwen3_4b'],'generation':config['generation'],
            'role':'interpretation','request_sha256':hashlib.sha256(json.dumps(req,sort_keys=True).encode()).hexdigest(),
            'response':{'choices':[{'message':{'content':raw},'finish_reason':'stop'}],
                        'usage':{'completion_tokens':1}},'elapsed_seconds':0.0}


def record(raw=None):
    raw=json.dumps(proposal()) if raw is None else raw
    return c.record('synthetic-1',source(),'0'*64,raw,trace(raw))


@pytest.mark.parametrize('mutate',[
    lambda p:p.update(schema_version=True),lambda p:p.update(schema_version=1.0),
    lambda p:p.update(extra='forbidden'),lambda p:p.pop('target'),
    lambda p:p['target'].update(start=True),lambda p:p['target'].update(start=1.0),
    lambda p:p['target'].update(end=1),lambda p:p['target'].update(end=99),
    lambda p:p['target'].update(quote='invented'),
    lambda p:p.update(target={'start':0,'end':1,'quote':'Please'}),
    lambda p:p.update(status='confident'),lambda p:p.update(readings=[]),
    lambda p:p.update(status='alternatives'),lambda p:p.update(uncertainties=[''] ),
    lambda p:p['readings'][0].update(anchors=[]),
    lambda p:p['readings'][0]['anchors'][0].update(quote='wrong'),
    lambda p:p['readings'][0]['anchors'][0].update(start=False),
    lambda p:p['readings'][0].update(anchors=[source()['target']]),
    lambda p:p['readings'][0].update(gloss='x'*241),
    lambda p:p['readings'][0].update(relations=[{'text':'unsupported schema','anchors':[]}]),
])
def test_invalid_output_rejected_without_source_mutation(mutate):
    s=source();before=digest(s);p=proposal();mutate(p)
    result=c.validation_report(json.dumps(p),s)
    assert not result['admissible'] and result['proposal'] is None and result['errors']
    assert digest(s)==before


@pytest.mark.parametrize('raw',['not json','[]','{"schema_version":1,"schema_version":1}','NaN'])
def test_malformed_raw_preserved_as_rejected_record(raw):
    r=record(raw);c.validate_record(r)
    assert r['raw']==raw and r['lifecycle']=='rejected'


def test_overlapping_spans_allowed_but_duplicate_ranges_rejected():
    p=proposal();p['readings'][0]['anchors'].append({'start':2,'end':3,'quote':'blue widgets'})
    assert c.validate(json.dumps(p),source())==p
    p['readings'][0]['anchors'][1]=deepcopy(p['readings'][0]['anchors'][0])
    assert not c.validation_report(json.dumps(p),source())['admissible']


def test_ambiguity_and_explicit_insufficient_context():
    p=proposal();p['status']='alternatives';p['readings'].append(deepcopy(p['readings'][0]))
    p['readings'][1]['gloss']='A second synthetic possibility.'
    assert c.validate(json.dumps(p),source())==p
    p.update(status='insufficient_context',readings=[],uncertainties=['Synthetic missing context.'])
    assert c.validate(json.dumps(p),source())==p
    p['uncertainties']=[]
    assert not c.validation_report(json.dumps(p),source())['admissible']


def test_anchor_validity_does_not_claim_semantic_correctness():
    p=proposal();p['readings'][0]['gloss']='The source proves a fictional moon is made of cheese.'
    r=record(json.dumps(p));c.validate_record(r)
    assert r['result']['admissible'] and r['lifecycle']=='unverified_proposal'


def test_duplicate_conflict_and_consumer_nonmutation():
    s=c.newborn();r=record();s=c.append(s,r);before=digest(s)
    assert c.append(s,r)==s
    assert c.retrieve(s,r['id'],'primary')==c.retrieve(s,r['id'],'ordinary_memory')==r
    retrieved=c.retrieve(s,r['id'],'primary');retrieved['raw']='modified copy'
    other=record('[]')
    with pytest.raises(ValueError,match='conflicting'):c.append(s,other)
    assert digest(s)==before


@pytest.mark.parametrize('change',[
    lambda r:r.update(source_sha256='f'*64),
    lambda r:r['source']['tokens'].__setitem__(0,'Different'),
    lambda r:r.update(role='teacher'),lambda r:r.update(author='trusted-fact'),
    lambda r:r.update(lifecycle='accepted'),lambda r:r.update(request_sha256='0'*64),
    lambda r:r['result']['proposal'].update(schema_version=True),
    lambda r:r['result']['proposal']['target'].update(start=1.0),
    lambda r:r['generation'].update(seed=42.0),
])
def test_provenance_and_cached_type_corruption_reject(change):
    r=record();change(r)
    with pytest.raises(ValueError):c.validate_record(r)


def test_request_contains_only_tokens_target_and_instructions():
    config=load_config(c.ROOT/'config/local_models.json');req=c.request(source(),config['generation'])
    user=json.loads(req['messages'][1]['content'])
    assert set(user)=={'surface_tokens','target'}
    assert req['temperature']==0 and req['seed']==42 and req['max_tokens']==1024
    assert req['chat_template_kwargs']=={'enable_thinking':False}


def test_mechanical_selection_sorted_keys_then_id():
    rows=[{'target_sense_key':sense,'example_id':id} for sense in ['e','c','a','d','b'] for id in ['z','a']]
    assert [(x['target_sense_key'],x['example_id']) for x in runner.select(rows)]==[(s,'a') for s in 'abcd']


def test_actual_process_restart_identical_retrieval_and_corruption_refusal(tmp_path):
    s=c.append(c.newborn(),record());s=c.append(s,{**record('[]'),'id':'synthetic-rejected'})
    store=Store(tmp_path);store.commit(s);before=(tmp_path/'checkpoint.json').read_bytes()
    command=[sys.executable,str(c.ROOT/'experiments/slm_representation.py'),'--state-dir',str(tmp_path)]
    env={**os.environ,'PYTHONPATH':str(c.ROOT/'src')}
    response=subprocess.run(command,capture_output=True,text=True,env=env,check=True)
    restored=json.loads(response.stdout)
    assert restored['state_sha256']==digest(s)
    assert all(v['primary']==v['ordinary_memory'] for v in restored['record_hashes'].values())
    assert before==(tmp_path/'checkpoint.json').read_bytes()
    s['schema_version']=True;store.commit(s)
    assert subprocess.run(command,capture_output=True,text=True,env=env).returncode!=0


class Process:
    pid=123
    dead=False
    def poll(self):return 0 if self.dead else None


class Fake:
    raw='[]'
    fail=False
    calls=0
    def __init__(self,*args,**kwargs):self.process=Process()
    def generate(self,role,request,version,validator):
        type(self).calls+=1
        assert role=='interpretation'
        if self.fail:raise ModelError('synthetic transport failure')
        return validator(self.raw),trace(self.raw)
    def close(self):self.process.dead=True;self.process=None


@pytest.mark.parametrize('failure', [False,True])
def test_attempt_cap_no_repairs_restart_or_resume_after_failure(tmp_path,failure):
    Fake.calls=0;Fake.fail=failure
    config=load_config(c.ROOT/'config/local_models.json')
    cases=[{'id':f'synthetic-{i}','source':source(),'original_sha256':'0'*64,
            'request':c.request(source(),config['generation'])} for i in range(4)]
    result=runner.capture(cases,config,tmp_path,factory=Fake)
    assert Fake.calls==result['attempts']==(1 if failure else 4)
    assert result['owned_server_closed']
    if not failure:assert all(x['status']=='rejected' for x in result['results'])
    else:assert sum(x['status']=='unattempted_after_failure' for x in result['results'])==3
    with pytest.raises(FileExistsError):runner.capture(cases,config,tmp_path,factory=Fake)
