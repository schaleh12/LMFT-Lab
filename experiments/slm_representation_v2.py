"""Neutral, singular context-anchored UNVERIFIED proposals shared by two consumers (Protocol 2)."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path

from lmft_lab.local_models import strict_json, load_config
from lmft_lab.runtime_store import Store, digest

ROOT = Path(__file__).resolve().parents[1]
KIND = 'slm-representation-interface-2'
SYSTEM = '''Given indexed surface tokens and a target span, output JSON conforming to the schema.
1. Copy the target span exactly into target.
2. If the sentence provides sufficient context to interpret target:
   - Set status to "one_reading".
   - In readings, provide exactly one object with:
     * gloss: a concise target-relative reading (1..240 chars).
     * context_anchor: a token span (start, end, quote) identifying surrounding words that inform the reading.
   - CRITICAL: context_anchor must include tokens outside the target. Never set context_anchor equal to target.
3. If surrounding context is insufficient to determine meaning:
   - Set status to "insufficient_context".
   - Set readings to [].
   - Provide 1..2 concise reasons in uncertainties.
Token spans are zero-based (start inclusive, end exclusive). quote must be the exact space-joined tokens. /no_think'''


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def exact(value, keys):
    if type(value) is not dict or set(value) != set(keys):
        raise ValueError('unexpected fields/type')


def text(value):
    if type(value) is not str or not value.strip() or len(value) > 240:
        raise ValueError('invalid concise text')


def span(value, tokens):
    exact(value, {'start', 'end', 'quote'})
    start, end = value['start'], value['end']
    if type(start) is not int or type(end) is not int or not 0 <= start < end <= len(tokens):
        raise ValueError('invalid token span')
    if type(value['quote']) is not str or value['quote'] != ' '.join(tokens[start:end]):
        raise ValueError('source quotation mismatch')


def source_valid(source):
    exact(source, {'tokens', 'target'})
    if (type(source['tokens']) is not list or not source['tokens'] or
            any(type(t) is not str or not t.strip() for t in source['tokens'])):
        raise ValueError('invalid source tokens')
    span(source['target'], source['tokens'])


def validate(raw, source):
    source_valid(source)
    p = strict_json(raw)
    exact(p, {'schema_version', 'status', 'target', 'readings', 'uncertainties'})
    if type(p['schema_version']) is not int or p['schema_version'] != 1:
        raise ValueError('invalid schema version')
    span(p['target'], source['tokens'])
    if canonical(p['target']) != canonical(source['target']):
        raise ValueError('target mismatch')
    counts = {'one_reading': 1, 'insufficient_context': 0}
    if type(p['status']) is not str or p['status'] not in counts:
        raise ValueError('invalid proposal status')
    if type(p['readings']) is not list or len(p['readings']) != counts[p['status']]:
        raise ValueError('status/reading count mismatch')
    if type(p['uncertainties']) is not list or len(p['uncertainties']) > 2:
        raise ValueError('invalid uncertainties')
    if p['status'] == 'insufficient_context':
        if not (1 <= len(p['uncertainties']) <= 2):
            raise ValueError('insufficient context needs 1..2 uncertainties')
        for value in p['uncertainties']:
            text(value)
    elif p['status'] == 'one_reading':
        if len(p['uncertainties']) != 0:
            raise ValueError('one_reading requires empty uncertainties')
        reading = p['readings'][0]
        exact(reading, {'gloss', 'context_anchor'})
        text(reading['gloss'])
        span(reading['context_anchor'], source['tokens'])
        target_positions = set(range(source['target']['start'], source['target']['end']))
        anchor_positions = set(range(reading['context_anchor']['start'], reading['context_anchor']['end']))
        if not (anchor_positions - target_positions):
            raise ValueError('reading requires a non-target context anchor')
    return p


def validation_report(raw, source):
    """Return rejection as data: no repair/retry, no transport server restart."""
    try:
        return {'admissible': True, 'proposal': validate(raw, source), 'errors': []}
    except (ValueError, TypeError, KeyError) as exc:
        return {'admissible': False, 'proposal': None, 'errors': [str(exc)]}


def schema():
    string = {'type': 'string', 'minLength': 1, 'maxLength': 240}
    def obj(properties):
        return {'type': 'object', 'additionalProperties': False,
                'required': list(properties), 'properties': properties}
    anchor = obj({'start': {'type': 'integer', 'minimum': 0},
                  'end': {'type': 'integer', 'minimum': 1}, 'quote': {'type': 'string'}})
    reading = obj({'gloss': string, 'context_anchor': anchor})
    return obj({'schema_version': {'type': 'integer', 'enum': [1]},
                'status': {'type': 'string', 'enum': ['one_reading', 'insufficient_context']},
                'target': anchor,
                'readings': {'type': 'array', 'maxItems': 1, 'items': reading},
                'uncertainties': {'type': 'array', 'maxItems': 2, 'items': string}})


def request(source, generation):
    source_valid(source)
    user = {'surface_tokens': [{'index': i, 'text': t} for i, t in enumerate(source['tokens'])],
            'target': source['target']}
    return {'messages': [{'role': 'system', 'content': SYSTEM + '\nSchema: ' + canonical(schema())},
                         {'role': 'user', 'content': canonical(user)}],
            'temperature': generation['temperature'], 'seed': generation['seed'],
            'max_tokens': generation['max_tokens'], 'stream': False, 'cache_prompt': False,
            'chat_template_kwargs': {'enable_thinking': False},
            'response_format': {'type': 'json_object', 'schema': schema()}}


def pins():
    names = ['experiments/SLM_REPRESENTATION_INTERFACE_PROTOCOL_V2.md',
             'experiments/slm_representation_v2.py', 'experiments/run_slm_representation_v2.py',
             'config/local_models.json', 'src/lmft_lab/local_models.py',
             'src/lmft_lab/model_assets.py', 'src/lmft_lab/runtime_store.py']
    return {n: hashlib.sha256((ROOT/n).read_bytes()).hexdigest() for n in names}


def record(identifier, source, original_hash, raw, trace):
    result = validation_report(raw, source)
    return {'id': identifier, 'source': deepcopy(source), 'source_sha256': digest(source),
            'original_record_sha256': original_hash, 'raw': raw, 'result': result,
            'lifecycle': 'unverified_proposal' if result['admissible'] else 'rejected',
            'author': 'local-model', 'model': deepcopy(trace['model']),
            'generation': deepcopy(trace['generation']), 'role': trace['role'],
            'request_sha256': trace['request_sha256'], 'trace_sha256': digest(trace)}


def validate_record(r):
    exact(r, {'id', 'source', 'source_sha256', 'original_record_sha256', 'raw', 'result',
              'lifecycle', 'author', 'model', 'generation', 'role', 'request_sha256', 'trace_sha256'})
    if type(r['id']) is not str or not r['id'] or type(r['raw']) is not str:
        raise ValueError('invalid record identity/raw')
    source_valid(r['source'])
    if r['source_sha256'] != digest(r['source']):
        raise ValueError('changed source reference')
    for key in ('source_sha256', 'original_record_sha256', 'request_sha256', 'trace_sha256'):
        if type(r[key]) is not str or len(r[key]) != 64 or any(c not in '0123456789abcdef' for c in r[key]):
            raise ValueError('invalid hash')
    config = load_config(ROOT/'config/local_models.json')
    if (r['author'] != 'local-model' or r['role'] != 'interpretation' or
            canonical(r['model']) != canonical(config['models'][config['roles']['interpretation']]) or
            canonical(r['generation']) != canonical(config['generation'])):
        raise ValueError('model provenance mismatch')
    expected_request = request(r['source'], config['generation'])
    h = hashlib.sha256(json.dumps(expected_request, sort_keys=True).encode()).hexdigest()
    if r['request_sha256'] != h:
        raise ValueError('request/source provenance mismatch')
    expected = validation_report(r['raw'], r['source'])
    if canonical(r['result']) != canonical(expected):
        raise ValueError('cached validation mismatch')
    if r['lifecycle'] != ('unverified_proposal' if expected['admissible'] else 'rejected'):
        raise ValueError('invalid lifecycle')


def newborn():
    return {'schema_version': 1, 'kind': KIND, 'pins': pins(), 'records': []}


def append(state, value):
    validate_record(value)
    for old in state['records']:
        if old['id'] == value['id']:
            if canonical(old) != canonical(value):
                raise ValueError('conflicting record ID')
            return deepcopy(state)
    updated = deepcopy(state)
    updated['records'].append(deepcopy(value))
    return updated


def validate_state(state):
    exact(state, {'schema_version', 'kind', 'pins', 'records'})
    if (type(state['schema_version']) is not int or state['schema_version'] != 1 or
            state['kind'] != KIND or canonical(state['pins']) != canonical(pins()) or
            type(state['records']) is not list):
        raise ValueError('state schema/pin mismatch')
    seen = set()
    for r in state['records']:
        validate_record(r)
        if r['id'] in seen:
            raise ValueError('duplicate persisted ID')
        seen.add(r['id'])


def retrieve(state, identifier, consumer):
    if consumer not in ('primary', 'ordinary_memory'):
        raise ValueError('unknown consumer')
    validate_state(state)
    return deepcopy(next(r for r in state['records'] if r['id'] == identifier))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--state-dir', required=True)
    args = parser.parse_args()
    state = Store(args.state_dir).read()
    validate_state(state)
    print(canonical({'state_sha256': digest(state), 'record_hashes': {
        r['id']: {consumer: digest(retrieve(state, r['id'], consumer))
                  for consumer in ('primary', 'ordinary_memory')} for r in state['records']}}))
