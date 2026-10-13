"""Fresh-process worker; stdin is public input and strict verifier responses only."""
import argparse
import importlib.abc
import json
import os
from pathlib import Path
import sys


class Boundary(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in ('context_applicability_device', 'run_context_applicability'):
            raise ImportError('private coordinator module unavailable to worker')
        return None


sys.meta_path.insert(0, Boundary())
import context_applicability_contract as c
import context_applicability_engine as engine
from lmft_lab.runtime_store import Store
from lmft_lab.local_models import strict_json


def send(value):
    print(c.canonical(value), flush=True)


def verify(record):
    send({'kind': 'verify', 'record': record})
    response = strict_json(sys.stdin.readline())
    if type(response) is not dict or set(response) != {'accepted'} or type(response['accepted']) is not bool:
        raise ValueError('invalid verifier response')
    return response['accepted']


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--controller', required=True, choices=c.CONTROLLERS)
    parser.add_argument('--schedule', required=True, choices=c.SCHEDULES)
    parser.add_argument('--stage', required=True, choices=('initial', 'followup', 'reload'))
    args = parser.parse_args()
    request = strict_json(sys.stdin.readline())
    if (type(request) is not dict or set(request) != {'events', 'cases'}
            or type(request['events']) is not list or type(request['cases']) is not list):
        raise ValueError('invalid public worker request')
    store = Store(Path.cwd())
    if args.stage == 'initial':
        if (store.root / 'checkpoint.json').exists():
            raise ValueError('fresh checkpoint already exists')
        state = engine.newborn(args.controller, args.schedule)
    else:
        state = store.read()
        engine.validate(state, args.controller, args.schedule)
        if state['phase'] != ('ready' if args.stage == 'followup' else 'closed'):
            raise ValueError('stage/phase mismatch')
    if args.stage == 'reload' and request['events']:
        raise ValueError('reload must be read-only')
    for item in request['events']:
        state = engine.advance(state, item, verify)
    expected_phase = 'ready' if args.stage == 'initial' else 'closed'
    if state['phase'] != expected_phase:
        raise ValueError('incomplete stage')
    engine.validate(state, args.controller, args.schedule)
    predictions = engine.evaluate(state, request['cases'])
    renamed = engine.evaluate(state, c.rename_cases(request['cases']))
    probes = engine.evaluate(state, c.integrity_cases())
    mappings = [engine.mapping(state, list(ctx)) for ctx in c.CONTEXTS]
    if args.stage != 'reload':
        store.commit(state)
    send({'kind': 'result', 'pid': os.getpid(), 'state': state, 'predictions': predictions,
          'renamed': renamed, 'probes': probes, 'mappings': mappings})


if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print(str(exc), file=sys.stderr)
        raise SystemExit(1)
