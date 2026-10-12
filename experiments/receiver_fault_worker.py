"""Fault-test child; physical-call marker is deliberately outside checkpoint."""
import argparse
import json
import os
from pathlib import Path
from lmft_lab import insufficiency_fixture as fixture
from lmft_lab.runtime import advance
from lmft_lab.runtime_store import Store,digest,atomic_json


def main():
    parser=argparse.ArgumentParser(); parser.add_argument("--root",required=True); parser.add_argument("--fault",choices=("before_replace","after_replace")); args=parser.parse_args()
    root=Path(args.root); store=Store(root/"individual"); state=store.read(); item=json.loads((root/"input.json").read_text())
    original=fixture.execute
    def observed(*values):
        answer=original(*values)
        with (root/"physical-calls.jsonl").open("a",encoding="utf-8") as handle:
            handle.write(json.dumps({"pid":os.getpid(),"arguments":values,"returned":answer})+"\n"); handle.flush(); os.fsync(handle.fileno())
        return answer
    fixture.execute=observed
    changed=advance(state,(state["cursor"]+1,item,None,json.dumps(item)),None)
    def fault(where):
        if where==args.fault: raise RuntimeError("controlled fault after computation")
    try: store.commit(changed,fault=fault)
    except RuntimeError: pass
    record={"pid":os.getpid(),"fault":args.fault,"restored_digest":digest(store.read())}
    atomic_json(root/("worker-"+(args.fault or "replay")+".json"),record); print(json.dumps(record))


if __name__=="__main__": main()
