"""Fixed public binding contract. No world mapping, outcome oracle or held labels."""
from itertools import permutations, product
import hashlib
import json

VERSION = 'neutral-binding-1'
CHANNELS = ('a', 'b', 'c')
DOMAIN = tuple(product(range(4), repeat=3))
OPS = ('lt', 'le', 'eq', 'ge', 'gt', 'ne')
POLICIES = ('informative', 'no-acquisition', 'noninformative', 'unavailable', 'already-supported')
SOURCE = 'registered-binding-observation-1'
VERIFIER = 'bounded-write-oracle-1'


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':'),
                                    ensure_ascii=False, allow_nan=False).encode()).hexdigest()


def representations():
    return [{'left': left, 'op': op, 'right': right}
            for left, right in permutations(CHANNELS, 2) for op in OPS]


def features_valid(values):
    return (isinstance(values, list) and len(values) == 3
            and all(type(v) is int and 0 <= v <= 3 for v in values))


def observation(identifier, values):
    return {'id': identifier, 'channels': list(values)}


def query_pool(policy):
    rows = [observation(f'q{i:03}', p) for i, p in enumerate(product(range(3), repeat=3))]
    return [r for r in rows if len(set(r['channels'])) == 1] if policy == 'unavailable' else rows


def held_features():
    return [observation(f'h{i:03}', p) for i, p in enumerate(DOMAIN) if 3 in p]


def configuration():
    return {'version': VERSION, 'channels': list(CHANNELS), 'values': [0, 1, 2, 3],
            'representations': representations(), 'query_pool': query_pool('informative'),
            'held_features': held_features(), 'query_budget': 1,
            'class_equivalence': 'identical truth vector on lexicographic complete domain',
            'tie_policy': 'first lexicographic query with maximum positive disagreement',
            'policies': list(POLICIES), 'validation': 'none; evaluation read-only', 'model_calls': 0}


def class_id(vector):
    return 'class-' + digest(vector)

