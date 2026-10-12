"""Read original demo; test checkpoint-only copies with current and archived code."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import time
from lmft_lab.preservation_context import file_hash
from lmft_lab.runtime_store import Store, atomic_json


def run(output, archive, demo):
    output.mkdir(parents=True, exist_ok=False)
    original = {p.relative_to(demo).as_posix(): file_hash(p) for p in demo.rglob('*') if p.is_file()}
    checkpoint = json.loads((demo/'checkpoint.json').read_text())
    expected = checkpoint['state']['manifest']['sources']
    actual = {p.name: file_hash(p) for p in (archive/'src/lmft_lab').glob('*.py')}
    assert actual == expected, 'exact old source unavailable'
    # No replay of the user's inbox. This tests safe checkpoint recovery only.
    copy = output/'checkpoint-copy'; copy.mkdir()
    shutil.copyfile(demo/'checkpoint.json', copy/'checkpoint.json')
    command = [sys.executable,'-m','lmft_lab.runtime','--root',str(copy),'start',
               '--mode','fixture','--experiment',checkpoint['state']['experiment']]
    denied = subprocess.run(command,capture_output=True,text=True,timeout=30,
                            creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    assert denied.returncode != 0 and 'Code/config/control changed' in denied.stdout+denied.stderr
    assert json.loads((copy/'checkpoint.json').read_text()) == checkpoint
    env = dict(os.environ); env['PYTHONPATH'] = str(archive/'src')
    process = subprocess.Popen(command,cwd=archive,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,
                               creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    try:
        deadline = time.monotonic()+30
        while not (copy/'lifecycle.json').exists():
            if process.poll() is not None: raise RuntimeError(process.communicate())
            if time.monotonic()>deadline: raise TimeoutError('archived runtime did not start')
            time.sleep(.02)
        started = process.stdout.readline()
        assert 'started' in started
        Store(copy).stop()
        stdout,stderr = process.communicate(timeout=30)
        assert process.returncode == 0 and 'halted' in stdout
    finally:
        if process.poll() is None:
            Store(copy).stop();process.communicate(timeout=30)
    checks = {'archived_sources_match': actual == expected,
              'current_source_rejects_old': denied.returncode != 0,
              'archived_checkpoint_exact': file_hash(copy/'checkpoint.json') == original['checkpoint.json'],
              'original_demo_unchanged': original == {p.relative_to(demo).as_posix(): file_hash(p) for p in demo.rglob('*') if p.is_file()}}
    result = {'checks':checks,'passed':all(checks.values()),'demo_files':len(original),'source_files':len(actual),
              'archive':str(archive),'current_rejection':{'stdout':denied.stdout,'stderr':denied.stderr},
              'archived_process':{'pid':process.pid,'stdout':started+stdout,'stderr':stderr},
              'scope':'checkpoint-only copy startup/halt; no original session or queued inputs reopened'}
    atomic_json(output/'results.json',result)
    assert result['passed']
    print(json.dumps({'passed':result['passed'],'checks':checks,'demo_files':len(original)}))


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',required=True)
    parser.add_argument('--archive',default='outputs/binding-runtime-prework-001/source')
    parser.add_argument('--demo',default='outputs/action-demo-20261012T150026-75a8489b')
    args=parser.parse_args();run(Path(args.output).resolve(),Path(args.archive).resolve(),Path(args.demo).resolve())
