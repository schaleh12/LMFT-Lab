"""Coordinator-only synthetic oracle/evaluator. Never imported by learner workers."""
from itertools import permutations, product
import attribute_binding_contract as contract
from lmft_lab.capacity_fixture import execute

MAPPINGS = tuple(permutations(range(3)))  # neutral indices for length, capacity, distractor
PHYSICAL_TRAIN = ((0, 0, 0), (1, 2, 1), (2, 1, 2), (2, 2, 2))


def label(mapping, values):
    return execute(values[mapping[0]], values[mapping[1]])


def training(mapping, supported=False):
    if supported:
        triples = list(product(range(3), repeat=3))
    else:
        triples = []
        for physical in PHYSICAL_TRAIN:
            values = [None]*3
            for index, value in zip(mapping, physical):
                values[index] = value
            triples.append(tuple(values))
        triples.sort()
    return [record(mapping, f't{i:03}', 'training', values) for i, values in enumerate(triples)]


def record(mapping, identifier, split, values):
    return {'version': contract.VERSION, 'id': identifier, 'split': split,
            'channels': list(values), 'outcome': label(mapping, values), 'source': contract.SOURCE}


def verify(mapping, candidate):
    from attribute_binding_engine import valid_record
    if not valid_record(candidate) or candidate['outcome'] is not label(mapping, candidate['channels']):
        return None
    return contract.digest(candidate)


def score(mapping, frozen_predictions):
    labels = {row['case']['id']: label(mapping, row['case']['channels']) for row in frozen_predictions}
    def metrics(rows):
        decided = [r for r in rows if type(r['prediction']) is bool]
        wrong = [r['case']['id'] for r in decided if r['prediction'] != labels[r['case']['id']]]
        return {'total': len(rows), 'decided': len(decided), 'correct': len(decided)-len(wrong),
                'wrong': wrong, 'abstained': [r['case']['id'] for r in rows if r['prediction'] is None],
                'coverage': len(decided)/len(rows) if rows else None,
                'accuracy': (len(decided)-len(wrong))/len(decided) if decided else None}
    equal = [r for r in frozen_predictions if r['case']['channels'][mapping[0]] == r['case']['channels'][mapping[1]]]
    groups = {}
    for row in frozen_predictions:
        values = row['case']['channels']; key = f'{values[mapping[0]]},{values[mapping[1]]}'
        groups.setdefault(key, []).append({'distractor': values[mapping[2]], 'prediction': row['prediction']})
    comparable = {key: rows for key, rows in groups.items() if len(rows) > 1}
    return {'overall': metrics(frozen_predictions), 'equality': metrics(equal),
            'success': metrics([r for r in frozen_predictions if labels[r['case']['id']]]),
            'failure': metrics([r for r in frozen_predictions if not labels[r['case']['id']]]),
            'distractor_groups': groups,
            'distractor_invariant': all(len({r['prediction'] for r in rows}) == 1 for rows in comparable.values()),
            'labels': labels}
