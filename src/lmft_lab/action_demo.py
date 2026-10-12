"""Local terminal presentation of the existing synthetic action runtime."""
import argparse
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess
import sys
import time
import uuid
from . import action_runtime as adapter, action_policy, correction_fixture as fixture
from .late_evidence import late_record
from .runtime_store import Store, locked
from .action_console import terminal_input

BANNER = ('SYNTHETIC FIXTURE DEMO - no language model or freeform chat.\n'
          'Registered reports can be wrong. Typed claims never become verified evidence.\n'
          'One lifetime request; no reset. Quit/EOF stops the owned runtime and preserves files.')
HELP = 'Commands: help | inspect | request | reply | late | repeat | stop | resume | provenance | quit'


def envelope(mid, text, record=None, reply_to=None):
    evidence = text in ('reply', 'evidence')
    msg = {'schema_version': 1, 'id': mid,
           'sender': fixture.AUTHORITY if evidence else 'fixture-operator',
           'source': fixture.SOURCE if evidence else adapter.RULE,
           'type': 'teacher_reply' if reply_to else 'observation', 'content': {'text': text}}
    if record is not None:
        msg['content']['record'] = deepcopy(record)
    if reply_to:
        msg['reply_to'] = reply_to
    return msg


def render(message):
    content = message['content']
    if message['type'] == 'clarification_request':
        return f"REQUEST {message['id']}: {content['selected']['kind']} / {content['operation_id']} (budget 0)"
    if 'current' not in content:
        return content.get('text', '') + (' ' + content['reason'] if 'reason' in content else '')
    current = content['current']; historical = content['historical_request']
    lines = [f"CURRENT: {current['decision'] if current else 'not initialized'}",
             f"HISTORICAL REQUEST: {historical['status'] if historical else 'none'} | phase {content['phase']} | remaining budget {content['budget_remaining']}"]
    if current:
        unresolved = []
        for field, support in current['support'].items():
            label = 'resolved' if support['resolved'] else 'conflicting' if support['inconsistent'] else 'incomplete'
            lines.append(f"  {field}: {label}; evidence IDs: {', '.join(support['evidence_refs']) or 'none'}")
            if not support['resolved']:
                unresolved.append(field + ' ' + label)
        if current['decision'] == 'abstain':
            lines.append('ABSTENTION: ' + ('; '.join(unresolved) or current.get('scope_gate', 'predictor abstains')))
    return '\n'.join(lines)


