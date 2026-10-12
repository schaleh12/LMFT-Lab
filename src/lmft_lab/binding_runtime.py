"""Opt-in neutral binding through the supervised runtime; no model inference."""
from copy import deepcopy
import re
from . import binding_contract as contract, binding_primary as primary, binding_memory as memory

RULE = 'binding-runtime-state-1'
MODES = ('binding-primary', 'binding-memory')
POLICIES = (*contract.POLICIES, 'informative-frozen')
KERNELS = {'binding-primary': primary, 'binding-memory': memory}
RECORD_KEYS = {'version', 'id', 'split', 'channels', 'outcome', 'source'}


def policy(condition):
    if condition not in POLICIES:
        raise ValueError('unsupported binding condition')
    return {'version': RULE, 'condition': condition, 'family': contract.configuration()}


def newborn(mode, condition):
    policy(condition)
    return {'version': RULE, 'mode': mode, 'condition': condition, 'phase': 'training',
            'candidate_digest': contract.digest(KERNELS[mode].catalog()), 'evidence': {},
            'analysis': KERNELS[mode].analyze({}), 'prediction_snapshot': None,
            'query': None, 'request_id': None, 'budget_spent': 0}


def records(current):
    return {eid: row['record'] for eid, row in current['evidence'].items()}


def valid_record(record):
    return (type(record) is dict and set(record) == RECORD_KEYS
            and record['version'] == contract.VERSION and type(record['id']) is str
            and re.fullmatch(r'[tq]\d{3}', record['id']) is not None
            and record['split'] in ('training', 'acquisition')
            and record['id'].startswith('t' if record['split'] == 'training' else 'q')
            and contract.features_valid(record['channels']) and 3 not in record['channels']
            and type(record['outcome']) is bool and record['source'] == contract.SOURCE)


def check_state(current):
    """Recompute derived state at load; no repair or silent migration."""
    if (type(current) is not dict or current.get('version') != RULE
            or current.get('mode') not in MODES or current.get('condition') not in POLICIES):
        raise ValueError('unsupported binding state')
    expected = newborn(current['mode'], current['condition'])
    if set(current) != set(expected) or current['candidate_digest'] != expected['candidate_digest']:
        raise ValueError('binding state schema/family mismatch')
    kernel = KERNELS[current['mode']]
    if (type(current['evidence']) is not dict
            or any(type(row) is not dict or set(row) != {'record', 'message_id', 'verification'}
                   or not valid_record(row['record']) or eid != row['record']['id']
                   or row['verification'] != {'rule': 'binding-registry-verifier-1',
                                              'record_digest': contract.digest(row['record'])}
                   for eid, row in current['evidence'].items())
            or current['analysis'] != kernel.analyze(records(current))):
        raise ValueError('binding evidence/derivation mismatch')
    phase = current['phase']
    train = {eid: row for eid, row in records(current).items() if row['split'] == 'training'}
    acquired = [row for row in records(current).values() if row['split'] == 'acquisition']
    if phase == 'training':
        if (acquired or current['query'] is not None or current['request_id'] is not None
                or type(current['budget_spent']) is not int or current['budget_spent'] != 0
                or current['prediction_snapshot'] is not None):
            raise ValueError('invalid training episode')
    elif phase in ('pending', 'evaluation'):
        count = 27 if current['condition'] == 'already-supported' else 4
        snapshot = kernel.analyze(train)['survivors']
        condition = 'informative' if current['condition'] == 'informative-frozen' else current['condition']
        query = kernel.choose(snapshot, contract.query_pool(condition), condition)
        selected = query['selected']
        if (set(train) != {f't{i:03}' for i in range(count)} or current['query'] != query
                or current['prediction_snapshot'] != snapshot
                or type(current['budget_spent']) is not int or current['budget_spent'] != int(selected is not None)
                or (selected is None and current['request_id'] is not None)
                or (selected is not None and (type(current['request_id']) is not str or not current['request_id']))
                or len(acquired) > current['budget_spent']
                or (phase == 'evaluation' and len(acquired) != current['budget_spent'])
                or any(selected is None or row['id'] != selected['id'] or row['channels'] != selected['channels'] for row in acquired)):
            raise ValueError('invalid binding episode/selection')
    else:
        raise ValueError('unsupported binding phase')
    return True


def applies(state):
    """Notice binding identity at any layer, including inconsistent outer state."""
    def field(value, key):
        return value.get(key) if type(value) is dict else None
    return any(value in MODES for value in (field(state, 'experiment'),
        field(field(state, 'manifest'), 'experiment'), field(field(state, 'judgment'), 'mode')))


