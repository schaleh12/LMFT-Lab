"""Explicit-relation learner; no oracle, hidden mapping or memory implementation."""
from copy import deepcopy
from functools import lru_cache
import operator
from . import binding_contract as contract

OPERATORS = {name: getattr(operator, name) for name in contract.OPS}


def evaluate(representation, values):
    left = values[contract.CHANNELS.index(representation['left'])]
    right = values[contract.CHANNELS.index(representation['right'])]
    return OPERATORS[representation['op']](left, right)


@lru_cache(maxsize=1)
def catalog():
    grouped = {}
    for rep in contract.representations():
        vector = [evaluate(rep, p) for p in contract.DOMAIN]
        key = contract.class_id(vector)
        entry = grouped.setdefault(key, {'id': key, 'members': [], 'truth_vector': vector})
        assert entry['truth_vector'] == vector
        entry['members'].append(rep)
    return {key: grouped[key] for key in sorted(grouped)}


def analyze(records):
    counterexamples = {}
    for key, entry in catalog().items():
        rep = entry['members'][0]
        counterexamples[key] = [eid for eid, record in sorted(records.items())
                               if evaluate(rep, record['channels']) != record['outcome']]
    return {'survivors': [key for key, refs in counterexamples.items() if not refs],
            'counterexamples': counterexamples}


def choose(survivors, pool, policy):
    rows = []
    for case in pool:
        votes = [evaluate(catalog()[key]['members'][0], case['channels']) for key in survivors]
        yes = sum(votes)
        rows.append({'case': deepcopy(case), 'votes': votes, 'score': yes*(len(votes)-yes)})
    selected = None
    if survivors and policy != 'no-acquisition':
        best = max((r['score'] for r in rows), default=0)
        if policy == 'noninformative':
            selected = next((r['case'] for r in rows if r['score'] == 0), None)
        elif best > 0:
            selected = next(r['case'] for r in rows if r['score'] == best)
    return {'policy': policy, 'scored': rows, 'selected': deepcopy(selected)}


def predict(survivors, case):
    votes = [evaluate(catalog()[key]['members'][0], case['channels']) for key in survivors]
    result = votes[0] if votes and all(v == votes[0] for v in votes) else None
    return {'case': deepcopy(case), 'votes': votes, 'prediction': result,
            'reason': 'unsupported' if not votes else 'ambiguous' if result is None else 'consensus'}
