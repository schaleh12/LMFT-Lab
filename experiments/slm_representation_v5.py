"""Neutral, non-tautological context-anchored proposals for Batch 1 (Protocol 5)."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

from lmft_lab.local_models import strict_json, load_config
from lmft_lab.runtime_store import Store, digest

ROOT = Path(__file__).resolve().parents[1]
KIND = 'slm-representation-interface-5'
SYSTEM = '''Given indexed surface tokens and a target span, output JSON conforming to the schema.
1. Copy the target span exactly into target.
2. If the sentence provides sufficient context to interpret target:
   - Set status to "one_reading".
   - In readings, provide exactly one object with:
     * gloss: an explanatory paraphrase of target's meaning in this context (1..240 chars).
       CRITICAL: Do NOT use the target word or its plurals in gloss. Define or substitute its meaning using other words (e.g., sequence, magnitude, decree, command, arrangement, purchase).
     * context_quote: an exact phrase of 2 or more words from the sentence (outside target) that informs the reading.
   - CRITICAL: context_quote must be an exact quote from the sentence. Do not quote target alone.
3. If surrounding context is insufficient to determine meaning:
   - Set status to "insufficient_context".
   - Set readings to [].
   - Provide 1..2 concise reasons in uncertainties.
Return valid JSON only. /no_think'''


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


def resolve_token_slice(quote, tokens, target):
    """Find the contiguous token slice matching quote, prioritizing proximity to target."""
    text_clean = quote.strip()
    norm_space = re.sub(r'\s+', ' ', text_clean).lower()
    norm_compact = re.sub(r'[\s_]+', '', text_clean).lower()
    target_mid = (target['start'] + target['end']) / 2.0

    candidates = []
    # 1. Exact or whitespace-normalized space-join match
    for i in range(len(tokens)):
        for j in range(i + 1, min(len(tokens) + 1, i + 30)):
            joined = ' '.join(tokens[i:j])
            if joined.lower() == norm_space:
                candidates.append((i, j, joined, abs((i + j) / 2.0 - target_mid)))

    # 2. Compact character match (handles token boundaries like '3 %' vs '3%')
    if not candidates:
        for i in range(len(tokens)):
            for j in range(i + 1, min(len(tokens) + 1, i + 30)):
                joined = ' '.join(tokens[i:j])
                if re.sub(r'[\s_]+', '', joined).lower() == norm_compact:
                    candidates.append((i, j, joined, abs((i + j) / 2.0 - target_mid)))

    if not candidates:
        raise ValueError(f'context_quote not found in source tokens: {repr(quote)}')

    # Choose candidate closest to target
    candidates.sort(key=lambda c: c[3])
    best = candidates[0]
    return {'start': best[0], 'end': best[1], 'quote': best[2]}


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
        exact(reading, {'gloss', 'context_quote'})
        text(reading['gloss'])
        text(reading['context_quote'])

        # Protocol 5: Non-tautological substitution check
        target_quote = source['target']['quote'].lower()
        pattern = rf'\b{re.escape(target_quote)}s?\b'
        if re.search(pattern, reading['gloss'], flags=re.IGNORECASE):
            raise ValueError('gloss tautology: target word repeated in gloss')

        # Deterministically resolve token slice
        anchor = resolve_token_slice(reading['context_quote'], source['tokens'], source['target'])
        target_positions = set(range(source['target']['start'], source['target']['end']))
        anchor_positions = set(range(anchor['start'], anchor['end']))
        if not (anchor_positions - target_positions):
            raise ValueError('context_quote must cover at least one non-target token')
        reading['context_anchor'] = anchor
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
        return {'type': 'object', 'properties': properties, 'required': list(properties.keys()), 'additionalProperties': False}
    target_obj = {'type': 'object', 'properties': {'start': {'type': 'integer', 'minimum': 0},
                                                   'end': {'type': 'integer', 'minimum': 1},
                                                   'quote': {'type': 'string'}},
                  'required': ['start', 'end', 'quote'], 'additionalProperties': False}
    reading_item = obj({'gloss': string, 'context_quote': string})
    return obj({'schema_version': {'type': 'integer', 'enum': [1]},
                'status': {'type': 'string', 'enum': ['one_reading', 'insufficient_context']},
                'target': target_obj,
                'readings': {'type': 'array', 'maxItems': 1, 'items': reading_item},
                'uncertainties': {'type': 'array', 'maxItems': 2, 'items': string}})


def request(source, generation):
    source_valid(source)
    user = json.dumps({'sentence': ' '.join(source['tokens']),
                       'surface_tokens': [{'index': i, 'text': t} for i, t in enumerate(source['tokens'])],
                       'target': source['target']}, ensure_ascii=False)
    system = SYSTEM + '\nSchema: ' + json.dumps(schema(), sort_keys=True)
    return {'messages': [{'role': 'system', 'content': system},
                         {'role': 'user', 'content': user}],
            'temperature': generation['temperature'],
            'max_tokens': generation['max_tokens'],
            'seed': generation['seed'],
            'stream': False,
            'cache_prompt': False,
            'chat_template_kwargs': {'enable_thinking': False},
            'response_format': {'type': 'json_object', 'schema': schema()}}


def record(case_id, source, original_sha256, raw, trace):
    rep = validation_report(raw, source)
    return {'id': case_id,
            'role': trace['role'],
            'model': trace['model'],
            'generation': trace['generation'],
            'request_sha256': trace['request_sha256'],
            'source': source,
            'source_sha256': digest(source),
            'original_record_sha256': original_sha256,
            'trace_sha256': digest(trace),
            'raw': raw,
            'result': rep,
            'lifecycle': 'unverified_proposal' if rep['admissible'] else 'rejected',
            'author': 'local-model'}


def pins():
    files = ['experiments/SLM_REPRESENTATION_INTERFACE_PROTOCOL_V5.md',
             'experiments/slm_representation_v5.py',
             'experiments/run_slm_representation_v5.py',
             'src/lmft_lab/model_assets.py',
             'src/lmft_lab/local_models.py',
             'src/lmft_lab/runtime_store.py',
             'config/local_models.json']
    return {p: hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in files}


def newborn():
    return {'schema_version': 1, 'kind': KIND, 'pins': pins(), 'records': []}


def append(state, value):
    exact(state, {'schema_version', 'kind', 'pins', 'records'})
    if state['schema_version'] != 1 or state['kind'] != KIND or canonical(state['pins']) != canonical(pins()):
        raise ValueError('state kind/pins mismatch')
    exact(value, {'id', 'role', 'model', 'generation', 'request_sha256', 'source',
                  'source_sha256', 'original_record_sha256', 'trace_sha256', 'raw',
                  'result', 'lifecycle', 'author'})
    if any(r['id'] == value['id'] for r in state['records']):
        raise ValueError('duplicate proposal id')
    updated = deepcopy(state)
    updated['records'].append(deepcopy(value))
    return updated


def consumer_views(records):
    """Primary capacity learner and ordinary structured memory have identical read access."""
    primary = {r['id']: {'lifecycle': r['lifecycle'],
                         'result': r['result'],
                         'source_sha256': r['source_sha256'],
                         'raw': r['raw']} for r in records}
    memory = deepcopy(primary)
    return primary, memory


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--state-dir', required=True)
    args = parser.parse_args()
    store = Store(Path(args.state_dir))
    current = store.read()
    p_view, m_view = consumer_views(current['records'])
    hashes = {i: {'primary': digest(p_view[i]), 'ordinary_memory': digest(m_view[i])} for i in p_view}
    print(canonical({'state_sha256': digest(current), 'record_hashes': hashes}))
