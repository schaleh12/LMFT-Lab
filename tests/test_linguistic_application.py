"""Synthetic contract tests only; no natural corpus or held-out data access."""
from copy import deepcopy
from itertools import product
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
import linguistic_application as a
import linguistic_application_memory as memory
import linguistic_application_development as dev
from lmft_lab.runtime_store import Store, digest


def example(i, label='a', words=('blue',), document=None):
    return {'id': str(i), 'document_id': document or 'd' + str(i),
            'tokens': ['order', *words], 'target_indices': [0], 'sense': label,
            'provenance': {'source': 'synthetic-contract-only', 'locator': str(i),
                           'source_sha256': '0' * 64}}


def batch(number=1, rows=None):
    if rows is None:
        rows = ([example(1), example(2), example(3, 'b', ('red',)),
                 example(4, 'b', ('red',))] if number == 1 else
                [example(5, 'b'), example(6, 'a', ('green',)),
                 example(7, 'a', ('green',))])
    return {'split_id': 'synthetic-split', 'batch': number, 'examples': rows}


def trained():
    return a.advance(a.newborn('synthetic-split'), batch())


def item(words=('blue',), id='probe'):
    return {'id': id, 'tokens': ['order', *words], 'target_indices': [0]}


def rule(state, cue, label='a', version=-1):
    return next(r for r in state['revisions'][version]['primary'][label]['rules']
                if r['cue'] == list(cue))


def test_fixed_tokenizer_compound_punctuation_and_all_target_occurrences():
    record = {'tokens': ['Order', "BLUE-green's", 'orders', 'two words', '99', '!', 'unused'],
              'target_indices': [0, 6]}
    assert a.features(record) == {'blue', 'green', 's', 'two', 'words'}


def test_two_documents_not_two_examples_required():
    state = a.advance(a.newborn('synthetic-split'), batch(rows=[
        example(1, document='same'), example(2, document='same')]))
    r = rule(state, ['blue'])
    assert r['positive'] == ['1', '2'] and r['positive_documents'] == ['same']
    assert r['reasons'] == ['insufficient_documents']
    assert state['revisions'][0]['primary']['a']['lifecycle'] == 'unsupported'


def test_independent_pair_cue_works_when_each_unigram_contradicted():
    rows = [example(1, words=('blue', 'wide')), example(2, words=('wide', 'blue')),
            example(3, 'b', ('blue',)), example(4, 'b', ('wide',))]
    state = a.advance(a.newborn('synthetic-split'), batch(rows=rows))
    assert rule(state, ['blue', 'wide'])['status'] == 'active'
    assert rule(state, ['blue'])['negative'] == ['3']
    assert rule(state, ['wide'])['negative'] == ['4']
    assert a.predict(state, [item(('wide', 'blue'))])[0]['controllers']['primary']['labels'] == ['a']


def test_revision_invalidates_preserves_witnesses_and_original_evidence():
    before = trained(); fingerprint = digest(before)
    after = a.advance(before, batch(2))
    assert digest(before) == fingerprint
    assert after['revisions'][0] == before['revisions'][0]
    assert after['examples'][:4] == before['examples']
    r = rule(after, ['blue'])
    assert r['status'] == 'invalidated' and r['previous_status'] == 'active'
    assert r['positive'] == ['1', '2'] and r['negative'] == ['5']
    assert rule(after, ['green'])['status'] == 'active'
    outputs = a.predict(after, [item()])[0]['controllers']
    assert outputs['primary']['status'] == 'abstain'
    assert outputs['frozen']['labels'] == ['a']
    a.validate(after)


def test_insufficient_can_become_active_and_no_invalidated_resurrection():
    s = a.advance(a.newborn('synthetic-split'), batch(rows=[example(1)]))
    t = a.advance(s, batch(2, [example(2)]))
    assert rule(t, ['blue'])['status'] == 'active'
    assert rule(t, ['blue'])['previous_status'] == 'rejected'
    prior = deepcopy(t['revisions'][-1]['primary'])
    prior['a']['rules'][0]['status'] = 'invalidated'
    with pytest.raises(ValueError, match='resurrection'):
        a.revised(a.primary_table(t['examples']), prior, 3)


@pytest.mark.parametrize('words,status,labels', [
    (('blue',), 'single', ['a']), (('red',), 'single', ['b']),
    (('blue', 'red'), 'ambiguous', ['a', 'b']),
    (('unknown',), 'abstain', []), ((), 'abstain', [])])
