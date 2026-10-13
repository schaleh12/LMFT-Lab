"""One request per process; predict never receives labels or writes checkpoints."""
import argparse
import json
import os
from pathlib import Path
import sys

from lmft_lab.local_models import strict_json
from lmft_lab.runtime_store import Store, digest, locked
import linguistic_application as app


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=('train', 'predict', 'inspect'))
    parser.add_argument('--state-dir', type=Path, required=True)
    args = parser.parse_args()
    store = Store(args.state_dir)
    with locked(args.state_dir / 'runtime.lock'):
        if args.operation == 'train':
            request = strict_json(sys.stdin.read())
            exists = (args.state_dir / 'checkpoint.json').exists()
            state = store.read() if exists else app.newborn(request['split_id'])
            app.validate(state)
            updated = app.advance(state, request)
            if updated != state:
                store.commit(updated)
            result = {'stage': updated['stage'], 'state_digest': digest(updated),
                      'examples': len(updated['examples']), 'replayed': updated == state}
        else:
            state = store.read()
            app.validate(state)
            if args.operation == 'predict':
                request = strict_json(sys.stdin.read())
                app.exact(request, {'items'})
                result = {'stage': state['stage'], 'predictions': app.predict(state, request['items']),
                          'state_digest': digest(state)}
            else:
                result = {'stage': state['stage'], 'examples': len(state['examples']),
                          'state_digest': digest(state), 'pins': state['pins']}
    print(json.dumps({'pid': os.getpid(), **result}, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
