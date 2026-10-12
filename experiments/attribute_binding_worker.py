"""Fresh process, public requests/checkpoints only; no oracle import or labels."""
import importlib.abc
import json
import os
from pathlib import Path
import sys


class NoOracle(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path=None, target=None):
        if fullname in ('attribute_binding_oracle', 'lmft_lab.capacity_fixture'):
            raise ImportError('oracle is outside the learner process boundary')
        return None


sys.meta_path.insert(0, NoOracle())
import attribute_binding_contract as contract
import attribute_binding_engine as engine
from lmft_lab.runtime_store import atomic_json


def read(path):
    def invalid(value):
        raise ValueError('nonfinite JSON is not permitted')
    return json.loads(Path(path).read_text(encoding='utf-8'), parse_constant=invalid)


def main():
    for name in ('output-checkpoint.json', 'result.json', 'error.json'):
        if Path(name).exists():
            raise ValueError('worker output already exists')
    try:
        request = read('request.json')
        old = read('input-checkpoint.json') if Path('input-checkpoint.json').exists() else None
        state = engine.load_checkpoint(old) if old is not None else None
        loaded = contract.digest(state) if state is not None else None
        state, predictions = engine.transition(request, state)
        atomic_json('output-checkpoint.json', engine.checkpoint(state))
        atomic_json('result.json', {'pid': os.getpid(), 'loaded_digest': loaded,
                                   'state_digest': contract.digest(state), 'predictions': predictions,
                                   'oracle_imported': 'attribute_binding_oracle' in sys.modules
                                   or 'lmft_lab.capacity_fixture' in sys.modules})
        return 0
    except Exception as exc:
        atomic_json('error.json', {'type': type(exc).__name__, 'reason': str(exc)})
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
