"""Actual process interruption around the existing checkpoint replace boundary."""
import argparse
import json
import os
from pathlib import Path
from lmft_lab import correction_fixture as fixture
from lmft_lab.runtime import advance, run
from lmft_lab.runtime_store import Store, locked


def main():
    parser = argparse.ArgumentParser(); parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--fault', choices=('before_replace', 'after_replace')); parser.add_argument('--resume', action='store_true')
    args = parser.parse_args(); original = fixture.replacement_valid
    def counted(record, cid):
        with (args.root / 'physical-verifications.jsonl').open('a', encoding='utf-8') as stream:
            stream.write(json.dumps({'pid': os.getpid(), 'correction_id': cid}) + '\n')
            stream.flush(); os.fsync(stream.fileno())
        return original(record, cid)
    fixture.replacement_valid = counted
    if args.resume:
        run(args.root, mode='fixture', experiment='action-command-lmft')
        return
    store = Store(args.root)
    with locked(args.root / 'runtime.lock'):
        state = store.read(); changed = advance(state, store.next_input(state['cursor']), None)
        def fault(where):
            if where == args.fault:
                os._exit(17)
        store.commit(changed, fault=fault)


if __name__ == '__main__':
    main()
