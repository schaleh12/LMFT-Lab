"""Copied-checkpoint restart regressions for the independently found blockers."""
from copy import deepcopy
import importlib
import json
from pathlib import Path
import subprocess
import sys
import pytest

from lmft_lab import runtime, binding_runtime as b
from lmft_lab.binding_verifier import Adapter
from lmft_lab.preservation_context import file_hash
from lmft_lab.runtime_store import Store, atomic_json, digest


@pytest.fixture(scope='module')
def samples(tmp_path_factory):
    directory=tmp_path_factory.mktemp('binding-consistency-source')
    experiments=str(Path(__file__).resolve().parents[1]/'experiments')
    sys.path.insert(0,experiments)
    try:
        h=importlib.import_module('run_binding_runtime')
    finally:
        sys.path.remove(experiments)
    registry=directory/'private.json'
    training=h.private_registry(registry,h.oracle.MAPPINGS[0]); verifier=Adapter(registry)
    states={}
    for mode in b.MODES:
        for condition in ('informative','informative-frozen','no-acquisition'):
            manifest=runtime.software_manifest(None,'fixture')
            manifest.update(experiment=mode,fixture_rule=b.RULE,binding_policy=b.policy(condition),binding_verifier=verifier.pin)
            state=runtime.initial_state('restart-regression',True,manifest,mode)
            states[mode,condition,'training']=deepcopy(state)
            state=h.replay(state,[h.command('train-'+r['id'],'train',r) for r in training]+[h.command('select','select')],verifier)
            states[mode,condition,'pending']=deepcopy(state)
            selected=state['judgment']['query']['selected']
            if selected:
                record=json.loads(registry.read_text())['records'][selected['id']]
                state=h.replay(state,[h.command('reply','reply',record,state['judgment']['request_id'])],verifier)
            states[mode,condition,'replied']=deepcopy(state)
            state=h.replay(state,[h.command('close','close')],verifier)
            states[mode,condition,'closed']=deepcopy(state)
    for (mode,condition,phase),state in states.items():
        assert b.check_runtime(state)
        atomic_json(directory/(mode+'-'+condition+'-'+phase+'.json'),state)
    return h,states,registry,verifier


def copied(root,state):
    store=Store(root);store.commit(state)
    atomic_json(root/'lifecycle.json',{'status':'halted','pid':0})
    atomic_json(root/'stop.json',{'requested_at':0})
    (root/'runtime.lock').write_bytes(b'0')
    # A consumed queue marker preserves sequence allocation in this checkpoint-only fixture.
    atomic_json(root/'inbox'/f"{state['cursor']:012d}.json",{'consumed_cursor_marker':True})
    return store


def inventory(root):
    return {p.relative_to(root).as_posix():file_hash(p) for p in root.rglob('*') if p.is_file()}


MUTATIONS=('condition','nested-mode','outer-mode','manifest-mode','manifest-policy',
    'launch-mode','launch-condition','missing-id','closed-missing-id','removed-request',
    'duplicate-request','wrong-type','wrong-query','wrong-text','wrong-source','wrong-sender',
    'wrong-sequence','wrong-budget','wrong-correlation','wrong-cycle','missing-selection',
    'missing-reply','reply-correlation','evidence-message','missing-closure','closure-order',
    'pending-with-closure','training-orphan','no-query-orphan')


def mutated(samples,name):
    h,states,registry,verifier=samples
    condition='no-acquisition' if name=='no-query-orphan' else 'informative'
    phase=('training' if name=='training-orphan' else 'closed' if name in
           ('condition','closed-missing-id','missing-reply','reply-correlation','evidence-message',
            'missing-closure','closure-order','pending-with-closure','no-query-orphan') else 'pending')
    state=deepcopy(states['binding-primary',condition,phase]); current=state['judgment']
    mode='binding-primary'; launch_condition=condition
    req=next((o for o in state['outbox'] if o['type']=='clarification_request'),None)
    if name=='condition':current['condition']='informative-frozen'
    elif name=='nested-mode':current['mode']='binding-memory'
    elif name=='outer-mode':state['experiment']='channel'
    elif name=='manifest-mode':state['manifest']['experiment']='binding-memory'
    elif name=='manifest-policy':state['manifest']['binding_policy']=b.policy('informative-frozen')
    elif name=='launch-mode':mode='binding-memory'
    elif name=='launch-condition':launch_condition='informative-frozen'
    elif name in ('missing-id','closed-missing-id'):current['request_id']='missing-outbox-request'
    elif name=='removed-request':state['outbox'].remove(req)
    elif name=='duplicate-request':state['outbox'].append(deepcopy(req))
    elif name=='wrong-type':req['type']='response'
    elif name=='wrong-query':req['content']['query']['channels']=[2,2,2]
    elif name=='wrong-text':req['content']['text']='A different request'
    elif name=='wrong-source':req['source']='another-source'
    elif name=='wrong-sender':req['sender']='another-individual'
    elif name=='wrong-sequence':req['sequence']=999
    elif name=='wrong-budget':req['content']['budget_spent']=0
    elif name=='wrong-correlation':req['reply_to']='train-t000'
    elif name=='wrong-cycle':req['cycle']=1
    elif name=='missing-selection':state['receipts']=[r for r in state['receipts'] if r['status']!='training_closed']
    elif name=='missing-reply':state['receipts']=[r for r in state['receipts'] if r.get('message_id')!='reply']
    elif name=='reply-correlation':
        r=next(r for r in state['receipts'] if r.get('message_id')=='reply')
        r['message']['reply_to']='unrelated'
        state['processed']['reply']=runtime.message_identity(r['message'])
    elif name=='evidence-message':
        row=next(row for row in current['evidence'].values() if row['record']['split']=='acquisition')
        row['message_id']='unrelated'
    elif name=='missing-closure':state['receipts']=[r for r in state['receipts'] if r['status']!='acquisition_closed']
    elif name=='closure-order':next(r for r in state['receipts'] if r['status']=='acquisition_closed')['cycle']=1
    elif name=='pending-with-closure':current['phase']='pending'
    else:
        source=states['binding-primary','informative','pending']
        state['outbox'].append(deepcopy(next(o for o in source['outbox'] if o['type']=='clarification_request')))
    return state,mode,launch_condition


