"""Shared strict admission/lifecycle; learning decisions belong to separate kernels."""
from copy import deepcopy
import re
import attribute_binding_contract as contract
import attribute_binding_primary as primary
import attribute_binding_memory as memory

KERNELS = {'primary': primary, 'memory': memory}
RECORD_KEYS = {'version', 'id', 'split', 'channels', 'outcome', 'source'}


def records(state):
    return {eid: entry['record'] for eid, entry in state['evidence'].items()}


def new(implementation, policy):
    if implementation not in KERNELS or policy not in contract.POLICIES:
        raise ValueError('unknown implementation or policy')
    kernel = KERNELS[implementation]
    return {'version': contract.VERSION, 'implementation': implementation, 'policy': policy,
            'phase': 'training', 'evidence': {}, 'analysis': kernel.analyze({}),
            'query': None, 'budget_spent': 0, 'events': [],
            'candidate_digest': contract.digest(kernel.catalog())}


def valid_record(record):
    return (isinstance(record, dict) and set(record) == RECORD_KEYS
            and record['version'] == contract.VERSION
            and isinstance(record['id'], str) and bool(re.fullmatch(r'[tq]\d{3}', record['id']))
            and record['split'] in ('training', 'acquisition')
            and record['id'].startswith('t' if record['split'] == 'training' else 'q')
            and contract.features_valid(record['channels']) and type(record['outcome']) is bool
            and record['source'] == contract.SOURCE)


def admit(state, record, verified_digest):
    def finish(status, reason):
        state['events'].append({'operation': 'admit', 'status': status, 'reason': reason,
                                'record': deepcopy(record), 'verification_digest': verified_digest})
        return status
    if not valid_record(record):
        return finish('rejected', 'invalid evidence schema/source')
    if 3 in record['channels']:
        return finish('rejected', 'held-out features cannot enter admission')
    eid = record['id']
    old = state['evidence'].get(eid)
    if old:
        if contract.digest(old['record']) != contract.digest(record):
            return finish('rejected', 'conflicting evidence identity')
        return finish('duplicate', 'same admitted evidence; no additional learning or budget')
    if verified_digest != contract.digest(record):
        return finish('rejected', 'no matching trusted verification receipt')
    expected_phase = 'training' if record['split'] == 'training' else 'pending'
    if state['phase'] != expected_phase:
        return finish('rejected', 'evidence phase is closed or ineligible')
    if record['split'] == 'acquisition':
        selected = state['query']['selected']
        if selected is None or state['budget_spent'] != 1:
            return finish('rejected', 'no selected charged request')
        if eid != selected['id'] or record['channels'] != selected['channels']:
            return finish('rejected', 'not the selected query')
        if any(e['record']['split'] == 'acquisition' for e in state['evidence'].values()):
            return finish('rejected', 'one acquisition already admitted')
    state['evidence'][eid] = {'record': deepcopy(record),
                            'verification': {'verifier': contract.VERIFIER, 'digest': verified_digest}}
    before = list(state['analysis']['survivors'])
    state['analysis'] = KERNELS[state['implementation']].analyze(records(state))
    status = finish('accepted', 'independently verified observation in permitted phase')
    state['events'][-1].update(before=before, after=list(state['analysis']['survivors']))
    return status


def select(state):
    count = 27 if state['policy'] == 'already-supported' else 4
    if state['phase'] != 'training' or set(state['evidence']) != {f't{i:03}' for i in range(count)}:
        raise ValueError('complete training required; selection cannot repeat')
    kernel = KERNELS[state['implementation']]
    state['query'] = kernel.choose(state['analysis']['survivors'], contract.query_pool(state['policy']), state['policy'])
    state['budget_spent'] = int(state['query']['selected'] is not None)
    state['phase'] = 'pending'


def finish_acquisition(state):
    if state['phase'] != 'pending':
        raise ValueError('acquisition already closed')
    count = sum(e['record']['split'] == 'acquisition' for e in state['evidence'].values())
    if count != state['budget_spent']:
        raise ValueError('selected query requires its verified observation before closure')
    state['phase'] = 'evaluation'


def predictions(state):
    kernel = KERNELS[state['implementation']]
    return [kernel.predict(state['analysis']['survivors'], case) for case in contract.held_features()]


def transition(request, state=None):
    if not isinstance(request, dict) or set(request) != {'stage', 'implementation', 'policy', 'items'}:
        raise ValueError('invalid public request fields')
    stage = request['stage']
    if stage not in ('training', 'acquisition', 'evaluate'):
        raise ValueError('invalid stage')
    if not isinstance(request['items'], list) or any(
        not isinstance(item, dict) or set(item) != {'record', 'verified_digest'}
        or (item['verified_digest'] is not None and not isinstance(item['verified_digest'], str))
        for item in request['items']):
        raise ValueError('invalid admission items')
    # Keep hidden labels/mappings out of the actual serialized worker boundary,
    # including rejected-record metadata; ordinary malformed VALUE tests still
    # produce the intended inspectable rejection receipt.
    if any(isinstance(item['record'], dict) and set(item['record']) - RECORD_KEYS
           for item in request['items']):
        raise ValueError('invalid public evidence fields')
    if stage == 'training':
        if state is not None:
            raise ValueError('fresh training cannot overwrite a checkpoint')
        state = new(request['implementation'], request['policy'])
    elif state is None or (state['implementation'], state['policy']) != (request['implementation'], request['policy']):
        raise ValueError('checkpoint identity mismatch')
    if stage == 'evaluate':
        if state['phase'] != 'evaluation' or request['items']:
            raise ValueError('evaluation is read-only; no labels or admission allowed')
    else:
        for item in request['items']:
            admit(state, item['record'], item['verified_digest'])
        if stage == 'training':
            select(state)
        else:
            finish_acquisition(state)
    before = contract.digest(state)
    frozen_predictions = predictions(state)
    if contract.digest(state) != before:
        raise AssertionError('prediction mutated state')
    return state, frozen_predictions


def checkpoint(state):
    return {'state': deepcopy(state), 'state_digest': contract.digest(state),
            'configuration_digest': contract.digest(contract.configuration()), 'code_pin': contract.code_pin()}


def load_checkpoint(value):
    if not isinstance(value, dict) or set(value) != {'state', 'state_digest', 'configuration_digest', 'code_pin'}:
        raise ValueError('invalid checkpoint envelope')
    if (value['code_pin'] != contract.code_pin()
            or value['configuration_digest'] != contract.digest(contract.configuration())
            or value['state_digest'] != contract.digest(value['state'])):
        raise ValueError('checkpoint/source/configuration integrity mismatch')
    state = deepcopy(value['state'])
    if (state['version'] != contract.VERSION or state['implementation'] not in KERNELS
            or state['policy'] not in contract.POLICIES):
        raise ValueError('incompatible checkpoint')
    kernel = KERNELS[state['implementation']]
    if (state['candidate_digest'] != contract.digest(kernel.catalog())
            or state['analysis'] != kernel.analyze(records(state))):
        raise ValueError('checkpoint candidate/evidence disagreement')
    return state


def science(state):
    result = deepcopy(state)
    result.pop('implementation')
    return result