def test_application_status_not_candidate_lifecycle(words, status, labels):
    state = trained(); old = digest(state)
    out = a.predict(state, [item(words)])[0]['controllers']
    assert out['primary']['status'] == status and out['primary']['labels'] == labels
    assert out['primary']['selected'] == (labels[0] if len(labels) == 1 else None)
    assert out['primary'] == out['memory']
    assert out['majority']['labels'] == ['a']  # lexical tie, even unknown context
    assert digest(state) == old


def test_memory_generation_independent_of_primary(monkeypatch):
    rows = batch()['examples']
    expected = a.primary_table(rows)
    monkeypatch.setattr(a, 'primary_table', lambda _: pytest.fail('primary called'))
    assert memory.memory_table(rows) == expected


@pytest.mark.parametrize('labels', list(product(('a', 'b'), repeat=4)))
def test_exhaustive_small_labelings_match_independent_memory(labels):
    words = [('x',), ('y',), ('x', 'y'), ('x', 'z')]
    rows = [example(i, label, words[i]) for i, label in enumerate(labels)]
    assert a.primary_table(rows) == memory.memory_table(rows)


def test_identical_duplicate_does_not_change_support_majority_or_witnesses():
    request = batch(); request['examples'].append(deepcopy(request['examples'][0]))
    state = a.advance(a.newborn('synthetic-split'), request)
    assert len(state['examples']) == 4 and state['batches'][0]['duplicates'] == ['1']
    assert rule(state, ['blue'])['positive'] == ['1', '2']
    assert a.advance(state, request) == state


@pytest.mark.parametrize('mutation', [
    lambda r: r.update(batch=True), lambda r: r.update(batch=2),
    lambda r: r.update(split_id='other'), lambda r: r.update(examples=[]),
    lambda r: r['examples'][0].update(sense=None),
    lambda r: r['examples'][0].update(tokens='blue'),
    lambda r: r['examples'][0].update(tokens=[]),
    lambda r: r['examples'][0].update(tokens=['']),
    lambda r: r['examples'][0].update(target_indices=[True]),
    lambda r: r['examples'][0].update(target_indices=[-1]),
    lambda r: r['examples'][0].update(target_indices=[100]),
    lambda r: r['examples'][0].update(target_indices=[0, 0]),
    lambda r: r['examples'][0].update(target_indices=[1, 0]),
    lambda r: r['examples'][0].update(target_indices=[]),
    lambda r: r['examples'][0]['provenance'].update(source_sha256='bad'),
    lambda r: r['examples'][0]['provenance'].update(locator=''),
    lambda r: r['examples'][0].update(extra='not allowed'),
])
def test_bad_training_request_rejected_without_mutation(mutation):
    state = a.newborn('synthetic-split'); before = digest(state)
    request = batch(); mutation(request)
    with pytest.raises(ValueError):
        a.advance(state, request)
    assert digest(state) == before


@pytest.mark.parametrize('conflict', ['id', 'locator', 'document', 'replay'])
def test_conflicts_reject_entire_batch(conflict):
    state = trained(); before = digest(state)
    request = batch(2)
    if conflict == 'id': request['examples'][0]['id'] = '1'
    if conflict == 'locator': request['examples'][0]['provenance']['locator'] = '1'
    if conflict == 'document': request['examples'][0]['document_id'] = 'd1'
    if conflict == 'replay': request = batch(); request['examples'][0]['tokens'].append('different')
    with pytest.raises(ValueError): a.advance(state, request)
    assert digest(state) == before


@pytest.mark.parametrize('extra', ['sense', 'gold', 'document_id', 'provenance', 'stage'])
def test_runtime_refuses_gold_or_audit_metadata(extra):
    probe = item(); probe[extra] = 'forbidden'
    state = trained(); before = digest(state)
    with pytest.raises(ValueError): a.predict(state, [probe])
    assert digest(state) == before


def test_duplicate_application_ids_reject():
    with pytest.raises(ValueError): a.predict(trained(), [item(), item()])


def test_metrics_include_ambiguity_wrong_inclusions_exclusions_and_unseen_gold():
    state = trained()
    probes = [item(('blue',), 'one'), item(('blue','red'), 'two'), item((), 'three')]
    predictions = a.predict(state, probes); before = digest(state)
    result = a.score(predictions, {'one': 'a', 'two': 'a', 'three': 'unseen'})['primary']
    assert result['overall'] == {'n': 3, 'strict_correct': 1, 'singleton': 1,
        'singleton_wrong': 0, 'abstain': 1, 'ambiguous': 1, 'ambiguous_gold_included': 1,
        'wrong_inclusions': 1, 'exclusions': 1, 'singleton_coverage': 1/3}
    assert result['per_sense']['unseen']['n'] == 1
    assert digest(state) == before
    with pytest.raises(ValueError): a.score(predictions, {'one': 'a'})


