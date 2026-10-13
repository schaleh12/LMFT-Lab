"""Neutral, non-tautological context-anchored proposals for Batch 2 (Protocol 6)."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))

from lmft_lab.local_models import strict_json, load_config
from lmft_lab.runtime_store import Store, digest
KIND = 'slm-representation-interface-6'
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
    """Deterministically resolves the contiguous token slice [start:end] in tokens matching quote."""
    if not isinstance(quote, str) or not quote.strip():
        raise ValueError('nonempty context_quote required')

    clean_quote = quote.strip()
    norm_compact = re.sub(r'[\s_]+', '', clean_quote).lower()

    target_mid = (target['start'] + target['end']) / 2.0
    candidates = []

    # First attempt: exact substring match in joined tokens
    for i in range(len(tokens)):
        for j in range(i + 1, len(tokens) + 1):
            joined = ' '.join(tokens[i:j])
            if clean_quote in joined or joined in clean_quote:
                if re.sub(r'[\s_]+', '', joined).lower() == norm_compact:
                    candidates.append((i, j, joined, abs((i + j) / 2.0 - target_mid)))

    if not candidates:
        # Second attempt: relaxed character matching across token spans
        for i in range(len(tokens)):
            for j in range(i + 1, min(i + 25, len(tokens) + 1)):
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

        # Protocol 6: Non-tautological substitution check
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
    except Exception as e:
        return {'admissible': False, 'proposal': None, 'errors': [f'{type(e).__name__}: {e}']}


def schema():
    return {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object",
        "additionalProperties": False,
        "required": ["schema_version", "status", "target", "readings", "uncertainties"],
        "properties": {
            "schema_version": {"type": "integer", "const": 1},
            "status": {"type": "string", "enum": ["one_reading", "insufficient_context"]},
            "target": {
                "type": "object",
                "additionalProperties": False,
                "required": ["start", "end", "quote"],
                "properties": {
                    "start": {"type": "integer", "minimum": 0},
                    "end": {"type": "integer", "minimum": 1},
                    "quote": {"type": "string", "minLength": 1, "maxLength": 240}
                }
            },
            "readings": {
                "type": "array",
                "maxItems": 1,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["gloss", "context_quote"],
                    "properties": {
                        "gloss": {"type": "string", "minLength": 1, "maxLength": 240},
                        "context_quote": {"type": "string", "minLength": 1, "maxLength": 240}
                    }
                }
            },
            "uncertainties": {
                "type": "array",
                "maxItems": 2,
                "items": {"type": "string", "minLength": 1, "maxLength": 240}
            }
        }
    }


def user_prompt(source):
    source_valid(source)
    toks = ' '.join(f'[{i}:{t}]' for i, t in enumerate(source['tokens']))
    tgt = source['target']
    return (f'Tokens: {toks}\n'
            f'Target span: [{tgt["start"]}:{tgt["end"]}] "{tgt["quote"]}"\n'
            f'Output the single reading JSON (remember: gloss must NOT use "{tgt["quote"]}" or its plurals; context_quote must be an exact quote from Tokens).')


def request(source, generation):
    return {
        'messages': [{'role': 'system', 'content': SYSTEM},
                     {'role': 'user', 'content': user_prompt(source)}],
        'response_format': {'type': 'json_schema', 'json_schema': {'name': 'proposal', 'schema': schema(), 'strict': True}},
        **generation
    }


def record(case_id, source, original_sha256, raw, trace):
    source_valid(source)
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
    files = ['experiments/SLM_REPRESENTATION_INTERFACE_PROTOCOL_V6.md',
             'experiments/slm_representation_v6.py',
             'experiments/run_slm_representation_v6.py',
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
