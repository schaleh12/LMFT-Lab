"""Test-only gate after real reply submission for an observable PTY interrupt."""
import argparse
import json
from pathlib import Path
import time
from lmft_lab import action_demo
from lmft_lab.runtime_store import Store


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--root',type=Path,required=True)
    parser.add_argument('--gate',type=Path,required=True)
    args=parser.parse_args();args.gate.mkdir(parents=True,exist_ok=False)
    original=Store.submit
    def submit(store,message):
        result=original(store,message)
        if message['content']['text']=='reply':
            (args.gate/'waiting.json').write_text(json.dumps({'phase':'after_reply_submit_before_barrier','message_id':message['id']}))
            print('TEST GATE: reply submitted; waiting for release.',flush=True)
            deadline=time.monotonic()+45
            while not (args.gate/'release').exists():
                if time.monotonic()>deadline:raise RuntimeError('Test gate timeout')
                time.sleep(.02)
        return result
    Store.submit=submit
    try:return action_demo.main(['--root',str(args.root),'--scenario','r1'])
    finally:Store.submit=original


if __name__=='__main__':raise SystemExit(main())