class Demo:
    def __init__(self, root, mode, scenario, output=print):
        self.root = Path(root); self.store = Store(root); self.mode = mode; self.scenario = scenario
        self.output = output; self.process = None; self.last = None; self.counter = 0
        for path in (self.root / 'inbox').glob('[0-9]*.json'):
            if path.stat().st_size > 32000:
                continue
            try:
                mid = json.loads(path.read_text(encoding='utf-8-sig')).get('id', '')
                if isinstance(mid, str) and re.fullmatch(r'demo-[0-9]+', mid):
                    self.counter = max(self.counter, int(mid[5:]))
            except (ValueError, UnicodeError, AttributeError):
                continue

    def log(self, entry):
        with (self.root / 'demo-transcript.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps(entry, ensure_ascii=False, allow_nan=False) + '\n')

    def next_id(self):
        self.counter += 1
        return 'demo-' + str(self.counter)

    def start(self, new=False):
        if self.process is not None:
            self.output('Already running.'); return
        cmd = [sys.executable, '-m', 'lmft_lab.runtime', '--root', str(self.root), 'start',
               '--mode', 'fixture', '--experiment', self.mode]
        if new:
            cmd += ['--new', 'terminal-demo']
        self.process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
            # Keep terminal Ctrl+C in the wrapper so its finally block can request
            # the runtime's normal checkpoint-boundary stop.
            creationflags=(getattr(subprocess, 'CREATE_NO_WINDOW', 0) |
                           getattr(subprocess, 'CREATE_NEW_PROCESS_GROUP', 0)),
            start_new_session=sys.platform != 'win32')
        line = self.process.stdout.readline()
        if '"started"' not in line:
            _, error = self.process.communicate(timeout=30); self.process = None
            raise RuntimeError('Runtime could not start: ' + error.strip()[:400])
        self.log({'lifecycle': 'started', 'new': new, 'acknowledgment': json.loads(line)})
        self.output('Runtime running. No action is requested automatically.')

    def stop(self):
        if self.process is None:
            self.output('Already stopped; files preserved.'); return
        process = self.process
        if process.poll() is None:
            self.store.stop()
        stdout, stderr = process.communicate(timeout=30)
        self.process = None
        self.log({'lifecycle': 'halted', 'returncode': process.returncode, 'stdout': stdout, 'stderr': stderr,
                  'child_pid': process.pid, 'child_reaped': process.poll() is not None})
        if process.returncode != 0:
            raise RuntimeError('Runtime exited with an error; files preserved: ' + stderr[:400])
        self.output('Stopped at a checkpoint boundary. Files preserved; use resume or quit.')

    def send(self, message, command):
        after = max((o['sequence'] for o in self.store.receive()), default=0)
        barrier = envelope(self.next_id(), 'barrier')
        self.store.submit(message); self.store.submit(barrier)
        self.log({'command': command, 'submitted': [message, barrier]})
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            outputs = self.store.receive(after)
            if any(o['reply_to'] == barrier['id'] for o in outputs):
                self.log({'command': command, 'received': outputs})
                visible = [o for o in outputs if o['reply_to'] != barrier['id']]
                if not visible:
                    self.output('No new action output (replay may be deduplicated).')
                for out in visible or outputs[-1:]:
                    self.output(render(out))
                return
            if self.process.poll() is not None:
                raise RuntimeError('Runtime exited before acknowledgment; inbox and checkpoint preserved.')
            time.sleep(.02)
        raise RuntimeError('Acknowledgment timed out; stop/resume preserves queued inputs.')

    def provenance(self):
        if self.process is not None:
            self.output('Use stop first: internal provenance is available only after halt.'); return
        state = self.store.inspect(); current = state['judgment']
        self.output('HALTED PROVENANCE: registered reports are not guaranteed true.')
        for eid, entry in sorted(current['ledger'].items()):
            head = current['heads'].get(entry['root']) == eid
            verification = json.dumps(entry['verification'], ensure_ascii=False, sort_keys=True)
            self.output(f"  {'HEAD' if head else 'RETAINED ORIGINAL'} {eid}; root={entry['root']}; parent={entry.get('parent')}; source={entry['source']}; verification={verification}")
        self.log({'ui': 'provenance', 'after_halt': True})

    def execute(self, line):
        command = line.strip()
        if len(command) > 32 or command not in ('help','inspect','request','reply','late','repeat','stop','resume','provenance','quit'):
            self.output('Unknown or oversized command. ' + HELP)
            self.log({'ui_error': 'unknown or oversized command'}); return True
        if command == 'help': self.output(HELP); return True
        if command == 'quit': return False
        if command == 'stop': self.stop(); return True
        if command == 'resume': self.start(); return True
        if command == 'provenance': self.provenance(); return True
        if self.process is None:
            self.output('Session stopped. Use resume before submitting commands.'); return True
        if command == 'repeat':
            if self.last is None:
                self.output('Nothing submitted in this invocation to repeat.'); return True
            self.send(deepcopy(self.last), command); return True
        if command == 'reply':
            requests = [o for o in self.store.receive() if o['type'] == 'clarification_request']
            if not requests:
                self.output('No selected request. Use request explicitly first.'); return True
            request = requests[-1]
            record = {'episode_id': request['content']['episode_id'], 'request_id': request['id'],
                      'operation_id': request['content']['operation_id'],
                      'payload': action_policy.service_reply(request['content']['selected'])}
            self.output('Submitting the registered SYNTHETIC service reply; runtime checks it independently.')
            msg = envelope(self.next_id(), 'reply', record, request['id'])
        elif command == 'late':
            if self.scenario == 'r2':
                self.output('No registered late report exists for r2. Nothing submitted.'); return True
            case = fixture.public_case(action_policy.DEFS[self.scenario][0])
            self.output('Submitting a registered later instrument report, not a truth assertion.')
            msg = envelope(self.next_id(), 'evidence', late_record(case))
        else:
            msg = envelope(self.next_id(), command)
        self.last = deepcopy(msg); self.send(msg, command)
        return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    location = parser.add_mutually_exclusive_group()
    location.add_argument('--root', type=Path, help='Fresh directory; must not exist')
    location.add_argument('--resume', type=Path, help='Explicit halted compatible initialized session')
    parser.add_argument('--scenario', choices=adapter.SCENARIOS)
    parser.add_argument('--mode', choices=('lmft','memory'))
    parser.add_argument('--script', type=Path, help='Read the same terminal commands from a UTF-8 file')
    args = parser.parse_args(argv); demo = None
    try:
        # Check script access before creating or touching a session.
        if args.script and args.script.stat().st_size > 65536:
            raise ValueError('Script exceeds 65536 bytes.')
        commands = args.script.read_text(encoding='utf-8').splitlines() if args.script else None
        if commands is not None and len(commands) > 1000:
            raise ValueError('Script exceeds 1000 commands.')
        if args.resume:
            if args.scenario is not None or args.mode is not None:
                raise ValueError('Resume uses stored scenario/mode; do not supply overrides.')
            root = args.resume.resolve()
            if not (root/'checkpoint.json').is_file():
                raise ValueError('Resume requires an existing checkpoint.')
            state = Store(root).inspect(); mode = state.get('experiment'); scenario = state.get('action_session',{}).get('scenario')
            if mode not in adapter.MODES or scenario not in adapter.SCENARIOS:
                raise ValueError('Resume requires an initialized fixed-command session.')
        else:
            root = (args.root or Path('outputs') / ('action-demo-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S') + '-' + uuid.uuid4().hex[:8])).resolve()
            root.mkdir(parents=True, exist_ok=False)
            mode = 'action-command-' + (args.mode or 'lmft'); scenario = args.scenario or 'r1'
        demo = Demo(root, mode, scenario)
        with locked(root/'demo.lock'), terminal_input(enabled=commands is None, log=demo.log) as read_input:
            print(BANNER); print('Session:', root); print('Scenario:', scenario, '| Mode:', mode); print(HELP)
            try:
                demo.start(new=not bool(args.resume))
                if not args.resume:
                    demo.send(envelope(demo.next_id(), 'initialize '+scenario), 'initialize '+scenario)
                if commands is not None:
                    for line in commands:
                        print('demo> ' + (line if len(line)<=32 else '[oversized command]'))
                        if not demo.execute(line): break
                else:
                    while demo.execute(read_input('demo> ')):
                        pass
            except (EOFError, KeyboardInterrupt) as exc:
                demo.log({'input_ended': type(exc).__name__})
                print('\nInput ended; stopping safely and preserving this session.')
            finally:
                if demo.process is not None:
                    demo.stop()
        return 0
    except (OSError, ValueError, RuntimeError, subprocess.TimeoutExpired) as exc:
        print('Demo error: ' + str(exc)[:500], file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
