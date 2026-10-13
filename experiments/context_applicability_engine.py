"""Strict experiment-local admission, replay validation and read-only support."""
from copy import deepcopy
import context_applicability_contract as c
import context_applicability_primary as primary
import context_applicability_memory as memory


def kernel(controller):
    return memory if controller == 'memory' else primary


def refresh(state):
    implementation = kernel(state['controller'])
    state['analysis'] = implementation.analyze(state['evidence'])
    basis = state['evidence'][:1] if state['controller'] == 'frozen' else state['evidence']
    state['decision_analysis'] = implementation.analyze(basis)


def newborn(controller, schedule):
    config = c.configuration(controller, schedule)
    state = {'schema_version': 1, 'version': c.VERSION, 'controller': controller,
             'schedule': schedule, 'configuration': config, 'phase': 'initial',
             'charged': 0, 'evidence': [], 'events': [], 'receipts': []}
    refresh(state)
    return state


def _apply(state, event, verify):
    """Apply to private state; journal replay invokes exactly the same admission gates."""
    checked = None

    def finish(status, reason):
        state['receipts'].append({'sequence': len(state['receipts']) + 1,
                                  'status': status, 'reason': reason})
        return checked

    if type(event) is not dict or set(event) != {'operation', 'source', 'record'}:
        return finish('rejected', 'invalid_event')
    if event['source'] != c.SOURCE:
        return finish('rejected', 'wrong_source')
    if event['operation'] == 'opportunity':
        if not c.exact(event['record'], {}):
            return finish('rejected', 'invalid_opportunity')
        if state['phase'] != 'ready' or state['charged'] != 0:
            return finish('rejected', 'no_opportunity_remaining')
        state['charged'] = 1
        state['phase'] = 'pending' if state['configuration']['available'] else 'closed'
        return finish('opportunity', 'pending' if state['phase'] == 'pending' else 'unavailable')
    if event['operation'] != 'calibrate':
        return finish('rejected', 'unsupported_operation')
    record = event['record']
    if not c.calibration_valid(record):
        return finish('rejected', 'invalid_calibration')
    for old in state['evidence']:
        if old['evidence_id'] == record['evidence_id']:
            return finish('duplicate' if c.exact(old, record) else 'rejected',
                          'duplicate_evidence' if c.exact(old, record) else 'conflicting_evidence_id')
    if state['phase'] == 'initial':
        valid_slot = (record['slot'] == 'initial' and record['evidence_id'] == 'cal-0'
                      and c.exact(record['context'], [0, 0]))
    elif state['phase'] == 'pending':
        valid_slot = (record['slot'] == 'followup' and record['evidence_id'] == 'cal-1'
                      and c.exact(record['context'], state['configuration']['followup_context'])
                      and record['reference'] == 1 - state['evidence'][0]['reference'])
    else:
        valid_slot = False
    if not valid_slot:
        return finish('rejected', 'wrong_slot_or_schedule')
    checked = verify(deepcopy(record))
    if type(checked) is not bool:
        raise ValueError('reference verification must return a strict Boolean')
    if not checked:
        return finish('rejected', 'unverified_reference')
    state['evidence'].append(deepcopy(record))
    state['phase'] = 'ready' if record['slot'] == 'initial' else 'closed'
    refresh(state)
    return finish('accepted', 'registered_paired_observation')


def validate(state, controller, schedule):
    """Do not trust checksum-valid nested labels, counters or cached survivor sets."""
    expected = newborn(controller, schedule)
    if (type(state) is not dict or set(state) != set(expected)
            or type(state['events']) is not list
            or not c.exact(state['configuration'], expected['configuration'])
            or state['controller'] != controller or state['schedule'] != schedule):
        raise ValueError('checkpoint configuration/controller mismatch')
    for entry in state['events']:
        if (type(entry) is not dict or set(entry) != {'event', 'verification'}
                or (entry['verification'] is not None and type(entry['verification']) is not bool)):
            raise ValueError('invalid verification journal')
        calls = []

        def replay(record):
            calls.append(record)
            if type(entry['verification']) is not bool:
                raise ValueError('missing recorded reference check')
            return entry['verification']

        checked = _apply(expected, entry['event'], replay)
        if checked is None and entry['verification'] is not None:
            raise ValueError('spurious recorded reference check')
        expected['events'].append(deepcopy(entry))
    if not c.exact(expected, state):
        raise ValueError('checkpoint replay/state/witness mismatch')
    return True


def advance(state, event, verify):
    validate(state, state['controller'], state['schedule'])
    result = deepcopy(state)
    checked = _apply(result, event, verify)
    result['events'].append({'event': deepcopy(event), 'verification': checked})
    return result


def mapping(state, ctx):
    mode = state['controller']
    if mode in ('primary', 'memory', 'frozen'):
        return kernel(mode).predict(state['decision_analysis']['survivors'], ctx)
    if not c.context(ctx):
        return {'status': 'unknown_context', 'mapping': None, 'votes': []}
    if mode == 'equality':
        value = 0
    elif state['evidence']:
        last = state['evidence'][-1]
        value = last['raw'] ^ last['reference']
    else:
        return {'status': 'unsupported', 'mapping': None, 'votes': []}
    return {'status': 'consensus', 'mapping': value, 'votes': [value]}


def evaluate(state, cases):
    validate(state, state['controller'], state['schedule'])
    before = c.digest(state)
    result = []
    for case in cases:
        ctx = case.get('context') if type(case) is dict else None
        inferred = mapping(state, ctx)
        view = c.support_view(case)
        cross = []
        for value in sorted(set(inferred['votes'])):
            normalized = sorted({v ^ value for v in view['second']})
            cross.append({'mapping': value, 'normalized_second': normalized,
                          'cross_disagreement': view['first'][0] != normalized[0]
                          if len(view['first']) == len(normalized) == 1 else None})
        result.append({'mapping': inferred, 'support': view, 'cross_by_mapping': cross,
                       **c.supported_prediction(view, inferred['mapping'], inferred['status'])})
    if c.digest(state) != before:
        raise AssertionError('evaluation mutated scientific state')
    return result


def event(record=None, operation='calibrate', source=c.SOURCE):
    return {'operation': operation, 'source': source, 'record': deepcopy(record) if record is not None else {}}


def scientific(state):
    return {key: deepcopy(state[key]) for key in
            ('phase', 'charged', 'evidence', 'events', 'receipts', 'analysis', 'decision_analysis')}
