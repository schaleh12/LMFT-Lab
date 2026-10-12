"""Shared bounded action policy; extracted without changing experimental defaults."""
from copy import deepcopy
import json
from . import attention, consistent_attention as circuit, correction as repair
from . import correction_fixture as fixture, contextual
from .runtime_store import digest

DEFS = {
    'r1': ('c1', None, 'c1-a', None, True),
    'r2': ('c4', 'c4-a', None, 'shielded', True),
    'r3': ('c5', None, 'c5-a', None, True),
    'r4': ('c6', None, 'c6-a', None, True),
    'r5': ('c7', None, 'c7-a', None, True),
    'r6': ('c10', 'c10-a', 'c10-b', None, True),
    'r7': ('c12', None, 'c12-a', None, True),
    'r8': ('c9', None, 'c9-a', None, True),
    'r9': ('c1', None, 'c1-a', 'payload_valid', True),
    'r10': ('c3', None, 'c3-a', None, True),
    'r11': ('c4', 'c4-a', None, 'shielded', False),
    'r12': ('c4', None, None, 'shielded', True),
}

SOURCE = 'authored-action-correction-gather-1'

def message(identifier, op, record):
    return {'schema_version': 1, 'id': identifier, 'sender': fixture.AUTHORITY,
            'source': fixture.SOURCE, 'type': 'observation',
            'content': {'text': 'Authored bounded experiment.', 'operation': op, 'record': record}}

def step(state, item):
    from .runtime import advance
    return advance(state, (state['cursor'] + 1, item, None, json.dumps(item)), None)

def proposal(key, cid):
    return next(r for r in fixture.corrections(key) if r['correction_id'] == cid)

def prepare(identifier):
    from .runtime import initial_state, software_manifest
    key, preparation, cid, gather, available = DEFS[identifier]
    state = initial_state('action-' + identifier, True, software_manifest(None, 'fixture'), 'correction-lmft')
    for trial in list(contextual.TRIALS)[:8]:
        state = step(state, message('prior-' + trial, 'outcome', contextual.outcome(trial)))
    for i, record in enumerate(fixture.initial_records(key)):
        if identifier == 'r9' and record['question'] == 'payload_valid':
            continue
        state = step(state, message('initial-' + str(i), 'evidence', record))
    if preparation:
        state = step(state, message('preparation', 'correction', proposal(key, preparation)))
    case = fixture.public_case(key)
    current = state['judgment']
    prediction = repair.predict(current, case)
    current['cases'][key] = {'input': case, 'request': None, 'evaluations': []}
    current['cache'][key] = {'key': repair.cache_key(current, case), 'result': prediction, 'selected': None}
    offers = []
    if cid:
        record = proposal(key, cid)
        # Offer describes operation capability, NEVER replacement truth/value.
        coordinate = {k: record['replacement'].get(k) for k in ('case_id', 'scope', 'question', 'part')}
        offers.append({'id': 'correct-' + cid, 'kind': 'correction', 'field': coordinate['question'],
                       'correction_id': cid, 'target_id': record['target_id'],
                       'expected_digest': record['expected_digest'], 'coordinate': coordinate,
                       'authority': record['authority'], 'payload_sha256': digest(record),
                       'available': True})
    if gather:
        support = prediction['support'][gather]
        parts = [p for p, values in support['part_values'].items() if not values]
        offers.append({'id': 'gather-' + gather, 'kind': 'gather', 'field': gather,
                       'case_id': key, 'scope': case['scope'], 'parts': parts, 'available': available})
    return {'state': state, 'case': case, 'offers': offers}

def preflight(current, case, offer):
    if not offer['available']:
        return 'service unavailable'
    if offer['field'] not in case['decision_questions']:
        return 'irrelevant question'
    status = circuit.support(repair.effective(current), case, offer['field'])
    if status['resolved']:
        return 'already resolved'
    if offer['kind'] == 'gather':
        missing = [p for p, values in status['part_values'].items() if not values]
        if offer['case_id'] != case['case_id'] or offer['scope'] != case['scope']:
            return 'wrong gather scope'
        if not offer['parts'] or offer['parts'] != missing:
            return 'gather must request exactly missing parts'
        return None
    if not status['inconsistent']:
        return 'no inconsistent support to correct'
    permit = current['policy']['permits'].get(offer['correction_id'])
    if not permit or permit['authority'] != offer['authority'] or permit['payload_sha256'] != offer['payload_sha256']:
        return 'no matching operation permit'
    if offer['correction_id'] in current['correction_index']:
        return 'correction ID already used'
    target = current['ledger'].get(offer['target_id'])
    root = current['roots'].get(offer['target_id'])
    if target is None or current['heads'].get(root) != offer['target_id']:
        return 'inactive or missing target'
    if digest(target['record']) != offer['expected_digest']:
        return 'stale target digest'
    if target['record']['case_id'] != case['case_id'] or target['record']['scope'] != case['scope'] or target['record']['question'] != offer['field']:
        return 'target outside requested question scope'
    if any(offer['coordinate'].get(k) != target['record'][k] for k in ('case_id', 'scope', 'question', 'part')):
        return 'wrong correction coordinate'
    return None