def check_runtime(state, *, experiment=None, condition=None):
    """Validate cross-layer identity and committed request history, without I/O."""
    from .runtime import validate_message, message_identity
    current = state['judgment']; manifest = state['manifest']
    check_state(current)
    mode = current['mode']; selected_condition = current['condition']
    if (state.get('experiment') != mode or manifest.get('experiment') != mode
            or manifest.get('mode') != 'fixture' or manifest.get('fixture_rule') != RULE
            or contract.digest(manifest.get('binding_policy')) != contract.digest(policy(selected_condition))
            or (experiment is not None and experiment != mode)
            or (condition is not None and condition != selected_condition)):
        raise ValueError('binding runtime configuration mismatch')
    receipts, outbox = state['receipts'], state['outbox']
    if (type(receipts) is not list or any(type(r) is not dict for r in receipts)
            or type(outbox) is not list or any(type(o) is not dict for o in outbox)
            or type(state['processed']) is not dict):
        raise ValueError('invalid binding runtime history')

    def accepted(status):
        return [r for r in receipts if r.get('status') == status]

    def message(receipt, operation, kind):
        item = receipt.get('message')
        try:
            validate_message(item, contextual_content=True)
        except (ValueError, TypeError, KeyError) as exc:
            raise ValueError('invalid binding accepted-message history') from exc
        content = item['content']
        if (item['type'] != kind or set(content) != {'text', 'operation', 'record'}
                or content['operation'] != operation or type(content['record']) is not dict
                or receipt.get('message_id') != item['id']
                or state['processed'].get(item['id']) != message_identity(item)
                or type(receipt.get('cycle')) is not int or not 0 < receipt['cycle'] <= state['cycle']
                or type(receipt.get('sequence')) is not int or not 0 < receipt['sequence'] <= state['cursor']):
            raise ValueError('inconsistent binding accepted-message history')
        return item

    selections = accepted('training_closed'); closures = accepted('acquisition_closed')
    requests = [o for o in outbox if o.get('type') == 'clarification_request']
    replies = [r for r in accepted('accepted_evidence')
               if r.get('message', {}).get('content', {}).get('operation') == 'reply'
               or str(r.get('evidence_ref', '')).startswith('q')]
    if current['phase'] == 'training':
        if selections or closures or requests or replies:
            raise ValueError('orphan binding history before selection')
        return True
    if len(selections) != 1:
        raise ValueError('binding selection history must be unique')
    selection = selections[0]; selection_message = message(selection, 'select', 'observation')
    if selection_message['content']['record']:
        raise ValueError('invalid binding selection command')
    selected = current['query']['selected']
    if selected is None:
        if requests or current['request_id'] is not None or replies:
            raise ValueError('orphan binding request without selected query')
    else:
        matches = [(i, o) for i, o in enumerate(outbox) if o.get('id') == current['request_id']]
        if len(requests) != 1 or len(matches) != 1 or matches[0][1] != requests[0]:
            raise ValueError('binding request must resolve uniquely in outbox')
        index, request = matches[0]
        expected = {'schema_version': 1, 'id': f'out-{index+1}', 'sender': state['individual_id'],
            'source': 'authored-communication-rule-1', 'type': 'clarification_request',
            'content': {'text': 'Request one registered observation.', 'query': selected, 'budget_spent': 1},
            'reply_to': selection_message['id'], 'sequence': index+1, 'cycle': selection['cycle']}
        if (set(request) != set(expected) | {'timestamp'} or type(request['timestamp']) is not str
                or not request['timestamp']
                or contract.digest({k:v for k,v in request.items() if k != 'timestamp'}) != contract.digest(expected)):
            raise ValueError('binding request payload/source/correlation mismatch')
    acquired = [row for row in current['evidence'].values() if row['record']['split'] == 'acquisition']
    if len(replies) != len(acquired):
        raise ValueError('binding acquired evidence/reply history mismatch')
    reply_cycle = selection['cycle']
    if acquired:
        row = acquired[0]; reply = replies[0]; item = message(reply, 'reply', 'teacher_reply')
        if (row['message_id'] != item['id'] or reply.get('evidence_ref') != row['record']['id']
                or item['reply_to'] != current['request_id'] or item['source'] != contract.SOURCE
                or contract.digest(item['content']['record']) != contract.digest(row['record'])
                or reply['cycle'] <= selection['cycle']):
            raise ValueError('binding accepted reply correlation mismatch')
        reply_cycle = reply['cycle']
    if current['phase'] == 'pending':
        if closures:
            raise ValueError('binding pending state has closed history')
    else:
        if len(closures) != 1:
            raise ValueError('binding closure history must be unique')
        closure = closures[0]; item = message(closure, 'close', 'observation')
        if item['content']['record'] or closure['cycle'] <= reply_cycle:
            raise ValueError('binding closure precedes selection/reply')
    return True


