"""Four frozen development inputs, offline local transport, no repair/retry."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

from lmft_lab.local_models import LocalModels, load_config, strict_json
from lmft_lab.model_assets import BACKEND_FILES, ModelError, digest_file
from lmft_lab.runtime_store import Store, atomic_json, digest
import slm_representation as c

EXPORT_HASH = '77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90'
RESEARCH = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives')
CACHE = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\cache')


def assets(config, cache):
    spec = config['models'][config['roles']['interpretation']]
    expected = {'repo_id':'Qwen/Qwen3-4B-GGUF',
                'revision':'bc640142c66e1fdd12af0bd68f40445458f3869b',
                'filename':'Qwen3-4B-Q4_K_M.gguf',
                'sha256':'7485fe6f11af29433bc51cab58009521f205840f5b4ae3a32fa7f92e8534fdf5'}
    if spec != expected or config['generation'] != {'context_size':8192,'max_tokens':1024,
            'temperature':0,'seed':42,'timeout_seconds':120}:
        raise ValueError('unapproved model/settings')
    model = cache/'models'/spec['repo_id'].replace('/','--')/spec['revision']/spec['filename']
    if not model.is_file() or digest_file(model) != spec['sha256']:
        raise ValueError('missing/mismatched model; no download allowed')
    hashes = {str(model):spec['sha256']}
    for name, expected in BACKEND_FILES.items():
        archive = cache/'backend/b11429'/name
        if not archive.is_file() or digest_file(archive) != expected:
            raise ValueError('missing/mismatched backend archive')
        hashes[str(archive)] = expected
        with zipfile.ZipFile(archive) as z:
            for info in z.infolist():
                if info.is_dir():
                    continue
                p = (cache/'backend/b11429/bin'/info.filename).resolve()
                if not p.is_relative_to((cache/'backend/b11429/bin').resolve()):
                    raise ValueError('unsafe backend path')
                expected_hash = hashlib.sha256(z.read(info)).hexdigest()
                if not p.is_file() or digest_file(p) != expected_hash:
                    raise ValueError('missing/mismatched extracted backend; no repair allowed')
                hashes[str(p)] = expected_hash
    return hashes


def select(rows):
    keys = sorted({r['target_sense_key'] for r in rows})[:4]
    if len(keys) != 4:
        raise ValueError('four represented categories required')
    return [min((r for r in rows if r['target_sense_key']==key),key=lambda r:r['example_id'])
            for key in keys]


def prepare(export_dir, work_dir):
    work_dir = Path(work_dir).resolve()
    if work_dir.parent != RESEARCH.resolve():
        raise ValueError('use fresh direct child of approved research-archives')
    export_dir = Path(export_dir)
    if digest_file(export_dir/'development.json') != EXPORT_HASH:
        raise ValueError('unapproved development export')
    config = load_config(c.ROOT/'config/local_models.json')
    verified = assets(config, CACHE)
    rows = strict_json((export_dir/'development.json').read_text(encoding='utf-8'))
    selected = select(rows)
    work_dir.mkdir(exist_ok=False)
    for name in ('README','LICENSE','USE-NOTICE.txt','DATASET-LICENSES.md'):
        shutil.copy2(export_dir/name,work_dir/name)
    cases = []
    for i, original in enumerate(selected,1):
        index = original['target_index']; tokens = original['surface_tokens']
        source = {'tokens':tokens,'target':{'start':index,'end':index+1,'quote':tokens[index]}}
        request = c.request(source,config['generation'])
        cases.append({'id':f'representation-{i:02d}', 'original':original,
                      'original_sha256':digest(original),'source':source,
                      'source_sha256':digest(source),'request':request,
                      'request_sha256':hashlib.sha256(json.dumps(request,sort_keys=True).encode()).hexdigest()})
    atomic_json(work_dir/'cases.json',cases)
    atomic_json(work_dir/'schema.json',c.schema())
    (work_dir/'system-prompt.txt').write_text(c.SYSTEM,encoding='utf-8')
    atomic_json(work_dir/'asset-verification.json',verified)
    frozen = {'kind':c.KIND,'pins':c.pins(),'export_sha256':EXPORT_HASH,
              'config':config,'attempt_limit':4,'cases_sha256':digest_file(work_dir/'cases.json'),
              'schema_sha256':digest_file(work_dir/'schema.json'),
              'system_prompt_sha256':digest_file(work_dir/'system-prompt.txt'),
              'asset_verification_sha256':digest_file(work_dir/'asset-verification.json'),
              'selection':[{'id':x['id'],'example_id':x['original']['example_id'],
                'selection_sense_key':x['original']['target_sense_key'],
                'original_sha256':x['original_sha256'],'source_sha256':x['source_sha256'],
                'request_sha256':x['request_sha256']} for x in cases]}
    atomic_json(work_dir/'frozen-manifest.json',frozen)
    return frozen


def capture(cases, config, work_dir, factory=LocalModels):
    """One fresh invocation only; explicit failure reports keep a healthy server alive."""
    if len(cases) != 4 or len({x['id'] for x in cases}) != 4:
        raise ValueError('exactly four distinct frozen inputs required')
    marker = work_dir/'run-started.json'
    with marker.open('x',encoding='utf-8') as stream:
        stream.write(c.canonical({'attempt_limit':4,'resume_allowed':False}))
    client = factory(config,root=CACHE,offline=True)
    state = c.newborn(); results = []; server_pid = None; calls = 0
    try:
        for case in cases:
            if server_pid is not None and (client.process is None or client.process.poll() is not None):
                results.append({'id':case['id'],'status':'unattempted_server_lost'})
                break
            calls += 1
            atomic_json(work_dir/'attempts.json',{'attempt_count':calls,'current_id':case['id']})
            try:
                report, trace = client.generate('interpretation',case['request'],c.KIND,
                    lambda raw:c.validation_report(raw,case['source']))
                pid = client.process.pid if client.process else None
                if server_pid is not None and pid != server_pid:
                    raise RuntimeError('owned server changed unexpectedly')
                server_pid = pid
                raw = trace['response']['choices'][0]['message']['content']
                value = c.record(case['id'],case['source'],case['original_sha256'],raw,trace)
                if c.canonical(value['result']) != c.canonical(report):
                    raise ValueError('validation report mismatch')
                state = c.append(state,value)
                Store(work_dir/'neutral-state').commit(state)
                atomic_json(work_dir/f"{case['id']}-trace.json",trace)
                results.append({'id':case['id'],'status':value['lifecycle'],
                                'admissible':report['admissible'],'errors':report['errors'],
                                'elapsed_seconds':trace['elapsed_seconds'],
                                'usage':trace['response'].get('usage'),
                                'finish_reason':trace['response']['choices'][0].get('finish_reason'),
                                'trace_sha256':digest(trace),'raw_response_sha256':hashlib.sha256(raw.encode()).hexdigest(),
                                'request_sha256':trace['request_sha256'],
                                'proposal_status':report['proposal']['status'] if report['admissible'] else None})
            except (ModelError,OSError,ValueError,RuntimeError,KeyError,TypeError) as exc:
                trace = getattr(exc,'trace',{'error':str(exc)})
                atomic_json(work_dir/f"{case['id']}-failed-trace.json",trace)
                results.append({'id':case['id'],'status':'transport_or_capture_failed',
                                'error':str(exc),'trace_sha256':digest(trace)})
                break
    finally:
        owned = client.process
        if server_pid is None and owned is not None:
            server_pid = owned.pid
        client.close()
        closed = owned is None or owned.poll() is not None
    attempted_ids = {x['id'] for x in results}
    results.extend({'id':x['id'],'status':'unattempted_after_failure'} for x in cases if x['id'] not in attempted_ids)
    summary = {'attempts':calls,'attempt_limit':4,'server_pid':server_pid,'owned_server_closed':closed,
               'results':results,'state_sha256':digest(state),'source_pins':c.pins(),
               'model_config':config,'model_calls_authorized':True,'heldout_used':False}
    if hasattr(client,'log_path'):
        log = Path(client.log_path)
        if log.is_file():
            shutil.copy2(log,work_dir/'owned-server.log')
            summary['server_log_sha256'] = digest_file(work_dir/'owned-server.log')
    atomic_json(work_dir/'summary.json',summary)
    return summary


def run(work_dir):
    work_dir = Path(work_dir).resolve()
    if work_dir.parent != RESEARCH.resolve():
        raise ValueError('unapproved work directory')
    frozen = strict_json((work_dir/'frozen-manifest.json').read_text(encoding='utf-8'))
    if c.canonical(frozen['pins']) != c.canonical(c.pins()) or frozen['attempt_limit'] != 4:
        raise ValueError('frozen source/limit mismatch')
    for name,key in [('cases.json','cases_sha256'),('schema.json','schema_sha256'),
                     ('system-prompt.txt','system_prompt_sha256'),('asset-verification.json','asset_verification_sha256')]:
        if digest_file(work_dir/name) != frozen[key]:
            raise ValueError('frozen artifact changed')
    verified = assets(frozen['config'],CACHE)
    if c.canonical(verified) != c.canonical(strict_json((work_dir/'asset-verification.json').read_text())):
        raise ValueError('asset set changed')
    cases = strict_json((work_dir/'cases.json').read_text(encoding='utf-8'))
    summary = capture(cases,frozen['config'],work_dir)
    checkpoint = work_dir/'neutral-state/checkpoint.json'
    if checkpoint.exists():
        before = digest_file(checkpoint)
        command = [sys.executable,str(c.ROOT/'experiments/slm_representation.py'),
                   '--state-dir',str(checkpoint.parent)]
        env = {**os.environ,'PYTHONPATH':str(c.ROOT/'src')}
        restart = subprocess.run(command,capture_output=True,text=True,env=env,timeout=30)
        (work_dir/'restart.stdout').write_text(restart.stdout,encoding='utf-8')
        (work_dir/'restart.stderr').write_text(restart.stderr,encoding='utf-8')
        if restart.returncode:
            raise RuntimeError('restart retrieval failed; captured logs retained')
        restored = strict_json(restart.stdout)
        if (restored['state_sha256'] != summary['state_sha256'] or digest_file(checkpoint) != before or
                any(x['primary'] != x['ordinary_memory'] for x in restored['record_hashes'].values())):
            raise ValueError('restart/nonmutation/consumer parity failure')
        summary['restart'] = {'checkpoint_nonmutation':True,'consumer_parity':True,
                              'record_hashes':restored['record_hashes'],
                              'checkpoint_sha256':before}
    atomic_json(work_dir/'summary.json',summary)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('phase',choices=('prepare','run'))
    parser.add_argument('--work-dir',required=True)
    parser.add_argument('--export-dir')
    args = parser.parse_args()
    result = prepare(args.export_dir,args.work_dir) if args.phase=='prepare' else run(args.work_dir)
    print(c.canonical(result))
