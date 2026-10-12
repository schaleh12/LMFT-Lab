"""Independent ordinary-memory learner using truth-table masks, not relation calls."""
from copy import deepcopy
from functools import lru_cache
from . import binding_contract as contract

# Comparison signs, deliberately independent of operator functions in primary.
SIGNS = {'lt': {-1}, 'le': {-1, 0}, 'eq': {0}, 'ge': {0, 1}, 'gt': {1}, 'ne': {-1, 1}}


def address(values):
    return values[0]*16 + values[1]*4 + values[2]


@lru_cache(maxsize=1)
def tables():
    groups = {}
    for rep in contract.representations():
        mask = 0
        i, j = contract.CHANNELS.index(rep['left']), contract.CHANNELS.index(rep['right'])
        for a in range(4):
            for b in range(4):
                for c in range(4):
                    values = (a, b, c)
                    difference = values[i] - values[j]
                    sign = (difference > 0) - (difference < 0)
                    if sign in SIGNS[rep['op']]:
                        mask |= 1 << address(values)
        groups.setdefault(mask, []).append(rep)
    result = {}
    for mask, members in groups.items():
        vector = [bool(mask & (1 << index)) for index in range(64)]
        key = contract.class_id(vector)
        result[key] = {'mask': mask, 'members': members, 'vector': vector}
    return {key: result[key] for key in sorted(result)}


def catalog():
    return {key: {'id': key, 'members': deepcopy(row['members']), 'truth_vector': list(row['vector'])}
            for key, row in tables().items()}


def analyze(records):
    positive, negative = 0, 0
    indexed = {}
    for eid in sorted(records):
        record = records[eid]
        bit = 1 << address(record['channels'])
        indexed[eid] = (bit, record['outcome'])
        if record['outcome']:
            positive |= bit
        else:
            negative |= bit
    survivors, counterexamples = [], {}
    for key, row in tables().items():
        mask = row['mask']
        if mask & positive == positive and mask & negative == 0:
            survivors.append(key)
        counterexamples[key] = [eid for eid, (bit, value) in indexed.items() if bool(mask & bit) != value]
    return {'survivors': survivors, 'counterexamples': counterexamples}


def choose(survivors, pool, policy):
    rows, selected, maximum = [], None, 0
    for point in pool:
        bit = 1 << address(point['channels'])
        votes = [bool(tables()[key]['mask'] & bit) for key in survivors]
        positives = votes.count(True)
        score = positives*votes.count(False)
        rows.append({'case': deepcopy(point), 'votes': votes, 'score': score})
        if score > maximum:
            maximum, selected = score, deepcopy(point)
    if not survivors or policy == 'no-acquisition':
        selected = None
    elif policy == 'noninformative':
        selected = None
        for row in rows:
            if row['score'] == 0:
                selected = deepcopy(row['case']); break
    return {'policy': policy, 'scored': rows, 'selected': selected}


def predict(survivors, case):
    bit = 1 << address(case['channels'])
    votes = [bool(tables()[key]['mask'] & bit) for key in survivors]
    yes, no = votes.count(True), votes.count(False)
    prediction = True if yes and not no else False if no and not yes else None
    return {'case': deepcopy(case), 'votes': votes, 'prediction': prediction,
            'reason': 'unsupported' if not survivors else 'ambiguous' if yes and no else 'consensus'}
