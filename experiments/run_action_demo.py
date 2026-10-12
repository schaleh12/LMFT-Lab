"""Scripted real-process terminal/direct-runtime equivalence; no mocked learner."""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import shutil
import subprocess
import sys
from lmft_lab import action_runtime as adapter, preservation_context as preservation
from lmft_lab.runtime_store import Store, atomic_json
from run_comparative import send, halt
from run_action_runtime import semantic, science

PROTOCOL=Path('experiments/ACTION_DEMO_PROTOCOL.md')
WALKTHROUGH=['inspect','reply','I claim success','x'*40,'provenance','request','repeat','stop','resume',
             'reply','repeat','late','repeat','inspect','request','stop','provenance','resume','inspect','quit']
RESUME=['inspect','request','reply','late','inspect','quit']


def invoke(args, output):
    result=subprocess.run([sys.executable,'-m','lmft_lab.action_demo',*map(str,args)],capture_output=True,text=True,timeout=90)
    atomic_json(output,{'args':list(map(str,args)),'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    return result


def run_case(root,mode,scenario):
    root.mkdir(parents=True,exist_ok=False);session=root/'session';script=root/'commands.txt'
    script.write_text('\n'.join(WALKTHROUGH)+'\n');resume_script=root/'resume.txt';resume_script.write_text('\n'.join(RESUME)+'\n')
    args=['--root',session,'--mode',mode,'--scenario',scenario,'--script',script]
    first=invoke(args,root/'fresh-output.json')
    if first.returncode:raise AssertionError(first.stderr)
    store=Store(session);initial=store.inspect();before=(session/'checkpoint.json').read_bytes()
    transcript_before=(session/'demo-transcript.jsonl').read_bytes()
    collision=invoke(args,root/'collision-output.json')
    checks={'collision_rejected':collision.returncode==1,
        'collision_checkpoint_unchanged':(session/'checkpoint.json').read_bytes()==before,
        'collision_transcript_unchanged':(session/'demo-transcript.jsonl').read_bytes()==transcript_before,
        'first_halted':json.loads((session/'lifecycle.json').read_text())['status']=='halted',
        'synthetic_banner':'SYNTHETIC FIXTURE DEMO' in first.stdout,
        'provenance_boundary':'Use stop first' in first.stdout and 'HALTED PROVENANCE' in first.stdout,
        'historical_display':'HISTORICAL REQUEST:' in first.stdout,
        'unknown_rejected':'Unknown or oversized command' in first.stdout,
        'fixed_source_display':'source=registered-instrument-log-1' in first.stdout,
        'zero_budget_display':'remaining budget 0' in first.stdout}
    resumed=invoke(['--resume',session,'--script',resume_script],root/'resume-output.json')
    if resumed.returncode:raise AssertionError(resumed.stderr)
    final=store.inspect();atomic_json(root/'final-halted.json',final)
    checks['resume_no_scientific_change']=science(initial,initial['action_session']['case'])==science(final,final['action_session']['case'])
    checks['one_lifetime_request']=len([o for o in final['outbox'] if o['type']=='clarification_request'])==final['episode']['charged']==1
    checks['no_repeat_initialization']=sum(r.get('status')=='initialized' for r in final['receipts'])==1
    checks['exact_replay_dedup']=any(r.get('status')=='duplicate' for r in final['receipts'])
    checks['final_halted']=json.loads((session/'lifecycle.json').read_text())['status']=='halted'
    lines=[json.loads(line) for line in (session/'demo-transcript.jsonl').read_text().splitlines()]
    submitted=[m for row in lines for m in row.get('submitted',[])]
    direct=Store(root/'direct')
    process=subprocess.Popen([sys.executable,'-m','lmft_lab.runtime','--root',str(direct.root),'start',
        '--mode','fixture','--experiment','action-command-'+mode,'--new','terminal-demo'],
        stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    try:
        if 'started' not in process.stdout.readline():raise RuntimeError(process.communicate())
        send(direct,process,submitted)
        reference=halt(direct,process);process=None
    finally:
        if process is not None and process.poll() is None:halt(direct,process)
    atomic_json(root/'direct-halted.json',reference)
    checks['direct_complete_semantic_parity']=semantic(final)==semantic(reference)
    checks['expected_final']=adapter.snapshot(final)['current']['decision']==('success' if scenario=='r2' else 'abstain')
    checks['current_historical_distinct']=adapter.snapshot(final)['historical_request']['status']==('resolved_by_gather' if scenario=='r2' else 'resolved_by_correction')
    if scenario!='r2':checks['abstention_reason_display']='ABSTENTION: shielded conflicting' in first.stdout
    result={'checks':checks,'mode':mode,'scenario':scenario,'messages':len(submitted),'final':final}
    atomic_json(root/'result.json',result)
    if not all(checks.values()):raise AssertionError([k for k,v in checks.items() if not v])
    return result


def run(root,context_path):
    root.mkdir(parents=True,exist_ok=False);context=json.loads(context_path.read_text());preservation.verify_current(context,Path.cwd())
    for n in context['files']:
        dst=root/'archive'/n;dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(n,dst)
    shutil.copy2(context_path,root/'current-preservation-context.json');atomic_json(root/'archive-manifest.json',context['files'])
    atomic_json(root/'provenance.json',{'source_commit':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        'working_tree':subprocess.check_output(['git','status','--short'],text=True),'protocol_sha256':preservation.file_hash(PROTOCOL),
        'preservation_kind':preservation.KIND,'preservation_context_sha256':preservation.file_hash(context_path),'model_calls':0})
    try:
        rows={}
        for mode in ('lmft','memory'):
            for scenario in adapter.SCENARIOS:
                preservation.pinned_current(root,Path.cwd());rows[mode+'/'+scenario]=run_case(root/(mode+'-'+scenario),mode,scenario)
        checks={}
        for scenario in adapter.SCENARIOS:
            a=rows['lmft/'+scenario]['final'];b=rows['memory/'+scenario]['final']
            checks[scenario+'_memory_parity']=science(a,a['action_session']['case'])==science(b,b['action_session']['case'])
        preservation.pinned_current(root,Path.cwd());checks['source_archive']=all(preservation.file_hash(root/'archive'/n)==v for n,v in context['files'].items())
        values=list(checks.values())+[v for r in rows.values() for v in r['checks'].values()]
        result={'checks':checks,'integrity_passed':sum(values),'integrity_total':len(values),'model_calls':0,
                'messages':{k:r['messages'] for k,r in rows.items()},'requests':sum(r['final']['episode']['charged'] for r in rows.values())}
        atomic_json(root/'results.json',result);print(json.dumps(result))
        if not all(values):raise AssertionError('demo comparison failed')
        return result
    except Exception as exc:
        atomic_json(root/'failure.json',{'error':repr(exc)});raise


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--preservation-context',type=Path,required=True)
    args=p.parse_args();run(args.output,args.preservation_context)
