"""Contract boundaries and actual process restart for the isolated frozen study."""
from copy import deepcopy
import importlib
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
import context_applicability_contract as c
import context_applicability_primary as primary
import context_applicability_memory as memory
import context_applicability_engine as engine
import context_applicability_device as device
import run_context_applicability as harness
from lmft_lab.runtime_store import Store


def ready(controller='primary', schedule='P10', world='switch0-high', flip=0):
    initial, follow = device.calibrations(world, schedule, flip)
    calls = []
    verify = harness.registry_verifier([initial, follow], calls)
    state = engine.advance(engine.newborn(controller, schedule), engine.event(initial), verify)
    return state, initial, follow, verify, calls


def closed(controller='primary', schedule='P10', world='switch0-high', flip=0):
    state, initial, follow, verify, calls = ready(controller, schedule, world, flip)
    state = engine.advance(state, engine.event(operation='opportunity'), verify)
    if follow:
        state = engine.advance(state, engine.event(follow), verify)
    return state, initial, follow, verify, calls


def projection(state):
    return {k: state[k] for k in ('evidence', 'analysis', 'decision_analysis', 'phase', 'charged')}


@pytest.mark.parametrize('world', device.WORLDS)
@pytest.mark.parametrize('schedule', c.SCHEDULES)
@pytest.mark.parametrize('flip', [0, 1])
def test_all_worlds_realizable_and_independent_memory_parity(world, schedule, flip):
    p, initial, follow, _, _ = closed('primary', schedule, world, flip)
    m, *_ = closed('memory', schedule, world, flip)
    assert c.exact(engine.scientific(p), engine.scientific(m))
    assert p['analysis']['survivors']
    cases, labels = device.evaluation(world)
    before = c.digest(p)
    pp = engine.evaluate(p, cases); mp = engine.evaluate(m, cases)
    assert c.exact(pp, mp) and c.digest(p) == before
    for row, label in zip(pp, labels):
        if row['prediction'] is not None:
            assert row['prediction'] == label['target'] and label['oracle_resolved']
        if label['template'] == 'contradiction':
            assert row['support']['within_part'] and row['prediction'] is None
            assert all(x['normalized_second'] == [0, 1] for x in row['cross_by_mapping'])


@pytest.mark.parametrize('schedule,world,expected', [
    ('P10', 'switch0-high', ['c0']),
    ('P11', 'switch0-high', ['c0', 'c1']),
    ('P10', 'switch1-high', ['0', 'c1']),
    ('P00', 'pass', ['0', 'c0', 'c1']),
    ('U10', 'switch0-high', ['0', 'c0', 'c1']),
])
def test_frozen_identifiability_examples(schedule, world, expected):
    state, *_ = closed(schedule=schedule, world=world)
    assert state['analysis']['survivors'] == expected


def test_memory_does_not_call_primary(monkeypatch):
    def forbidden(*args, **kwargs):
        pytest.fail('memory called primary kernel')
    for name in ('value', 'analyze', 'predict'):
        monkeypatch.setattr(primary, name, forbidden)
    state, *_ = closed('memory')
    assert engine.mapping(state, [1, 1])['mapping'] == 1
    assert engine.evaluate(state, c.integrity_cases())


@pytest.mark.parametrize('field,value', [
    ('context', [False, 0]), ('context', [0, True]), ('context', [0.0, 0]),
    ('context', [0]), ('context', [0, 2]), ('context', '00'),
    ('raw', False), ('raw', 0.0), ('raw', -1), ('reference', True),
    ('reference', 1.0), ('version', True), ('scope', 'foreign'),
    ('evidence_id', True), ('slot', True),
])
def test_strict_calibration_schema(field, value):
    state = engine.newborn('primary', 'P10')
    record = c.calibration('cal-0', [0, 0], 0, 0, 'initial'); record[field] = value
    calls = []
    after = engine.advance(state, engine.event(record), lambda row: calls.append(row) or True)
    assert c.exact(projection(state), projection(after)) and not calls
    assert after['receipts'][-1]['status'] == 'rejected'


@pytest.mark.parametrize('kind', ['extra', 'missing', 'source', 'slot', 'id', 'unknown_op', 'unverified'])
def test_untrusted_or_malformed_calibration_does_not_learn(kind):
    state = engine.newborn('primary', 'P10')
    event = engine.event(c.calibration('cal-0', [0, 0], 0, 0, 'initial'))
    if kind == 'extra':
        event['record']['relation'] = 'untrusted-claim'
    elif kind == 'missing':
        del event['record']['reference']
    elif kind == 'source':
        event['source'] = 'unregistered'
    elif kind == 'slot':
        event['record']['slot'] = 'followup'
    elif kind == 'id':
        event['record']['evidence_id'] = 'cal-1'
    elif kind == 'unknown_op':
        event['operation'] = 'support'
    after = engine.advance(state, event, lambda row: False)
    assert c.exact(projection(state), projection(after))
    assert after['receipts'][-1]['status'] == 'rejected'


