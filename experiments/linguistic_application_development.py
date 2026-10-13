"""Development-only export adapter/runner. Never locates or reads evaluation data."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import linguistic_application as app
from lmft_lab.local_models import strict_json
from lmft_lab.runtime_store import Store, atomic_json

ROOT = Path(__file__).resolve().parents[1]
BINDING = Path(__file__).with_name('LINGUISTIC_APPLICATION_DATA_BINDING.json')


def file_hash(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_development(directory):
    directory = Path(directory).resolve()
    binding = strict_json(BINDING.read_text(encoding='utf-8'))
    for name, pin in [('development.json', 'development_sha256'),
                      ('export-manifest.json', 'export_manifest_sha256')]:
        if file_hash(directory / name) != binding[pin]:
            raise ValueError('unapproved development export hash')
    manifest = strict_json((directory / 'export-manifest.json').read_text(encoding='utf-8'))
    expected = {'development.json', 'development-metadata.json', 'README', 'LICENSE',
                'USE-NOTICE.txt', 'DATASET-LICENSES.md'}
    if set(manifest) != expected:
        raise ValueError('export inventory mismatch')
    for name, record in manifest.items():
        if file_hash(directory / name) != record['sha256']:
            raise ValueError('export member mismatch')
    metadata = strict_json((directory / 'development-metadata.json').read_text(encoding='utf-8'))
    if metadata['split_manifest_sha256'] != binding['split_id']:
        raise ValueError('split identity mismatch')
    original = strict_json((directory / 'development.json').read_text(encoding='utf-8'))
    batches = {1: [], 2: []}
    ids, documents = set(), {1: set(), 2: set()}
    sentences = {1: set(), 2: set()}
    for row in original:
        app.exact(row, {'example_id', 'document_id', 'target_index', 'surface_tokens',
                        'target_sense_key', 'provenance', 'stage'})
        if row['stage'] not in ('development_batch_1', 'development_batch_2'):
            raise ValueError('non-development row')
        stage = int(row['stage'][-1])
        p = row['provenance']
        app.exact(p, {'archive_sha256', 'archive_member', 'sentence_id', 'sentence_sha256',
                      'annotation_version'})
        if p['archive_sha256'] != binding['archive_sha256']:
            raise ValueError('source identity mismatch')
        e = {'id': row['example_id'], 'document_id': row['document_id'],
             'tokens': row['surface_tokens'], 'target_indices': [row['target_index']],
             'sense': row['target_sense_key'],
             'provenance': {'source': p['annotation_version'],
                            'locator': f"{p['archive_member']}:{p['sentence_id']}:{row['target_index']}",
                            'source_sha256': p['archive_sha256']}}
        app.validate_example(e)
        if e['id'] in ids:
            raise ValueError('duplicate export ID')
        ids.add(e['id'])
        documents[stage].add(e['document_id'])
        sentences[stage].add((p['archive_member'], p['sentence_id']))
        batches[stage].append(e)
    if documents[1] & documents[2]:
        raise ValueError('development batches overlap documents')
    for stage in (1, 2):
        if (len(batches[stage]) != binding['batch_examples'][stage-1] or
                len(documents[stage]) != binding['batch_documents'][stage-1] or
                len(sentences[stage]) != binding['batch_sentences'][stage-1]):
            raise ValueError('export count mismatch')
    return binding, batches


def public_items(examples):
    return [{k: e[k] for k in ('id', 'tokens', 'target_indices')} for e in examples]


def invoke(state_dir, operation, request=None):
    env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
    result = subprocess.run([sys.executable, str(Path(__file__).with_name(
        'linguistic_application_worker.py')), operation, '--state-dir', str(state_dir)],
        input=json.dumps(request) if request is not None else '', text=True,
        capture_output=True, env=env, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr)
    return strict_json(result.stdout)


def run(export_dir, work_dir):
    work_dir = Path(work_dir).resolve()
    if work_dir == ROOT or ROOT in work_dir.parents:
        raise ValueError('corpus working artifacts must be outside repository')
    binding, batches = load_development(export_dir)
    work_dir.mkdir(parents=True, exist_ok=False)
    for name in ('README', 'LICENSE', 'USE-NOTICE.txt', 'DATASET-LICENSES.md',
                 'development.json', 'development-metadata.json', 'export-manifest.json'):
        shutil.copy2(Path(export_dir) / name, work_dir / name)
    state_dir = work_dir / 'state'
    trace, reports, batch1_predictions = [], {}, None
    for stage in (1, 2):
        request = {'split_id': binding['split_id'], 'batch': stage, 'examples': batches[stage]}
        atomic_json(work_dir / f'batch-{stage}-request.json', request)
        trained = invoke(state_dir, 'train', request)
        trace.append({'operation': 'train', **trained})
        checkpoint = state_dir / 'checkpoint.json'
        before = checkpoint.read_bytes()
        replayed = invoke(state_dir, 'train', request)
        assert replayed['replayed'] and before == checkpoint.read_bytes()
        trace.append({'operation': 'replay', **replayed})
        examples = batches[1] + (batches[2] if stage == 2 else [])
        output = invoke(state_dir, 'predict', {'items': public_items(examples)})
        again = invoke(state_dir, 'predict', {'items': public_items(examples)})
        assert output['predictions'] == again['predictions']
        assert before == checkpoint.read_bytes()
        trace.extend([{'operation': 'predict', **output}, {'operation': 'restart-predict', **again}])
        for row in output['predictions']:
            assert row['controllers']['primary'] == row['controllers']['memory']
        gold = {e['id']: e['sense'] for e in examples}
        reports[f'stage_{stage}_development'] = app.score(output['predictions'], gold)
        state = Store(state_dir).read()
        app.validate(state)
        revision = state['revisions'][-1]['primary']
        reports[f'stage_{stage}_cue_counts'] = dict(Counter(
            r['status'] for interp in revision.values() for r in interp['rules']))
        reports[f'stage_{stage}_new_cues'] = sum(r['transition'] == 'created'
            for interp in revision.values() for r in interp['rules'])
        if stage == 1:
            batch1_predictions = output['predictions']
            shutil.copy2(checkpoint, work_dir / 'batch-1-checkpoint.json')
        else:
            previous_ids = {e['id'] for e in batches[1]}
            after = [r for r in output['predictions'] if r['id'] in previous_ids]
            assert [r['controllers']['frozen'] for r in after] == [
                r['controllers']['primary'] for r in batch1_predictions]
            reports['stage_2_on_batch_1_development'] = app.score(
                after, {e['id']: e['sense'] for e in batches[1]})
            reports['development_regressions'] = {}
            for controller in app.CONTROLLERS:
                changes = []
                for old, new in zip(batch1_predictions, after):
                    assert old['id'] == new['id']
                    target = gold[old['id']]
                    a = old['controllers'][controller]['labels'] == [target]
                    b = new['controllers'][controller]['labels'] == [target]
                    changes.append((a, b))
                reports['development_regressions'][controller] = {
                    'n': len(changes), 'correct_to_not_correct': changes.count((True, False)),
                    'not_correct_to_correct': changes.count((False, True))}
    atomic_json(work_dir / 'development-trace.json', trace)
    summary = {'kind': 'development-only', 'evaluation_executed': False,
               'binding': binding, 'pins': app.pins(), 'reports': reports,
               'worker_pids': [x['pid'] for x in trace],
               'checks': {'fresh_process_restart': True, 'predict_nonmutation': True,
                          'replay_nonmutation': True, 'independent_memory_parity': True,
                          'frozen_retention': True},
               'external_artifacts': {p.relative_to(work_dir).as_posix(): file_hash(p)
                   for p in sorted(work_dir.rglob('*')) if p.is_file()}}
    atomic_json(work_dir / 'summary.json', summary)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--export-dir', required=True)
    parser.add_argument('--work-dir', required=True)
    args = parser.parse_args()
    summary = run(args.export_dir, args.work_dir)
    print(json.dumps(summary, sort_keys=True))
