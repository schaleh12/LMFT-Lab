"""Wrapper acceptance includes real child processes and direct-runtime replay."""
import importlib
import json
from pathlib import Path
import subprocess
import sys
import pytest
from lmft_lab import action_demo
from lmft_lab.runtime_store import Store


@pytest.fixture
def harness(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1]/'experiments'))
    return importlib.import_module('run_action_demo')


@pytest.mark.parametrize('scenario',['r1','r8','r2'])
def test_actual_terminal_direct_runtime_equivalence(harness,tmp_path,scenario):
    result=harness.run_case(tmp_path/'case','lmft',scenario)
    assert all(result['checks'].values())


@pytest.mark.parametrize('ending',[EOFError,KeyboardInterrupt])
def test_input_exit_stops_actual_owned_runtime(monkeypatch,tmp_path,ending):
    def end(prompt):raise ending()
    monkeypatch.setattr('builtins.input',end)
    root=tmp_path/'session'
    assert action_demo.main(['--root',str(root)])==0
    assert json.loads((root/'lifecycle.json').read_text())['status']=='halted'
    assert Store(root).inspect()['action_session']['scenario']=='r1'
    assert ending.__name__ in (root/'demo-transcript.jsonl').read_text()


def test_fresh_protects_existing_empty_directory_and_file(tmp_path):
    directory=tmp_path/'exists';directory.mkdir();file=tmp_path/'file';file.write_text('preserve')
    assert action_demo.main(['--root',str(directory)])==1 and list(directory.iterdir())==[]
    assert action_demo.main(['--root',str(file)])==1 and file.read_text()=='preserve'


def test_invalid_script_or_resume_never_creates_session(tmp_path):
    missing=tmp_path/'missing';root=tmp_path/'new'
    assert action_demo.main(['--root',str(root),'--script',str(missing)])==1 and not root.exists()
    assert action_demo.main(['--resume',str(missing)])==1 and not missing.exists()
    huge=tmp_path/'huge.txt';huge.write_text('x'*65537)
    assert action_demo.main(['--root',str(root),'--script',str(huge)])==1 and not root.exists()


def test_default_fresh_paths_are_unique(monkeypatch,tmp_path):
    monkeypatch.chdir(tmp_path)
    # Keep package resolution for the actual child while using a temporary cwd.
    monkeypatch.setenv('PYTHONPATH',str(Path(action_demo.__file__).resolve().parents[1]))
    script=tmp_path/'quit.txt';script.write_text('quit\n')
    assert action_demo.main(['--script',str(script)])==0
    assert action_demo.main(['--script',str(script)])==0
    roots=list((tmp_path/'outputs').iterdir());assert len(roots)==2
    assert all((r/'checkpoint.json').exists() for r in roots)


def test_resume_rejects_override_and_foreign_mode_without_checkpoint_change(tmp_path,harness):
    script=tmp_path/'commands';script.write_text('quit\n');root=tmp_path/'session'
    assert action_demo.main(['--root',str(root),'--script',str(script)])==0
    checkpoint=(root/'checkpoint.json').read_bytes()
    assert action_demo.main(['--resume',str(root),'--scenario','r8','--script',str(script)])==1
    assert (root/'checkpoint.json').read_bytes()==checkpoint
    # A separate valid foreign fixture individual is created through its runtime.
    foreign=tmp_path/'foreign'
    from run_comparative import start,halt
    process=start(foreign,'correction-lmft',new=True);halt(Store(foreign),process)
    original=(foreign/'checkpoint.json').read_bytes()
    assert action_demo.main(['--resume',str(foreign),'--script',str(script)])==1
    assert (foreign/'checkpoint.json').read_bytes()==original
