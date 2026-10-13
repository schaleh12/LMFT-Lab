"""Public fixed contract only: no world assignment or reference device."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys

VERSION = 'context-applicability-1'
FAMILY = ('0', '1', 'c0', 'not c0', 'c1', 'not c1')
CONTEXTS = ((0, 0), (0, 1), (1, 0), (1, 1))
CONTROLLERS = ('primary', 'memory', 'frozen', 'equality', 'replacement')
SCHEDULES = {'P10': ([1, 0], True), 'P11': ([1, 1], True),
             'P00': ([0, 0], True), 'U10': ([1, 0], False)}
SOURCE = 'registered-calibration-1'
SUPPORT_SOURCE = 'registered-measurement-1'
PROTOCOL = 'experiments/CONTEXT_APPLICABILITY_PROTOCOL.md'


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), allow_nan=False)


def digest(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def exact(a, b):
    return canonical(a) == canonical(b)


def bit(value):
    return type(value) is int and value in (0, 1)


def context(value):
    return type(value) is list and len(value) == 2 and all(bit(v) for v in value)


def source_manifest():
    root = Path(__file__).resolve().parents[1]
    paths = list((root / 'experiments').glob('context_applicability_*.py'))
    paths += [root / 'experiments/run_context_applicability.py', root / PROTOCOL,
              root / 'pyproject.toml', root / 'requirements.txt', root / 'requirements-dev.txt']
    paths += list((root / 'src/lmft_lab').glob('*.py'))
    paths += list((root / 'config').rglob('*.json'))
    return {p.relative_to(root).as_posix(): hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(paths)}


def configuration(controller, schedule):
    if controller not in CONTROLLERS or schedule not in SCHEDULES:
        raise ValueError('unknown controller or schedule')
    ctx, available = SCHEDULES[schedule]
    return {'version': VERSION, 'controller': controller, 'schedule': schedule,
            'family': list(FAMILY), 'contexts': list(map(list, CONTEXTS)),
            'initial_context': [0, 0], 'followup_context': deepcopy(ctx),
            'available': available, 'followup_budget': 1, 'python': sys.version,
            'source_manifest': source_manifest()}


def calibration(identifier, ctx, raw, reference, slot):
    return {'version': VERSION, 'evidence_id': identifier, 'scope': 'calibration',
            'context': list(ctx), 'raw': raw, 'reference': reference, 'slot': slot}


def calibration_valid(record):
    return (type(record) is dict and set(record) ==
            {'version', 'evidence_id', 'scope', 'context', 'raw', 'reference', 'slot'}
            and record['version'] == VERSION and type(record['evidence_id']) is str
            and record['evidence_id'] in ('cal-0', 'cal-1')
            and record['scope'] == 'calibration' and context(record['context'])
            and bit(record['raw']) and bit(record['reference'])
            and record['slot'] in ('initial', 'followup'))


def record(identifier, case_id, part, value, scope='evaluation'):
    return {'id': identifier, 'case_id': case_id, 'scope': scope,
            'part': part, 'value': value, 'source': SUPPORT_SOURCE}


def support_view(case):
    """Shared evidence gates; never chooses a mapping or changes learner state."""
    empty = {'first': [], 'second': [], 'within_part': False, 'complete': False,
             'evidence_refs': [], 'ignored_refs': [], 'raw_records': []}
    if (type(case) is not dict or set(case) != {'id', 'scope', 'context', 'records'}
            or type(case['id']) is not str or case['scope'] != 'evaluation'
            or type(case['records']) is not list):
        return {**empty, 'error': 'invalid_support'}
    if not context(case['context']):
        return {**empty, 'error': 'unknown_context'}
    seen = {}; applicable = []; ignored = []
    for item in case['records']:
        if (type(item) is not dict or set(item) != {'id', 'case_id', 'scope', 'part', 'value', 'source'}
                or any(type(item[k]) is not str for k in ('id', 'case_id', 'scope', 'part', 'source'))
                or item['part'] not in ('first', 'second') or not bit(item['value'])
                or item['source'] != SUPPORT_SOURCE):
            return {**empty, 'error': 'invalid_support'}
        if item['id'] in seen and not exact(item, seen[item['id']]):
            return {**empty, 'error': 'conflicting_support_id'}
        if item['id'] in seen:
            continue
        seen[item['id']] = item
        if item['case_id'] != case['id'] or item['scope'] != case['scope']:
            ignored.append(item['id'])
        else:
            applicable.append(item)
    values = {p: sorted({r['value'] for r in applicable if r['part'] == p})
              for p in ('first', 'second')}
    return {**values, 'within_part': any(len(v) > 1 for v in values.values()),
            'complete': all(bool(v) for v in values.values()),
            'evidence_refs': sorted(r['id'] for r in applicable),
            'ignored_refs': sorted(ignored), 'raw_records': deepcopy(case['records']), 'error': None}


def supported_prediction(view, mapping, mapping_status):
    """Declared common sufficiency gate, downstream of independent mapping kernels."""
    reasons = []
    if view['error']:
        reasons.append(view['error'])
    if mapping_status != 'consensus':
        reasons.append(mapping_status)
    if not view['complete']:
        reasons.append('incomplete')
    if view['within_part']:
        reasons.append('within_part_contradiction')
    normalized = sorted({v ^ mapping for v in view['second']}) if mapping is not None else None
    # Cross-part agreement is assessed only between individually consistent parts.
    # A within-part contradiction remains its own unresolved condition.
    cross = (view['first'][0] != normalized[0]
             if normalized is not None and len(view['first']) == len(normalized) == 1 else None)
    if cross:
        reasons.append('cross_part_disagreement')
    value = view['first'][0] if not reasons else None
    return {'prediction': value, 'reasons': reasons, 'normalized_second': normalized,
            'cross_part_disagreement': cross}


def integrity_cases():
    rows = []
    for ci, ctx in enumerate(CONTEXTS):
        for first in (0, 1):
            for second in (0, 1):
                key = f'i{ci}{first}{second}'
                rows.append({'id': key, 'scope': 'evaluation', 'context': list(ctx),
                             'records': [record(key+'a', key, 'first', first),
                                         record(key+'b', key, 'second', second)]})
    return rows


def rename_cases(cases):
    result = deepcopy(cases)
    for i, case in enumerate(result):
        ids = {r['id']: f'r{i:03}-{j}' for j, r in enumerate(case['records'])}
        old = case['id']; case['id'] = f'renamed-{i:03}'
        for item in case['records']:
            item['id'] = ids[item['id']]
            if item['case_id'] == old:
                item['case_id'] = case['id']
    return result