@pytest.mark.parametrize('corruption', ['pin', 'evidence', 'witness', 'history'])
def test_reloaded_state_rejects_inconsistent_or_unpinned_content(corruption):
    state = trained()
    if corruption == 'pin': state['pins']['pyproject.toml'] = 'f'*64
    if corruption == 'evidence': state['examples'][0]['sense'] = 'wrong'
    if corruption == 'witness': rule(state, ['blue'])['positive'] = []
    if corruption == 'history': state['batches'][0]['added_ids'] = []
    with pytest.raises(ValueError): a.validate(state)


def test_actual_restart_replay_predict_and_invalid_request_nonmutation(tmp_path):
    state_dir = tmp_path / 'synthetic-state'
    first = dev.invoke(state_dir, 'train', batch())
    checkpoint = state_dir / 'checkpoint.json'
    before = checkpoint.read_bytes()
    one = dev.invoke(state_dir, 'predict', {'items': [item()]})
    two = dev.invoke(state_dir, 'predict', {'items': [item()]})
    replay = dev.invoke(state_dir, 'train', batch())
    assert one['predictions'] == two['predictions']
    assert len({first['pid'], one['pid'], two['pid'], replay['pid']}) == 4
    assert before == checkpoint.read_bytes() and replay['replayed']
    with pytest.raises(RuntimeError):
        dev.invoke(state_dir, 'predict', {'items': [{**item(), 'sense': 'a'}]})
    bad = batch(2); bad['examples'][0]['provenance']['locator'] = '1'
    with pytest.raises(RuntimeError): dev.invoke(state_dir, 'train', bad)
    assert before == checkpoint.read_bytes()
    dev.invoke(state_dir, 'train', batch(2))
    changed = dev.invoke(state_dir, 'predict', {'items': [item()]})
    assert changed['predictions'][0]['controllers']['primary']['status'] == 'abstain'
    assert changed['predictions'][0]['controllers']['frozen']['labels'] == ['a']
    state = Store(state_dir).read(); state['revisions'][0]['primary']['a']['rules'][0]['positive'] = []
    Store(state_dir).commit(state)
    with pytest.raises(RuntimeError): dev.invoke(state_dir, 'inspect')


def test_development_adapter_rejects_unapproved_export_before_reading_data(tmp_path):
    (tmp_path / 'development.json').write_text('[]')
    with pytest.raises(ValueError, match='unapproved'):
        dev.load_development(tmp_path)


def test_corpus_artifact_output_cannot_be_repository():
    with pytest.raises(ValueError, match='outside'):
        dev.run('unread', Path(__file__).resolve().parents[1] / 'outputs' / 'forbidden')


@pytest.mark.parametrize('operation', ['inspect', 'predict'])
@pytest.mark.parametrize('field,value', [
    ('schema_version', True), ('schema_version', 1.0),
    ('revision_version', True), ('revision_version', 1.0),
    ('memory_version', True), ('memory_version', 1.0),
    ('cached_target', False), ('cached_target', 0.0),
    ('cached_batch', True), ('cached_batch', 1.0),
    ('stage', True), ('stage', 1.0),
    ('request_target', False), ('request_target', 0.0),
])
def test_restart_rejects_checksum_valid_numeric_type_substitution(tmp_path, operation, field, value):
    state = trained()
    if field in ('schema_version', 'stage'):
        state[field] = value
    elif field == 'revision_version':
        state['revisions'][0]['version'] = value
    elif field == 'memory_version':
        state['revisions'][0]['memory']['a']['version'] = value
    elif field == 'cached_target':
        state['examples'][0]['target_indices'] = [value]
    elif field == 'cached_batch':
        state['batches'][0]['batch'] = value
    else:
        state['batches'][0]['request']['examples'][0]['target_indices'] = [value]
    store = Store(tmp_path / 'numeric-type-probe')
    store.commit(state)  # Fresh correct checksum: rejection must be semantic/type checking.
    before = (store.root / 'checkpoint.json').read_bytes()
    with pytest.raises(RuntimeError):
        dev.invoke(store.root, operation, {'items': [item()]} if operation == 'predict' else None)
    assert (store.root / 'checkpoint.json').read_bytes() == before
