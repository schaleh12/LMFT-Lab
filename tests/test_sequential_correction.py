"""Late observations must reintroduce conflict without rewriting correction history."""
from copy import deepcopy
import importlib
from pathlib import Path
import pytest
from lmft_lab import correction as repair, preservation_context as preservation
from lmft_lab.runtime_store import atomic_json, digest


@pytest.fixture
def study(monkeypatch):
    monkeypatch.syspath_prepend(str(Path(__file__).resolve().parents[1] / 'experiments'))
    return importlib.import_module('run_sequential_correction')


@pytest.mark.parametrize('case', ['r1', 'r8'])
@pytest.mark.parametrize('mode', ['full', 'memory'])
@pytest.mark.parametrize('control', ['late', 'no-later', 'frozen'])
def test_correction_then_late_evidence_and_replay(study, case, mode, control):
    row = study.inputs()[f'{case}/{mode}/{control}']; initial = deepcopy(row['state'])
    assert repair.predict(initial['judgment'], row['case'])['decision'] == 'abstain'
    corrected = study.transition(row, 'corrected')
    assert corrected['probe']['prediction']['decision'] == 'success'
    assert corrected['probe']['stored_records'] == 4
    late = study.transition(corrected, 'late'); final = study.transition(late, 'final')
    expected = 'abstain' if control == 'late' else 'success'
    assert final['probe']['prediction']['decision'] == expected
    assert final['probe']['effective']['independent_count'] == 3 + (control == 'late')
    assert final['probe']['stored_records'] == 4 + (control == 'late')
    assert final['state']['questions']['action-request']['status'] == 'resolved_by_correction'
    assert final['state']['episode']['status'] == 'closed'
    events = final['state']['judgment']['corrections']
    assert [e['accepted'] for e in events] == [True, False, False, False]
    assert sum(e['verification']['checked'] for e in events) == 1
    assert all(final['state']['judgment']['ledger'][k] == v for k,v in initial['judgment']['ledger'].items())
    if control == 'late':
        assert final['probe']['prediction']['support']['shielded']['inconsistent']
        assert not final['probe']['prediction']['support']['shielded']['resolved']


def test_default_runtime_rejects_extended_registry(study):
    row = study.inputs()['r1/full/late']; record = study.late_record(row['case'])
    changed, receipt = study.intake(row['state'], 'not-opted-in', 'evidence', record)
    assert receipt['status'] == 'rejected'
    assert repair.effective_ref(changed['judgment']) == repair.effective_ref(row['state']['judgment'])
    changed, receipt = study.intake(row['state'], 'opted-in', 'evidence', record, study.LateRegistry())
    assert record['evidence_id'] in changed['judgment']['ledger']


@pytest.mark.parametrize('field,value', [('scope','elsewhere'), ('value',True), ('evidence_id','invented'), ('source','imposter')])
def test_late_registry_is_exact_and_rejections_do_not_supply_support(study, field, value):
    row = study.inputs()['r1/full/late']; record = study.late_record(row['case']); record[field] = value
    changed, receipt = study.intake(row['state'], 'bad-report', 'evidence', record, study.LateRegistry())
    assert receipt['status'] == 'rejected'
    assert repair.effective_ref(changed['judgment']) == repair.effective_ref(row['state']['judgment'])


def test_selection_and_probe_do_not_read_truth_or_mutate(study, monkeypatch):
    row = study.inputs()['r1/full/late']; before = digest(row)
    def forbidden(*args):
        pytest.fail('truth accessed during selection or probe')
    monkeypatch.setattr(study.fixture, 'actual_success', forbidden)
    monkeypatch.setattr(study.fixture, 'replacement_valid', forbidden)
    monkeypatch.setattr(study.action, 'service_reply', forbidden)
    study.probe(row['state'], row['case'])
    for mode in ('full','memory'):
        assert study.action.select(row['state']['judgment'], row['case'], row['offers'], mode)[0]
    assert digest(row) == before