def select(current, case, offers, mode):
    view = repair.effective(current)
    view['mode'] = 'consistent-no-clarity' if mode == 'ablated' else 'consistent-full'
    if mode == 'original':
        selected, traces = circuit.select(view, case)  # Unchanged original algorithm, no action filter.
        if selected is None:
            return None, {'questions': traces, 'actions': []}
        availability = next((o['available'] for o in offers if o['kind'] == 'gather' and o['field'] == selected['field']), True)
        action = {'id': 'original-' + selected['id'], 'kind': 'gather', 'field': selected['field'],
                  'case_id': case['case_id'], 'scope': case['scope'],
                  'parts': list(circuit.PARTS[selected['field']]), 'available': availability}
        return action, {'questions': traces, 'actions': [{'offer': action, 'rejection': None, 'policy': 'original unfiltered question request'}]}
    if mode == 'memory':
        question_traces = []
        for candidate in case['candidates']:
            if candidate['field'] not in case['decision_questions']:
                continue
            status = circuit.support(view, case, candidate['field'])
            conflict, _ = attention.appraisal(case, candidate)
            if not conflict:
                continue
            score = max(0., min(1., .25 * (view['weights'][candidate['route']] + .3125
                         - status['coverage'] - int(status['resolved']) + int(status['inconsistent']))))
            question_traces.append({'candidate': candidate, 'support': status, 'score': score})
    else:
        _, question_traces = circuit.select(view, case)
    scores = {row['candidate']['field']: row['score'] for row in question_traces if 'score' in row}
    traces = []; eligible = []
    for offer in offers:
        reason = preflight(current, case, offer)
        if mode == 'gather-only' and offer['kind'] == 'correction':
            reason = 'gather-only control'
        score = scores.get(offer['field'], 0.)
        if reason is None and score <= 0:
            reason = 'no positive question priority'
        traces.append({'offer': deepcopy(offer), 'rejection': reason, 'score': score})
        if reason is None:
            eligible.append((score, offer['id'], offer))
    eligible.sort(key=lambda x: (-x[0], x[1]))
    return (deepcopy(eligible[0][2]) if eligible else None), {'questions': question_traces, 'actions': traces}

def request(bundle, mode):
    state = deepcopy(bundle['state'])
    if 'episode' in state:
        return state  # Pending and closed episodes retain their original spent budget.
    original = digest(state)
    selected, traces = select(state['judgment'], bundle['case'], bundle['offers'], mode)
    if digest(state) != original:
        raise AssertionError('selection mutated state')
    state['episode'] = {'selected': selected, 'trace': traces, 'charged': int(selected is not None),
                        'status': 'pending' if selected else 'closed', 'reply_digest': None}
    if selected:
        state['questions']['action-request'] = {'case_id': bundle['case']['case_id'],
            'question': selected['field'], 'status': 'open', 'closed_by': None}
    return state

def service_reply(selected):
    if selected['kind'] == 'correction':
        return proposal(selected['coordinate']['case_id'], selected['correction_id'])
    if not selected['available']:
        return {'unavailable': True}
    return {'records': [{'evidence_id': 'gather/' + selected['case_id'] + '/' + selected['field'] + '/' + part,
        'case_id': selected['case_id'], 'scope': selected['scope'], 'question': selected['field'],
        'part': part, 'value': True, 'source': SOURCE} for part in selected['parts']]}

def receive(state, case, reply, sender=fixture.AUTHORITY, *, message_id='action-reply'):
    changed = deepcopy(state); episode = changed['episode']; selected = episode['selected']
    if episode['status'] != 'pending':
        return changed, {'status': 'duplicate_reply' if episode['reply_digest'] == digest(reply) else 'closed_episode'}
    receipt = {}
    if selected['kind'] == 'correction':
        # Correlate the selected operation before delegating all substantive checks.
        if reply.get('correction_id') != selected['correction_id'] or reply.get('target_id') != selected['target_id']:
            receipt['status'] = 'uncorrelated_reply'
        else:
            item = message(message_id, 'correction', reply); item['sender'] = sender
            repair.correct(changed, item, receipt)
    elif not selected['available']:
        receipt.update(status='gather_unavailable', verification_checked=False)
    elif sender != fixture.AUTHORITY or digest(reply) != digest(service_reply(selected)):
        receipt['status'] = 'unverified_gather_reply'
    else:
        current = changed['judgment']
        for record in reply['records']:
            eid = record['evidence_id']
            if eid in current['ledger']:
                raise ValueError('gather identity collision')
            current['ledger'][eid] = {'record': deepcopy(record), 'source': SOURCE,
                'verification': 'exact authored selected-coordinate reference', 'root': eid, 'parent': None}
            current['roots'][eid] = eid; current['heads'][eid] = eid
        current['cache'].pop(case['case_id'], None)
        question = changed['questions']['action-request']
        if circuit.support(repair.effective(current), case, selected['field'])['resolved']:
            question.update(status='resolved_by_gather', closed_by=message_id)
        receipt.update(status='gather_accepted', verification_checked=True)
    episode.update(status='closed', reply_digest=digest(reply), receipt=receipt)
    return changed, receipt

def semantic(state):
    current = state['judgment']
    return {'effective': repair.effective_ref(current), 'cache': current['cache'], 'questions': state['questions']}