def test_duplicate_conflict_and_single_opportunity():
    state, initial, follow, verify, calls = ready()
    duplicate = engine.advance(state, engine.event(initial), verify)
    assert projection(duplicate) == projection(state) and len(calls) == 1
    conflict = deepcopy(initial); conflict['raw'] = 1 - conflict['raw']
    rejected = engine.advance(duplicate, engine.event(conflict), verify)
    assert projection(rejected) == projection(state) and len(calls) == 1
    pending = engine.advance(rejected, engine.event(operation='opportunity'), verify)
    finished = engine.advance(pending, engine.event(follow), verify)
    second = engine.advance(finished, engine.event(operation='opportunity'), verify)
    assert projection(second) == projection(finished) and second['charged'] == 1 and len(calls) == 2


def test_verifier_response_is_strict_boolean():
    record = c.calibration('cal-0', [0, 0], 0, 0, 'initial')
    with pytest.raises(ValueError, match='strict Boolean'):
        engine.advance(engine.newborn('primary', 'P10'), engine.event(record), lambda row: 1)


def test_support_cannot_launder_mapping_uncertainty_or_contradiction():
    state, *_ = ready()
    case = c.integrity_cases()[-1]
    before = c.digest(state)
    row = engine.evaluate(state, [case])[0]
    assert row['mapping']['status'] == 'mapping_ambiguous'
    assert row['prediction'] is None and c.digest(state) == before
    state, *_ = closed()
    case = deepcopy(case)
    case['records'].append(c.record('contrary', case['id'], 'second', 0))
    row = engine.evaluate(state, [case])[0]
    assert row['support']['within_part'] and row['normalized_second'] == [0, 1]
    assert 'within_part_contradiction' in row['reasons'] and row['prediction'] is None
    assert row['cross_part_disagreement'] is None
    assert all(r['cross_disagreement'] is None for r in row['cross_by_mapping'])


@pytest.mark.parametrize('mutation', ['context', 'boolean_context', 'boolean_value', 'foreign', 'conflicting_id', 'unverified', 'extra'])
def test_support_schema_and_scope_are_read_only(mutation):
    state, *_ = closed(); case = deepcopy(c.integrity_cases()[0]); before = c.digest(state)
    if mutation == 'context': case['context'] = [2, 0]
    elif mutation == 'boolean_context': case['context'] = [False, 0]
    elif mutation == 'boolean_value': case['records'][1]['value'] = False
    elif mutation == 'foreign': case['records'][1]['scope'] = 'foreign'
    elif mutation == 'conflicting_id':
        bad = deepcopy(case['records'][1]); bad['value'] = 1; case['records'].append(bad)
    elif mutation == 'unverified': case['records'][1]['source'] = 'unknown'
    else: case['reference'] = 0
    result = engine.evaluate(state, [case])[0]
    assert result['prediction'] is None and c.digest(state) == before


@pytest.mark.parametrize('controller', c.CONTROLLERS)
def test_actual_three_process_restart_and_identity_invariance(tmp_path, controller):
    initial, follow = device.calibrations('switch0-high', 'P10', 0)
    cases, _ = device.evaluation('switch0-high')
    artifacts = tmp_path/'trace'; artifacts.mkdir()
    result = harness.run_individual(tmp_path/'opaque', controller, 'P10', initial, follow, cases, artifacts)
    assert all(result['checks'].values())
    # Each stage is launched by a fresh Popen and waited; PID uniqueness alone isn't proof.
    assert all(type(result[stage]['pid']) is int for stage in ('pre', 'post', 'reload'))


@pytest.mark.parametrize('controller', ['primary', 'memory'])
def test_empty_family_persists_with_witnesses_actual_restart(tmp_path, controller):
    initial = c.calibration('cal-0', [0, 0], 0, 0, 'initial')
    follow = c.calibration('cal-1', [0, 0], 0, 1, 'followup')
    artifacts = tmp_path/'trace'; artifacts.mkdir()
    result = harness.run_individual(tmp_path/'opaque', controller, 'P00', initial, follow,
                                    c.integrity_cases(), artifacts)
    assert all(result['checks'].values())
    state = result['post']['state']
    assert state['analysis']['survivors'] == []
    assert all(state['analysis']['rejection_witnesses'].values())
    assert len(state['evidence']) == 2
    assert all(r['mapping']['status'] == 'unsupported' and r['prediction'] is None
               for r in result['reload']['predictions'])


@pytest.mark.parametrize('mutation', ['controller', 'schedule', 'config_controller', 'config_family',
    'config_budget_bool', 'config_source', 'charged_bool', 'schema_bool', 'survivors',
    'decision_survivors', 'witness', 'phase', 'receipt', 'verification', 'evidence', 'extra',
    'launch_controller', 'launch_schedule'])
