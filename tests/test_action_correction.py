"""Action eligibility is external policy; existing receiver remains authoritative."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import pytest
from lmft_lab import correction as repair, correction_fixture as fixture
from lmft_lab.runtime_store import digest


def harness():
    spec = importlib.util.spec_from_file_location('action_harness', Path(__file__).resolve().parents[1] / 'experiments/run_action_correction.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize('identifier', ['r' + str(i) for i in range(1, 13)])
def test_frozen_actions_receiver_and_exact_memory_scores(identifier):
    h = harness(); bundle = h.prepare(identifier); before = digest(bundle)
    actual, traces = h.select(bundle['state']['judgment'], bundle['case'], bundle['offers'], 'full')
    memory, scalar = h.select(bundle['state']['judgment'], bundle['case'], bundle['offers'], 'memory')
    assert actual == memory
    assert [r['score'] for r in traces['questions'] if 'score' in r] == [r['score'] for r in scalar['questions'] if 'score' in r]
    for mode in h.MODES:
        row = h.finish(h.request(bundle, mode), bundle['case'])
        assert (row['selected']['kind'] if row['selected'] else None) == h.EXPECTED[mode][list(h.DEFS).index(identifier)]
        assert all(row['checks'].values())
    assert digest(bundle) == before


def test_selection_never_reads_reply_or_outcome(monkeypatch):
    h = harness(); bundle = h.prepare('r9')
    monkeypatch.setattr(h, 'service_reply', lambda *a: pytest.fail('reply accessed'))
    monkeypatch.setattr(h, 'proposal', lambda *a: pytest.fail('replacement accessed'))
    monkeypatch.setattr(fixture, 'replacement_valid', lambda *a: pytest.fail('verification accessed'))
    monkeypatch.setattr(fixture, 'actual_success', lambda *a: pytest.fail('truth accessed'))
    assert h.request(bundle, 'full')['episode']['selected']['kind'] == 'correction'
    assert h.request(bundle, 'ablated')['episode']['selected']['kind'] == 'gather'


@pytest.mark.parametrize('mutation,reason', [('digest', 'stale target digest'), ('target', 'inactive or missing target'),
    ('authority', 'no matching operation permit'), ('scope', 'wrong correction coordinate')])
def test_correction_offer_metadata_is_not_self_authorizing(mutation, reason):
    h = harness(); b = h.prepare('r1'); offer = deepcopy(b['offers'][0])
    if mutation == 'digest': offer['expected_digest'] = '0' * 64
    if mutation == 'target': offer['target_id'] = 'absent'
    if mutation == 'authority': offer['authority'] = 'imposter'
    if mutation == 'scope': offer['coordinate']['scope'] = 'elsewhere'
    assert h.preflight(b['state']['judgment'], b['case'], offer) == reason


def test_same_question_can_need_both_gather_and_correction():
    h = harness(); b = h.prepare('r1'); state = b['state']['judgment']
    # A second conflicting root at check1 plus absent check2: missing AND inconsistent.
    target = 'c1/shielded/check2'; state['ledger'].pop(target); state['heads'].pop(target); state['roots'].pop(target)
    r = deepcopy(state['ledger']['c1/shielded/check1']['record']); r.update(evidence_id='second', value=True)
    state['ledger']['second'] = {'record': r, 'root': 'second', 'parent': None}; state['heads']['second'] = 'second'; state['roots']['second'] = 'second'
    gather = {'id': 'gather', 'kind': 'gather', 'field': 'shielded', 'case_id': 'c1', 'scope': 'batch-1', 'parts': ['check2'], 'available': True}
    assert h.preflight(state, b['case'], b['offers'][0]) is None
    assert h.preflight(state, b['case'], gather) is None


@pytest.mark.parametrize('kind', ['correction', 'gather'])
def test_receiver_rejects_spoofed_sender_without_support_mutation(kind):
    h = harness(); b = h.prepare('r1' if kind == 'correction' else 'r2'); pending = h.request(b, 'full')
    reply = h.service_reply(pending['episode']['selected'])
    final, receipt = h.receive(pending, b['case'], reply, sender='imposter')
    assert h.semantic(final) == h.semantic(pending)
    assert final['episode']['charged'] == 1 and final['episode']['status'] == 'closed'
    assert receipt['status'] in ('correction_rejected', 'unverified_gather_reply')
    replay, receipt = h.receive(final, b['case'], reply)
    assert digest(replay) == digest(final) and receipt['status'] == 'duplicate_reply'


def test_permitted_wrong_replacement_is_not_verified_repair():
    h = harness(); b = h.prepare('r4'); row = h.finish(h.request(b, 'full'), b['case'])
    event = row['action_events'][0]
    assert event['authorization']['passed'] and event['eligibility']['passed']
    assert event['verification']['checked'] and not event['verification']['passed'] and not event['accepted']
    assert row['after']['decision'] == 'abstain' and row['new_resolved'] == 0


def test_gather_does_not_correct_existing_root_or_assume_consistency():
    h = harness(); b = h.prepare('r12'); row = h.finish(h.request(b, 'full'), b['case'])
    assert row['coverage_gain'] == .5 and row['new_resolved'] == 0
    assert row['after']['support']['shielded']['inconsistent'] and row['after']['decision'] == 'abstain'
    assert not row['action_events'] and len(row['final']['judgment']['heads']) == len(b['state']['judgment']['heads']) + 1


def test_correction_closes_only_own_question_and_retains_root():
    h = harness(); b = h.prepare('r9'); row = h.finish(h.request(b, 'full'), b['case'])
    final = row['final']; event = row['action_events'][0]
    assert final['questions']['action-request']['status'] == 'resolved_by_correction'
    assert row['after']['decision'] == 'abstain' and not row['after']['support']['payload_valid']['resolved']
    assert event['closed_questions'] == ['action-request'] and event['cache_invalidated'] == ['c1']
    root = 'c1/shielded/check1'; head = final['judgment']['heads'][root]
    assert final['judgment']['ledger'][head]['parent'] == root and final['judgment']['roots'][head] == root


def test_reply_correlation_budget_and_single_edge_ablation():
    h = harness(); b = h.prepare('r1'); pending = h.request(b, 'full')
    wrong = deepcopy(h.service_reply(pending['episode']['selected'])); wrong['correction_id'] = 'other'
    final, receipt = h.receive(pending, b['case'], wrong)
    assert receipt['status'] == 'uncorrelated_reply' and h.semantic(final) == h.semantic(pending)
    assert h.receive(final, b['case'], h.service_reply(pending['episode']['selected']))[1]['status'] == 'closed_episode'
    _, full = h.select(b['state']['judgment'], b['case'], b['offers'], 'full')
    _, ablated = h.select(b['state']['judgment'], b['case'], b['offers'], 'ablated')
    for f, a in zip([r for r in full['questions'] if 'score' in r], [r for r in ablated['questions'] if 'score' in r]):
        fp, ap = f['propagation'], a['propagation']; assert digest(fp['direct_frame']) == digest(ap['direct_frame'])
        differences = [(x, y) for x, y in zip(fp['relationships'], ap['relationships']) if x != y]
        assert len(differences) == 1
        x, y = differences[0]; assert x['source_id'] == h.attention.C and x['active'] and not y['active']
        assert {k: v for k, v in x.items() if k != 'active'} == {k: v for k, v in y.items() if k != 'active'}


def test_pending_and_closed_budget_cannot_be_reset():
    h = harness(); b = h.prepare('r1'); pending = h.request(b, 'full')
    assert digest(h.request({**b, 'state': pending}, 'memory')) == digest(pending)
    final = h.finish(pending, b['case'])['final']
    assert digest(h.request({**b, 'state': final}, 'gather-only')) == digest(final)


@pytest.mark.parametrize('mutation', ['value', 'scope', 'part'])
def test_gather_reply_exact_coordinate_reference(mutation):
    h = harness(); b = h.prepare('r2'); pending = h.request(b, 'full')
    reply = h.service_reply(pending['episode']['selected'])
    reply['records'][0][mutation] = False if mutation == 'value' else 'wrong'
    changed, receipt = h.receive(pending, b['case'], reply)
    assert receipt['status'] == 'unverified_gather_reply' and h.semantic(changed) == h.semantic(pending)


@pytest.mark.parametrize('identifier', ['r' + str(i) for i in range(1, 13)])
def test_original_control_is_unchanged_selector_without_action_filter(identifier):
    h = harness(); b = h.prepare(identifier); view = repair.effective(b['state']['judgment']); view['mode'] = 'consistent-full'
    selected, original_trace = h.circuit.select(view, b['case'])
    action, trace = h.select(b['state']['judgment'], b['case'], b['offers'], 'original')
    assert digest(trace['questions']) == digest(original_trace)
    assert (action is None) == (selected is None)
    if action:
        assert action['field'] == selected['field'] and action['parts'] == list(h.circuit.PARTS[selected['field']])


def test_original_contradiction_gather_preserves_conflict_and_spends_work():
    h = harness(); b = h.prepare('r1'); row = h.finish(h.request(b, 'original'), b['case'])
    assert row['selected']['kind'] == 'gather' and row['new_resolved'] == 0 and row['admitted_records'] == 2
    assert row['after']['support']['shielded']['inconsistent'] and row['after']['decision'] == 'abstain'
    assert not row['action_events'] and row['duplicate_additional_admissions'] == 0


def test_original_unavailable_request_spends_budget_without_receiver_work():
    h = harness(); b = h.prepare('r11'); pending = h.request(b, 'original'); row = h.finish(pending, b['case'])
    assert row['selected'] is not None and pending['episode']['charged'] == 1
    assert row['receipt'] == {'status': 'gather_unavailable', 'verification_checked': False}
    assert row['admitted_records'] == 0 and h.semantic(row['final']) == h.semantic(pending)
    assert h.request(b, 'full')['episode']['selected'] is None