def predict(current, case):
    if (type(case) is not dict or set(case) != {'id', 'channels'} or type(case['id']) is not str
            or not 1 <= len(case['id']) <= 96 or not contract.features_valid(case['channels'])):
        raise ValueError('invalid feature-only prediction case')
    if current['phase'] == 'training':
        raise ValueError('close training before prediction')
    survivors = (current['prediction_snapshot'] if current['condition'] == 'informative-frozen'
                 else current['analysis']['survivors'])
    result = KERNELS[current['mode']].predict(survivors, case)
    result['decision'] = 'abstain' if result['prediction'] is None else 'success' if result['prediction'] else 'failure'
    result['basis'] = 'pre-acquisition-frozen' if current['condition'] == 'informative-frozen' else 'current-evidence'
    return result


def handle(state, message, models, receipt, verifier=None):
    from .runtime import emit
    check_runtime(state)
    current = state['judgment']; content = message['content']
    def respond(text, **extra):
        return emit(state, 'response', {'text': text, **extra}, message['id'])
    def reject(reason):
        receipt.update(status='rejected', reason=reason)
        respond('Rejected: ' + reason)
        return state
    if set(content) != {'text', 'operation', 'record'} or type(content['record']) is not dict:
        return reject('invalid binding command')
    operation, record = content['operation'], content['record']
    if operation == 'reply':
        if message['type'] != 'teacher_reply' or not current['request_id'] or message['reply_to'] != current['request_id']:
            return reject('reply does not match outstanding request')
    elif message['type'] != 'observation':
        return reject('operation requires observation envelope')
    if operation == 'barrier' and not record:
        respond('Input barrier reached.'); return state
    if operation == 'evaluate':
        try:
            before = contract.digest(current); result = predict(current, record)
            assert contract.digest(current) == before
        except ValueError as exc:
            return reject(str(exc))
        receipt['status'] = 'evaluated'
        respond('Current prediction: ' + result['decision'] + '.', result=result)
        return state
    if operation not in ('train', 'reply', 'select', 'close'):
        return reject('unsupported binding operation; text/proposals cannot install relationships')
    if not state['learning']:
        return reject('learning disabled')
    if operation in ('train', 'reply'):
        if not valid_record(record) or message['source'] != contract.SOURCE:
            return reject('invalid evidence schema/source')
        split = 'training' if operation == 'train' else 'acquisition'
        if record['split'] != split:
            return reject('evidence split does not match operation')
        prior = current['evidence'].get(record['id'])
        if prior:
            if contract.digest(prior['record']) != contract.digest(record):
                return reject('conflicting evidence identity')
            receipt['status'] = 'duplicate_evidence'; return state
        if current['phase'] != ('training' if operation == 'train' else 'pending'):
            return reject('evidence phase closed')
        if operation == 'train':
            count = 27 if current['condition'] == 'already-supported' else 4
            if record['id'] not in {f't{i:03}' for i in range(count)}:
                return reject('unregistered training identity')
        else:
            selected = current['query']['selected']
            if (selected is None or current['budget_spent'] != 1 or record['id'] != selected['id']
                    or record['channels'] != selected['channels']):
                return reject('not the selected query')
        if verifier is None:
            return reject('trusted receiver verifier required')
        try:
            verified = verifier.verify(record)
        except (ValueError, OSError):
            return reject('trusted receiver verification failed')
        if verified is None or contract.digest(verified) != contract.digest(record):
            return reject('unverified registered observation')
        current['evidence'][record['id']] = {'record': deepcopy(verified), 'message_id': message['id'],
            'verification': {'rule': 'binding-registry-verifier-1', 'record_digest': contract.digest(verified)}}
        current['analysis'] = KERNELS[current['mode']].analyze(records(current))
        receipt.update(status='accepted_evidence', evidence_ref=record['id'])
        respond('Verified observation admitted.', evidence_id=record['id'])
        return state
    if record:
        return reject('control command requires empty record')
    if operation == 'select':
        count = 27 if current['condition'] == 'already-supported' else 4
        if current['phase'] != 'training' or set(current['evidence']) != {f't{i:03}' for i in range(count)}:
            return reject('complete training required; selection is one-shot')
        condition = 'informative' if current['condition'] == 'informative-frozen' else current['condition']
        current['prediction_snapshot'] = deepcopy(current['analysis']['survivors'])
        current['query'] = KERNELS[current['mode']].choose(current['analysis']['survivors'], contract.query_pool(condition), condition)
        selected = current['query']['selected']; current['budget_spent'] = int(selected is not None)
        current['phase'] = 'pending'
        if selected is not None:
            current['request_id'] = emit(state, 'clarification_request',
                {'text': 'Request one registered observation.', 'query': deepcopy(selected), 'budget_spent': 1}, message['id'])
        receipt['status'] = 'training_closed'; respond('Training closed; selection persisted.')
    else:
        acquired = sum(row['record']['split'] == 'acquisition' for row in current['evidence'].values())
        if current['phase'] != 'pending' or acquired != current['budget_spent']:
            return reject('pending selected reply required before closure')
        current['phase'] = 'evaluation'; receipt['status'] = 'acquisition_closed'
        respond('Acquisition closed; predictions remain read-only.')
    return state