@pytest.mark.parametrize('mutation',MUTATIONS)
def test_actual_invalid_restart_preserves_all_individual_bytes(samples,tmp_path,mutation):
    state,mode,condition=mutated(samples,mutation)
    root=tmp_path/'copy';copied(root,state);before=inventory(root)
    command=[sys.executable,'-m','lmft_lab.runtime','--root',str(root),'start','--mode','fixture',
             '--experiment',mode,'--binding-condition',condition,'--binding-registry',str(samples[2])]
    result=subprocess.run(command,capture_output=True,text=True,timeout=30,
                          creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    after=inventory(root)
    evidence={'mutation':mutation,'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr,
              'before':before,'after':after,'unchanged':before==after,'process_completed':True}
    atomic_json(tmp_path/'rejection-result.json',evidence)
    assert result.returncode!=0 and 'binding' in result.stderr
    assert '"started"' not in result.stdout and '"running"' not in result.stdout
    assert before==after


@pytest.mark.parametrize('mutation',[m for m in MUTATIONS if not m.startswith('launch-')])
def test_direct_transition_rejects_before_mutating(samples,mutation):
    h,_,_,verifier=samples;state,_,_=mutated(samples,mutation);before=digest(state)
    with pytest.raises(ValueError):
        h.replay(state,[h.command('attempt','barrier')],verifier)
    assert digest(state)==before


def test_preflight_before_worker_or_lock_creation(samples,tmp_path,monkeypatch):
    state,mode,condition=mutated(samples,'missing-id');root=tmp_path/'copy';Store(root).commit(state)
    before=inventory(root)
    def forbidden(*a,**k):raise AssertionError('verifier worker constructed before guard')
    monkeypatch.setattr(runtime,'BindingVerifier',forbidden)
    with pytest.raises(ValueError,match='binding request'):
        runtime.run(root,mode='fixture',experiment=mode,binding_condition=condition,binding_registry=str(samples[2]))
    assert inventory(root)==before and not (root/'runtime.lock').exists()


@pytest.mark.parametrize('mode',b.MODES)
@pytest.mark.parametrize('condition',('informative','informative-frozen','no-acquisition'))
@pytest.mark.parametrize('phase',('pending','replied','closed'))
def test_actual_valid_resume_duplicates_and_decisions(samples,tmp_path,mode,condition,phase):
    h,states,registry,verifier=samples;state=deepcopy(states[mode,condition,phase])
    root=tmp_path/'copy';store=copied(root,state)
    process=h.start(root,mode,extra_args=['--binding-condition',condition,'--binding-registry',str(registry)])
    pid=process.pid;items=[];selected=state['judgment']['query']['selected']
    try:
        if selected:
            record=json.loads(registry.read_text())['records'][selected['id']]
            items.append(h.command('resume-reply','reply',record,state['judgment']['request_id']))
            items.append(h.command('resume-duplicate','reply',record,state['judgment']['request_id']))
        if state['judgment']['phase']=='pending':items.append(h.command('resume-close','close'))
        items += [h.command('eval-'+c['id'],'evaluate',c) for c in h.contract.held_features()]
        items.append(h.command('barrier','barrier'))
        h.send(store,process,items);final=h.halt(store,process);process=None
    finally:
        if process is not None and process.poll() is None:h.halt(store,process)
    direct=h.replay(state,items,verifier)
    predictions=h.emitted(final,'eval-')
    expected=37 if condition=='informative' else 25
    assert sum(p['decision']!='abstain' for p in predictions)==expected
    assert h.semantic(final)==h.semantic(direct)
    assert b.check_runtime(final)
    assert json.loads((root/'lifecycle.json').read_text())['status']=='halted'
    before_eval=h.replay(state,items[:-38],verifier)
    assert final['judgment']==before_eval['judgment']
    atomic_json(tmp_path/'resume-result.json',{'pid':pid,'mode':mode,'condition':condition,'phase':phase,
        'decisions':expected,'total':37,'direct_parity':True,'evaluation_immutable':True,'halted':True})