def test_checksum_valid_inconsistent_restart_rejects_before_write(tmp_path, mutation):
    state, *_ = ready()
    controller = 'primary'; schedule = 'P10'
    if mutation == 'controller': state['controller'] = 'memory'
    elif mutation == 'schedule': state['schedule'] = 'P11'
    elif mutation == 'config_controller': state['configuration']['controller'] = 'memory'
    elif mutation == 'config_family': state['configuration']['family'] = ['0']
    elif mutation == 'config_budget_bool': state['configuration']['followup_budget'] = True
    elif mutation == 'config_source': state['configuration']['source_manifest'] = {}
    elif mutation == 'charged_bool': state['charged'] = False
    elif mutation == 'schema_bool': state['schema_version'] = True
    elif mutation == 'survivors': state['analysis']['survivors'] = ['0']
    elif mutation == 'decision_survivors': state['decision_analysis']['survivors'] = ['0']
    elif mutation == 'witness': state['analysis']['rejection_witnesses']['1'] = []
    elif mutation == 'phase': state['phase'] = 'closed'
    elif mutation == 'receipt': state['receipts'][0]['reason'] = 'other'
    elif mutation == 'verification': state['events'][0]['verification'] = 1
    elif mutation == 'evidence': state['evidence'][0]['raw'] = 1
    elif mutation == 'extra': state['hidden'] = 'not-allowed'
    elif mutation == 'launch_controller': controller = 'memory'
    else: schedule = 'P11'
    root = tmp_path/'individual'; Store(root).commit(state)
    before = {p.name: p.read_bytes() for p in root.iterdir()}
    with pytest.raises(RuntimeError, match='worker failed'):
        harness.worker(root, controller, schedule, 'followup', [], [], [], tmp_path/'failure')
    assert before == {p.name: p.read_bytes() for p in root.iterdir()}
    assert json.loads((tmp_path/'failure.json').read_text())['verification'] == []


def test_identical_histories_and_public_support_predictions():
    states = [ready(world=w)[0] for w in ('pass', 'switch0-high', 'switch1-high')]
    assert all(c.exact(engine.scientific(states[0]), engine.scientific(s)) for s in states)
    assert all(c.exact(engine.evaluate(states[0], c.integrity_cases()), engine.evaluate(s, c.integrity_cases()))
               for s in states)
    states = [closed(schedule='P11', world=w)[0] for w in ('switch0-high', 'switch1-high')]
    assert c.exact(engine.scientific(states[0]), engine.scientific(states[1]))
    assert engine.mapping(states[0], [0, 1])['status'] == 'mapping_ambiguous'


def test_controls_share_evidence_but_do_not_force_failure():
    states = {mode: closed(mode)[0] for mode in c.CONTROLLERS}
    assert all(s['evidence'] == states['primary']['evidence'] for s in states.values())
    assert engine.mapping(states['frozen'], [1, 1])['status'] == 'mapping_ambiguous'
    assert engine.mapping(states['equality'], [1, 1])['mapping'] == 0
    assert engine.mapping(states['replacement'], [0, 0])['mapping'] == 1
    # In the uniform equality world both simple controls are correct everywhere.
    for mode in ('equality', 'replacement'):
        state, *_ = closed(mode, world='pass')
        assert all(engine.mapping(state, list(ctx))['mapping'] == 0 for ctx in c.CONTEXTS)


def test_device_calibration_never_calls_learning(monkeypatch):
    def forbidden(*args, **kwargs): pytest.fail('device used a learner')
    monkeypatch.setattr(primary, 'value', forbidden)
    monkeypatch.setattr(memory, 'predict', forbidden)
    for world in device.WORLDS:
        initial, follow = device.calibrations(world, 'P10', 0)
        assert initial['reference'] == 0 and follow['reference'] == 1
        assert initial['context'] == [0, 0] and follow['context'] == [1, 0]


def test_protocol_pin_and_import_boundary():
    assert harness.file_hash(harness.ROOT/c.PROTOCOL) == harness.PROTOCOL_SHA256
    spec = importlib.util.spec_from_file_location('isolated_worker_test', harness.ROOT/'experiments/context_applicability_worker.py')
    module = importlib.util.module_from_spec(spec)
    try:
        spec.loader.exec_module(module)
        with pytest.raises(ImportError, match='private coordinator'):
            module.Boundary().find_spec('context_applicability_device')
        with pytest.raises(ImportError, match='private coordinator'):
            module.Boundary().find_spec('run_context_applicability')
    finally:
        sys.meta_path[:] = [finder for finder in sys.meta_path if finder.__class__.__module__ != 'isolated_worker_test']
