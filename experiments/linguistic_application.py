"""Experiment-local supervised cue revisions; no protected seed or model access."""
from collections import Counter, defaultdict
from copy import deepcopy
from itertools import combinations
import hashlib
import json
from pathlib import Path
import re

from lmft_lab.runtime_store import digest

KIND = 'linguistic-application-1'
CONTROLLERS = ('primary', 'memory', 'frozen', 'majority')
EXAMPLE_KEYS = {'id', 'document_id', 'tokens', 'target_indices', 'sense', 'provenance'}


def exact(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError('unexpected fields/type')


def nonempty(value):
    if type(value) is not str or not value.strip():
        raise ValueError('expected nonempty string')


def surface(item):
    tokens, indices = item['tokens'], item['target_indices']
    if (type(tokens) is not list or not tokens or
            any(type(t) is not str or not t.strip() for t in tokens)):
        raise ValueError('invalid surface tokens')
    if (type(indices) is not list or not indices or
            any(type(i) is not int or not 0 <= i < len(tokens) for i in indices) or
            indices != sorted(set(indices))):
        raise ValueError('invalid target indices')


def features(item):
    surface(item)
    return frozenset(t for i, word in enumerate(item['tokens'])
                     if i not in item['target_indices']
                     for t in re.findall('[a-z]+', word.lower())
                     if t not in {'order', 'orders'})


def validate_example(item):
    exact(item, EXAMPLE_KEYS)
    for key in ('id', 'document_id', 'sense'):
        nonempty(item[key])
    surface(item)
    exact(item['provenance'], {'source', 'locator', 'source_sha256'})
    for v in item['provenance'].values():
        nonempty(v)
    if not re.fullmatch('[0-9a-f]{64}', item['provenance']['source_sha256']):
        raise ValueError('invalid provenance hash')


def cue_id(sense, cue):
    return digest({'sense': sense, 'cue': list(cue)})


def primary_table(examples):
    """Inverted feature index, then label partition of every cue's witnesses."""
    index = defaultdict(list)
    for e in examples:
        words = sorted(features(e))
        for cue in [(w,) for w in words] + list(combinations(words, 2)):
            index[cue].append(e)
    result = {}
    for sense in sorted({e['sense'] for e in examples}):
        rules = []
        for cue, matches in sorted(index.items()):
            positive = [e for e in matches if e['sense'] == sense]
            if not positive:
                continue
            negative = [e for e in matches if e['sense'] != sense]
            documents = sorted({e['document_id'] for e in positive})
            reasons = []
            if negative:
                reasons.append('counterexample')
            if len(documents) < 2:
                reasons.append('insufficient_documents')
            rules.append({'id': cue_id(sense, cue), 'cue': list(cue),
                          'positive': sorted(e['id'] for e in positive),
                          'negative': sorted(e['id'] for e in negative),
                          'positive_documents': documents,
                          'status': 'rejected' if reasons else 'active',
                          'reasons': reasons})
        result[sense] = {'lifecycle': 'active' if any(r['status'] == 'active' for r in rules)
                         else 'unsupported', 'rules': rules}
    return result


def revised(table, previous, number):
    """Annotate lifecycle history without deleting rejected candidates."""
    result = deepcopy(table)
    for sense, interpretation in result.items():
        prior = {r['id']: r for r in previous.get(sense, {}).get('rules', [])}
        interpretation['version'] = number
        interpretation['supplied_sense'] = sense
        for rule in interpretation['rules']:
            old = prior.get(rule['id'])
            before = old['status'] if old else None
            if before in ('active', 'invalidated') and rule['status'] == 'rejected':
                rule['status'] = 'invalidated'
            if before == 'invalidated' and rule['status'] == 'active':
                raise ValueError('invalidated rule resurrection')
            rule['previous_status'] = before
            rule['transition'] = 'created' if before is None else (
                'retained' if before == rule['status'] else 'changed')
    return result


def pins():
    root = Path(__file__).resolve().parents[1]
    names = ['experiments/LINGUISTIC_APPLICATION_PROTOCOL.md',
             'experiments/LINGUISTIC_APPLICATION_DATA_BINDING.json',
             'experiments/linguistic_application.py',
             'experiments/linguistic_application_memory.py',
             'experiments/linguistic_application_worker.py',
             'experiments/linguistic_application_development.py',
             'src/lmft_lab/runtime_store.py', 'src/lmft_lab/local_models.py',
             'pyproject.toml', 'requirements.txt', 'requirements-dev.txt']
    return {name: hashlib.sha256((root / name).read_bytes()).hexdigest() for name in names}


def newborn(split_id):
    nonempty(split_id)
    return {'schema_version': 1, 'kind': KIND, 'pins': pins(), 'split_id': split_id,
            'stage': 0, 'examples': [], 'batches': [], 'revisions': []}


def advance(state, request):
    """All input validation precedes return; caller commits only a successful copy."""
    exact(request, {'split_id', 'batch', 'examples'})
    if request['split_id'] != state['split_id']:
        raise ValueError('split identity mismatch')
    batch = request['batch']
    if type(batch) is not int or batch not in (1, 2):
        raise ValueError('invalid batch')
    if batch <= state['stage']:
        if digest(request) == state['batches'][batch - 1]['request_digest']:
            return deepcopy(state)
        raise ValueError('conflicting batch replay')
    if batch != state['stage'] + 1:
        raise ValueError('out-of-order batch')
    if type(request['examples']) is not list or not request['examples']:
        raise ValueError('empty/invalid batch')
    records = {e['id']: e for e in state['examples']}
    locations = {(e['provenance']['source'], e['provenance']['locator']): e
                 for e in state['examples']}
    old_docs = {e['document_id'] for e in state['examples']}
    added, duplicates = [], []
    for e in request['examples']:
        validate_example(e)
        if e['id'] in records:
            if e != records[e['id']]:
                raise ValueError('conflicting example ID')
            duplicates.append(e['id'])
            continue
        location = (e['provenance']['source'], e['provenance']['locator'])
        if location in locations:
            raise ValueError('conflicting provenance locator')
        if e['document_id'] in old_docs:
            raise ValueError('document reused across batches')
        records[e['id']] = e
        locations[location] = e
        added.append(deepcopy(e))
    if not added:
        raise ValueError('batch contains no new examples')
    new = deepcopy(state)
    new['examples'].extend(added)
    previous = new['revisions'][-1] if new['revisions'] else {'primary': {}, 'memory': {}}
    from linguistic_application_memory import memory_table
    p = primary_table(new['examples'])
    m = memory_table(new['examples'])
    if p != m:
        raise ValueError('independent memory parity failure')
    new['revisions'].append({'version': batch, 'evidence_ids': [e['id'] for e in new['examples']],
                             'primary': revised(p, previous['primary'], batch),
                             'memory': revised(m, previous['memory'], batch)})
    new['stage'] = batch
    new['batches'].append({'batch': batch, 'request_digest': digest(request),
                           'added_ids': [e['id'] for e in added], 'duplicates': duplicates,
                           'request': deepcopy(request)})
    return new


def validate(state):
    exact(state, {'schema_version', 'kind', 'pins', 'split_id', 'stage', 'examples',
                  'batches', 'revisions'})
    if (type(state['schema_version']) is not int or state['schema_version'] != 1
            or state['kind'] != KIND or state['pins'] != pins()):
        raise ValueError('source/protocol/schema pin mismatch')
    if type(state['stage']) is not int or state['stage'] not in (0, 1, 2):
        raise ValueError('invalid stage')
    if type(state['batches']) is not list or len(state['batches']) != state['stage']:
        raise ValueError('invalid history')
    rebuilt = newborn(state['split_id'])
    for batch in state['batches']:
        rebuilt = advance(rebuilt, batch['request'])
    # JSON distinguishes true/1/1.0, unlike Python container equality. Compare the
    # entire persisted reconstruction, including cached nested records and history.
    if (json.dumps(rebuilt, sort_keys=True, allow_nan=False) !=
            json.dumps(state, sort_keys=True, allow_nan=False)):
        raise ValueError('checkpoint evidence/history inconsistency')


def apply_table(table, words):
    matching = {sense: [r['id'] for r in interp['rules']
                        if r['status'] == 'active' and set(r['cue']) <= words]
                for sense, interp in table.items()}
    matching = {sense: ids for sense, ids in matching.items() if ids}
    labels = sorted(matching)
    return {'labels': labels, 'status': 'abstain' if not labels else (
        'single' if len(labels) == 1 else 'ambiguous'),
        'selected': labels[0] if len(labels) == 1 else None, 'matched_rules': matching}


def predict(state, items):
    if type(items) is not list:
        raise ValueError('invalid items')
    ids = set()
    for item in items:
        exact(item, {'id', 'tokens', 'target_indices'})
        nonempty(item['id'])
        surface(item)
        if item['id'] in ids:
            raise ValueError('duplicate application ID')
        ids.add(item['id'])
    counts = Counter(e['sense'] for e in state['examples'])
    majority = min(counts, key=lambda s: (-counts[s], s)) if counts else None
    latest = state['revisions'][-1] if state['revisions'] else {'primary': {}, 'memory': {}}
    frozen = state['revisions'][0]['primary'] if state['revisions'] else {}
    result = []
    for item in items:
        words = features(item)
        outputs = {name: apply_table(table, words) for name, table in (
            ('primary', latest['primary']), ('memory', latest['memory']), ('frozen', frozen))}
        outputs['majority'] = {'labels': [majority] if majority else [],
                               'status': 'single' if majority else 'abstain',
                               'selected': majority, 'matched_rules': {}}
        result.append({'id': item['id'], 'controllers': outputs})
    return result


def score(predictions, gold):
    """Separate scorer: never called by worker application or learning."""
    if set(gold) != {row['id'] for row in predictions} or len(predictions) != len(gold):
        raise ValueError('prediction/gold identity mismatch')
    result = {}
    for controller in CONTROLLERS:
        def tally(rows):
            d = dict.fromkeys(('n', 'strict_correct', 'singleton', 'singleton_wrong',
                              'abstain', 'ambiguous', 'ambiguous_gold_included',
                              'wrong_inclusions', 'exclusions'), 0)
            for row in rows:
                labels = row['controllers'][controller]['labels']
                target = gold[row['id']]
                d['n'] += 1
                d['strict_correct'] += labels == [target]
                d['singleton'] += len(labels) == 1
                d['singleton_wrong'] += len(labels) == 1 and labels != [target]
                d['abstain'] += not labels
                d['ambiguous'] += len(labels) > 1
                d['ambiguous_gold_included'] += len(labels) > 1 and target in labels
                d['wrong_inclusions'] += len(set(labels) - {target})
                d['exclusions'] += target not in labels
            d['singleton_coverage'] = d['singleton'] / d['n'] if d['n'] else None
            return d
        result[controller] = {'overall': tally(predictions), 'per_sense': {
            sense: tally([r for r in predictions if gold[r['id']] == sense])
            for sense in sorted(set(gold.values()))}}
    return result
