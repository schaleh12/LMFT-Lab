"""Small synthetic command interface; no language model or freeform interpretation."""
from copy import deepcopy
import json
from . import action_policy as action, correction as repair, correction_fixture as fixture
from .late_evidence import LateRegistry
from .runtime_store import digest

RULE = 'action-command-1'
MODES = ('action-command-lmft', 'action-command-memory')
SCENARIOS = ('r1', 'r8', 'r2')


def policy():
    return {'rule': RULE, 'scenarios': list(SCENARIOS), 'request_budget': 1,
            'permits': repair.load_policy(), 'command_sender': 'fixture-operator',
            'command_source': RULE, 'reply_sender': fixture.AUTHORITY, 'reply_source': fixture.SOURCE}


def session(individual, mode):
    return {'rule': RULE, 'episode_id': individual + ':action-1', 'request_id': None,
            'scenario': None, 'mode': 'memory' if mode.endswith('memory') else 'full',
            'late_registration_checks': 0, 'gather_checks': 0}


def snapshot(state):
    control = state['action_session']; episode = state.get('episode')
    return {'initialized': control['scenario'] is not None,
            'current': repair.predict(state['judgment'], control['case']) if control['scenario'] else None,
            'historical_request': deepcopy(state['questions'].get('action-request')),
            'episode_id': control['episode_id'], 'request_id': control['request_id'],
            'phase': episode['status'] if episode else 'not-requested',
            'budget_remaining': 1 - episode['charged'] if episode else 1}


def evidence_shape(record):
    fields = {'evidence_id', 'case_id', 'scope', 'question', 'part', 'value', 'source'}
    return (type(record) is dict and set(record) == fields and type(record['value']) is bool
            and all(type(record[k]) is str for k in fields - {'value'}))


def reply_shape(selected, payload):
    if type(payload) is not dict:
        return False
    if selected['kind'] == 'gather':
        return (set(payload) == {'records'} and type(payload['records']) is list
                and 1 <= len(payload['records']) <= 2 and all(evidence_shape(r) for r in payload['records']))
    fields = {'correction_id', 'authority', 'target_id', 'expected_digest', 'reason', 'replacement'}
    return (set(payload) == fields and all(type(payload[k]) is str for k in fields - {'replacement'})
            and evidence_shape(payload['replacement']))


def handle(state, message, models, receipt):
    from .runtime import emit
    control = state['action_session']; content = message['content']; text = content['text']

    def reject(reason):
        receipt.update(status='rejected', reason=reason)
        emit(state, 'response', {'text': 'Command rejected.', 'reason': reason}, message['id'])
        return state

    def respond(status):
        state['receipts'][-1]['status'] = status
        emit(state, 'response', {'text': 'Synthetic action state.', **snapshot(state)}, message['id'])
        return state

    if len(text) > 32 or len(json.dumps(content, ensure_ascii=False).encode('utf-8')) > 4096:
        return reject('command exceeds bounded format')
    expected_keys = {'text', 'record'} if text in ('reply', 'evidence') else {'text'}
    if set(content) != expected_keys:
        return reject('invalid command fields')
    if text not in ('inspect', 'barrier', 'request', 'reply', 'evidence', *('initialize '+s for s in SCENARIOS)):
        return reject('unknown fixed command')
    if message['type'] != ('teacher_reply' if text == 'reply' else 'observation'):
        return reject('wrong command transport')
    if text in ('inspect', 'barrier'):
        return respond('inspected' if text == 'inspect' else 'barrier')
    if not state['learning']:
        return reject('learning disabled')
    if text.startswith('initialize') or text == 'request':
        if (message['sender'], message['source']) != ('fixture-operator', RULE):
            return reject('unregistered command operator')
    elif (message['sender'], message['source']) != (fixture.AUTHORITY, fixture.SOURCE):
        return reject('unregistered evidence operator')
    if text.startswith('initialize'):
        if control['scenario'] is not None:
            return reject('already initialized')
        scenario = text.split()[1]; bundle = action.prepare(scenario)
        if bundle['state']['judgment']['policy'] != state['judgment']['policy']:
            return reject('setup authority differs from pinned policy')
        state['judgment'] = bundle['state']['judgment']
        state['initialization'] = {'source': 'explicit authored fixture setup', 'scenario': scenario,
                                   'receipts': bundle['state']['receipts']}
        control.update(scenario=scenario, case=bundle['case'], offers=bundle['offers'])
        return respond('initialized')
    if control['scenario'] is None:
        return reject('initialize first')
    if text == 'request':
        if 'episode' in state:
            return respond('request_already_spent')
        receipt['status'] = 'action_requested'
        state = action.request({'state': state, 'case': control['case'], 'offers': control['offers']}, control['mode'])
        control = state['action_session']; selected = state['episode']['selected']
        if selected:
            request_id = emit(state, 'clarification_request', {'text': 'Supply the selected synthetic operation.',
                'episode_id': control['episode_id'], 'operation_id': selected['id'],
                'selected': selected, 'budget_remaining': 0}, message['id'])
            control['request_id'] = request_id
        return respond('action_requested' if selected else 'no_eligible_action')
    if text == 'reply':
        episode = state.get('episode'); record = content['record']
        fields = {'episode_id', 'request_id', 'operation_id', 'payload'}
        if not episode or not episode['selected']:
            return reject('no requested operation')
        if type(record) is not dict or set(record) != fields:
            return reject('invalid reply fields')
        selected = episode['selected']
        if (record['episode_id'], record['request_id'], record['operation_id'], message.get('reply_to')) != (
                control['episode_id'], control['request_id'], selected['id'], control['request_id']):
            return reject('uncorrelated operation')
        if not reply_shape(selected, record['payload']):
            return reject('invalid reply schema')
        if selected['kind'] == 'correction' and (record['payload']['correction_id'], record['payload']['target_id']) != (selected['correction_id'], selected['target_id']):
            return reject('uncorrelated correction target')
        pending = episode['status'] == 'pending'
        state, result = action.receive(state, control['case'], record['payload'], message['sender'], message_id=message['id'])
        if pending and selected['kind'] == 'gather' and selected['available']:
            # The existing exact-reference comparison also executes on a false
            # reply. Count that work even though no record is admitted.
            result['verification_checked'] = True
            state['action_session']['gather_checks'] += 1
        state['receipts'][-1].update(result)
        return respond(result['status'])
    # A closed request does not authorize another action. A registered later report
    # can still change support through the existing append-only evidence handler.
    if state.get('episode', {}).get('status') != 'closed':
        return reject('late evidence requires a closed episode')
    record = content['record']
    if not evidence_shape(record):
        return reject('invalid evidence schema')
    if record['case_id'] != control['case']['case_id'] or record['scope'] != control['case']['scope']:
        return reject('unrelated evidence coordinate')
    registry = LateRegistry(); forwarded = deepcopy(message)
    forwarded['content'] = {'text': 'Registered later instrument report.', 'operation': 'evidence', 'record': record}
    repair.handle(state, forwarded, None, receipt, evidence_registry=registry)
    control['late_registration_checks'] += registry.calls
    return respond('evidence_admitted' if receipt['status'] == 'processed' else receipt['status'])