@pytest.mark.parametrize('value', [0, 1, 0.0, 1.0, None, 'false', 'true', [], {}])
def test_non_boolean_late_values_rejected_without_support_or_lineage_changes(study, value):
    row = study.transition(study.inputs()['r1/full/late'], 'corrected')
    record = study.late_record(row['case']); record['value'] = value
    assert study.LateRegistry().admitted(record) is False
    changed, receipt = study.intake(row['state'], 'malformed-value', 'evidence', record, study.LateRegistry())
    assert receipt['status'] == 'rejected'
    assert study.probe(changed, row['case']) == study.probe(row['state'], row['case'])
    assert changed['judgment']['ledger'] == row['state']['judgment']['ledger']
    assert changed['judgment']['corrections'] == row['state']['judgment']['corrections']


@pytest.mark.parametrize('field', ['evidence_id', 'case_id', 'scope', 'question', 'part', 'source'])
@pytest.mark.parametrize('value', [False, 0, None, [], {}])
def test_registry_rejects_non_string_coordinate_and_identity_fields(study, field, value):
    record = study.late_record(study.fixture.public_case('c1')); record[field] = value
    assert study.LateRegistry().admitted(record) is False


@pytest.mark.parametrize('record', [None, False, 0, [], 'record', {}])
def test_registry_rejects_non_record_or_missing_schema(study, record):
    assert study.LateRegistry().admitted(record) is False


def test_registry_requires_exact_keys_and_preserves_valid_boolean_dedup(study):
    for key in ('c1', 'c9'):
        record = study.late_record(study.fixture.public_case(key))
        assert study.LateRegistry().admitted(record) is True
        assert study.LateRegistry().admitted(dict(reversed(list(record.items())))) is True
        assert study.LateRegistry().admitted({**record, 'extra': 'field'}) is False
        for field in record:
            missing = deepcopy(record); missing.pop(field)
            assert study.LateRegistry().admitted(missing) is False
    row = study.transition(study.inputs()['r1/full/late'], 'corrected')
    record = study.late_record(row['case'])
    accepted, _ = study.intake(row['state'], 'valid-boolean', 'evidence', record, study.LateRegistry())
    assert type(accepted['judgment']['ledger'][record['evidence_id']]['record']['value']) is bool
    replay, receipt = study.intake(accepted, 'new-transport-id', 'evidence', record, study.LateRegistry())
    assert receipt['status'] == 'duplicate_evidence' and digest(replay) == digest(accepted)
    alias = deepcopy(record); alias['value'] = 0
    rejected, receipt = study.intake(accepted, 'integer-identity-collision', 'evidence', alias, study.LateRegistry())
    assert receipt['status'] == 'rejected'
    assert study.probe(rejected, row['case']) == study.probe(accepted, row['case'])


def test_permitted_stale_operations_are_rejected_before_verification(study):
    result = study.stale_companion()
    assert all(r['event']['authorization']['passed'] for r in result['checks'])
    assert all(not r['event']['eligibility']['passed'] and not r['event']['verification']['checked'] for r in result['checks'])


def test_actual_chained_process_restart(study, tmp_path):
    context = tmp_path / 'context.json'; atomic_json(context, preservation.capture_current(Path.cwd()))
    result = study.run(tmp_path / 'study', context)
    assert result['integrity_passed'] == result['integrity_total']
    assert len(set(result['restart_pids'])) == 3
    assert result['metrics']['full/late']['final']['accuracy'] is None
    assert result['metrics']['full/no-later']['final']['accuracy'] == .5


def test_changed_restart_input_fails_before_admission(study, tmp_path):
    root = tmp_path / 'run'; root.mkdir()
    context = root / 'current-preservation-context.json'
    atomic_json(context, preservation.capture_current(Path.cwd()))
    atomic_json(root / 'provenance.json', {'preservation_kind': preservation.KIND,
                'preservation_context_sha256': preservation.file_hash(context)})
    snapshot = root / 'pending.json'; atomic_json(snapshot, study.inputs())
    with pytest.raises(ValueError, match='restart input hash mismatch'):
        study.worker(root, 'corrected', snapshot, '0'*64)
    assert not (root / 'restarted-corrected.json').exists()
