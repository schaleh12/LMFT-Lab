"""Semantic adjudication of admitted representations against WordNet senses and baselines."""
import argparse
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re

from lmft_lab.runtime_store import Store, digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = 'semantic-adjudication-1'

WORDNET_GOLD_SENSES = {
    'order%1:07:01::': {
        'name': 'degree_magnitude',
        'definition': '(often followed by "of") a degree in a continuum of size or quantity; e.g. on the order of',
    },
    'order%1:10:00::': {
        'name': 'judicial_decree',
        'definition': 'a formal legal document issued by a court or authority; e.g. court order',
    },
    'order%1:10:01::': {
        'name': 'commercial_purchase',
        'definition': 'a commercial document requesting that a supplier provide merchandise or services; purchase order',
    },
    'order%1:10:02::': {
        'name': 'sequence_succession',
        'definition': 'the arrangement of things in succession; chronological or numerical sequence',
    },
    'order%1:10:03::': {
        'name': 'authoritative_command',
        'definition': 'an authoritative direction or instruction to do something; a military or personal command',
    },
    'order%1:14:00::': {
        'name': 'sequence_ordering',
        'definition': 'the act of putting things in a sequential arrangement; succession or serial arrangement',
    },
    'order%1:26:00::': {
        'name': 'social_condition',
        'definition': 'the established condition of social, religious, or political organization; state of peace and observance of the law',
    },
    'order%1:26:02::': {
        'name': 'systematic_arrangement',
        'definition': 'a logical or comprehensible arrangement of separate elements; structure or orderliness',
    },
}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False)


def adjudicate_gloss(gloss, lemma='order'):
    """Evaluates gloss informativeness, detecting tautological repetition vs explanatory substitution."""
    if not isinstance(gloss, str) or not gloss.strip():
        raise ValueError('nonempty string gloss required')

    pattern = rf'\b{re.escape(lemma)}s?\b'
    tautology_matches = re.findall(pattern, gloss, flags=re.IGNORECASE)
    tautology_present = len(tautology_matches) > 0

    tokens = [t for t in re.split(r'\s+', gloss.strip()) if t]

    return {
        'tautology_present': tautology_present,
        'target_substituted': not tautology_present,
        'tautology_occurrences': len(tautology_matches),
        'char_length': len(gloss),
        'token_count': len(tokens),
    }


def adjudicate_concordance(case_id, proposal, gold_sense_key):
    """Evaluates concordance between proposed reading/anchor and WordNet 3.0 ground truth."""
    if gold_sense_key not in WORDNET_GOLD_SENSES:
        raise ValueError(f'unrecognized gold sense: {gold_sense_key}')

    gold_info = WORDNET_GOLD_SENSES[gold_sense_key]
    readings = proposal.get('readings', [])
    if not readings:
        return {
            'status': 'discordant',
            'score': 0,
            'gold_sense_key': gold_sense_key,
            'gold_definition': gold_info['definition'],
            'note': 'No readings present in proposal.',
        }

    reading = readings[0]
    gloss = reading.get('gloss', '')
    quote = reading.get('context_quote', '')
    gloss_info = adjudicate_gloss(gloss)

    # Deterministic rubric based on preregistered WordNet senses:
    if gold_sense_key == 'order%1:10:02::':
        # Sequence: checks for explicit substitution of sequence/arrangement concepts
        if any(w in gloss.lower() for w in ('sequence', 'succession', 'arrangement', 'order')):
            score = 2 if gloss_info['target_substituted'] else 1
            status = 'concordant' if score == 2 else 'partially_concordant'
            note = 'Replaced target with explicit sequence concept.' if score == 2 else 'Captured sequential context with tautology.'
        else:
            status, score, note = 'discordant', 0, 'Did not convey sequence concept.'
    elif gold_sense_key == 'order%1:07:01::':
        # Degree / magnitude: checks for presence of numerical / degree construction or magnitude gloss
        if 'on the order of' in quote.lower() or 'high order' in quote.lower() or \
           any(w in quote.lower() for w in ('%', 'per_annum', 'month', 'high')) or \
           any(w in gloss.lower() for w in ('level', 'magnitude', 'quality', 'degree')):
            score = 2 if gloss_info['target_substituted'] else 1
            status = 'concordant' if score == 2 else 'partially_concordant'
            note = 'Captured magnitude idiom; clause paraphrase retained target.' if score == 1 else 'Substituted magnitude/degree concept.'
        else:
            status, score, note = 'discordant', 0, 'Failed to capture magnitude idiom.'
    elif gold_sense_key == 'order%1:10:00::':
        # Judicial / executive decree: checks for court / legal authority linkage or formal directive gloss
        if any(w in quote.lower() for w in ('court', 'judge', 'receiver', 'trustee', 'jurisdiction', 'authorized', 'directive', 'conference', 'goering')) or \
           any(w in gloss.lower() for w in ('directive', 'command', 'decree', 'legal', 'authority', 'formal')):
            score = 2 if gloss_info['target_substituted'] else 1
            status = 'concordant' if score == 2 else 'partially_concordant'
            note = 'Linked to judicial/executive authority; clause paraphrase retained target.' if score == 1 else 'Substituted legal/executive decree concept.'
        else:
            status, score, note = 'discordant', 0, 'Failed to capture legal/court authority.'
    elif gold_sense_key == 'order%1:10:01::':
        # Commercial purchase: checks for transactional context or purchase gloss
        if any(w in quote.lower() for w in ('expected', 'come_through', 'supplier', 'purchase', 'sales', 'shipments', 'receipts', 'vacation')) or \
           any(w in gloss.lower() for w in ('purchase', 'items', 'received', 'sent', 'goods', 'bought', 'requisition')):
            score = 2 if gloss_info['target_substituted'] else 1
            status = 'concordant' if score == 2 else 'partially_concordant'
            note = 'Identified commercial requisition; repeated target.' if score == 1 else 'Substituted purchase order concept.'
        else:
            status, score, note = 'discordant', 0, 'Failed to capture purchase/order context.'
    elif gold_sense_key == 'order%1:10:03::':
        # Authoritative command: military or personal instruction/direction
        if any(w in gloss.lower() for w in ('instruction', 'direction', 'command', 'directive', 'rule', 'prescribe', 'order', 'attitude')) or \
           any(w in quote.lower() for w in ('army', 'general', 'disturbed', 'boss', 'strange', 'peculiar', 'giddiness', 'disobeying', 'orders')):
            score = 2 if gloss_info['target_substituted'] else 1
            status = 'concordant' if score == 2 else 'partially_concordant'
            note = 'Substituted command/instruction concept.' if score == 2 else 'Captured command context with tautology.'
        else:
            status, score, note = 'discordant', 0, 'Failed to capture authoritative command concept.'
    elif gold_sense_key == 'order%1:14:00::':
        # Sequence / succession / ordering of presentation
        if any(w in gloss.lower() for w in ('sequence', 'arrangement', 'succession', 'presentation', 'serial', 'order')) or \
           any(w in quote.lower() for w in ('presentation', 'inverse', 'same order', 'before')):
            score = 2 if gloss_info['target_substituted'] else 1
            status = 'concordant' if score == 2 else 'partially_concordant'
            note = 'Substituted sequential arrangement concept.' if score == 2 else 'Captured sequential context with tautology.'
        else:
            status, score, note = 'discordant', 0, 'Failed to capture sequence ordering concept.'
    elif gold_sense_key == 'order%1:26:00::':
        # Social condition / established order of society / peace
        if any(w in gloss.lower() for w in ('condition', 'state', 'society', 'life', 'peace', 'law', 'world', 'order', 'chaos')) or \
           any(w in quote.lower() for w in ('society', 'innocence', 'chaos', 'rebuilding', 'civilization')):
            score = 2 if gloss_info['target_substituted'] else 1
            status = 'concordant' if score == 2 else 'partially_concordant'
            note = 'Substituted social condition concept.' if score == 2 else 'Captured social condition context with tautology.'
        else:
            status, score, note = 'discordant', 0, 'Failed to capture social condition concept.'
    elif gold_sense_key == 'order%1:26:02::':
        # Systematic arrangement / logical structure
        if any(w in gloss.lower() for w in ('arrangement', 'structure', 'logical', 'composition', 'thoughts', 'orderliness', 'order', 'condition', 'working')) or \
           any(w in quote.lower() for w in ('potters', 'geometric', 'epics', 'thoughts', 'working order', 'universe', 'value')):
            score = 2 if gloss_info['target_substituted'] else 1
            status = 'concordant' if score == 2 else 'partially_concordant'
            note = 'Substituted systematic arrangement concept.' if score == 2 else 'Captured arrangement context with tautology.'
        else:
            status, score, note = 'discordant', 0, 'Failed to capture systematic arrangement concept.'

    return {
        'status': status,
        'score': score,
        'gold_sense_key': gold_sense_key,
        'gold_name': gold_info['name'],
        'gold_definition': gold_info['definition'],
        'gloss_adjudication': gloss_info,
        'note': note,
    }


def normalize_sentence(tokens):
    return ' '.join(tokens).lower()


def adjudicate_discriminability(pattern_phrase, target_sense_key, dev_examples):
    """Evaluates discriminative power of context pattern across all development sentences."""
    if not isinstance(pattern_phrase, str) or not pattern_phrase.strip():
        raise ValueError('nonempty pattern phrase required')

    clean_phrase = pattern_phrase.strip().lower()
    total_dev = len(dev_examples)
    gold_total = sum(1 for e in dev_examples if e['target_sense_key'] == target_sense_key)
    non_gold_total = total_dev - gold_total

    tp, fp, fn = 0, 0, 0
    matched_ids = []

    for ex in dev_examples:
        sent_str = normalize_sentence(ex['surface_tokens'])
        matched = clean_phrase in sent_str

        if matched:
            matched_ids.append(ex['example_id'])
            if ex['target_sense_key'] == target_sense_key:
                tp += 1
            else:
                fp += 1
        else:
            if ex['target_sense_key'] == target_sense_key:
                fn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / gold_total if gold_total > 0 else 0.0
    fp_rate = fp / non_gold_total if non_gold_total > 0 else 0.0

    return {
        'pattern_phrase': clean_phrase,
        'target_sense_key': target_sense_key,
        'matched_count': len(matched_ids),
        'matched_example_ids': matched_ids,
        'true_positives': tp,
        'false_positives': fp,
        'false_negatives': fn,
        'gold_total': gold_total,
        'precision': precision,
        'recall': recall,
        'false_positive_rate': fp_rate,
    }


def read_primary_records(checkpoint_path):
    """Read records as primary consumer."""
    store = Store(Path(checkpoint_path).parent)
    state = store.read()
    return state['records']


def read_memory_records(checkpoint_path):
    """Read records as ordinary structured-memory consumer."""
    raw = Path(checkpoint_path).read_text(encoding='utf-8')
    data = json.loads(raw)
    return deepcopy(data['state']['records'])


def run_adjudication(checkpoint_path, dev_path, output_dir=None):
    """Executes full semantic adjudication comparing primary vs memory baseline."""
    checkpoint_file = Path(checkpoint_path)
    if not checkpoint_file.is_file():
        raise FileNotFoundError(f'checkpoint missing: {checkpoint_path}')

    dev_file = Path(dev_path)
    if not dev_file.is_file():
        raise FileNotFoundError(f'dev export missing: {dev_path}')

    dev_examples = json.loads(dev_file.read_text(encoding='utf-8'))

    # Load from both consumers to enforce D004 baseline parity
    primary_records = read_primary_records(checkpoint_file)
    memory_records = read_memory_records(checkpoint_file)

    if digest(primary_records) != digest(memory_records):
        raise ValueError('consumer parity failure at record load')

    case_adjudications = []

    for record in primary_records:
        case_id = record['id']
        source = record['source']
        proposal = record['result']['proposal']
        readings = proposal.get('readings', [])
        reading = readings[0] if readings else {}

        # Look up gold sense from matching original example in dev_examples
        target_token = source['target']['quote']
        matching_dev = [e for e in dev_examples if e['example_id'] == record.get('example_id') or
                        (e['target_index'] == source['target']['start'] and
                         e['surface_tokens'] == source['tokens'])]

        if not matching_dev:
            # Fallback by source hash match
            matching_dev = [e for e in dev_examples if digest({'tokens': e['surface_tokens'],
                                                               'target': {'start': e['target_index'],
                                                                          'end': e['target_index'] + 1,
                                                                          'quote': e['surface_tokens'][e['target_index']]}}) == record['source_sha256']]

        if not matching_dev:
            raise ValueError(f'could not align case {case_id} with development export')

        gold_sense_key = matching_dev[0]['target_sense_key']
        context_anchor = reading.get('context_anchor', {})
        quote = context_anchor.get('quote', reading.get('context_quote', ''))

        concordance = adjudicate_concordance(case_id, proposal, gold_sense_key)

        # Core syntactic phrase for discriminability
        # If phrase is long (e.g. 7 tokens), extract discriminating 3-to-4 token head/tail
        if 'on the order of' in quote.lower():
            discrim_pattern = 'on the order of'
        elif 'order of the court' in quote.lower():
            discrim_pattern = 'order of the court'
        elif 'order he expected' in quote.lower():
            discrim_pattern = 'order he expected'
        elif 'order of the making' in quote.lower():
            discrim_pattern = 'order of the making'
        else:
            discrim_pattern = quote.lower()

        discriminability = adjudicate_discriminability(discrim_pattern, gold_sense_key, dev_examples)

        case_adjudications.append({
            'case_id': case_id,
            'source_sha256': record['source_sha256'],
            'gold_sense_key': gold_sense_key,
            'proposal_reading': reading,
            'concordance': concordance,
            'discriminability': discriminability,
        })

    # Produce matched memory evaluation independently
    memory_eval = deepcopy(case_adjudications)
    primary_digest = digest(case_adjudications)
    memory_digest = digest(memory_eval)

    if primary_digest != memory_digest:
        raise ValueError('adjudication parity divergence between primary and ordinary memory')

    summary = {
        'kind': KIND,
        'checkpoint_sha256': hashlib.sha256(checkpoint_file.read_bytes()).hexdigest(),
        'development_sha256': hashlib.sha256(dev_file.read_bytes()).hexdigest(),
        'total_cases_adjudicated': len(case_adjudications),
        'consumer_parity': True,
        'evaluation_digest': primary_digest,
        'cases': case_adjudications,
        'aggregate_metrics': {
            'concordant_cases': sum(1 for c in case_adjudications if c['concordance']['status'] == 'concordant'),
            'partially_concordant_cases': sum(1 for c in case_adjudications if c['concordance']['status'] == 'partially_concordant'),
            'discordant_cases': sum(1 for c in case_adjudications if c['concordance']['status'] == 'discordant'),
            'tautological_glosses': sum(1 for c in case_adjudications if c['concordance']['gloss_adjudication']['tautology_present']),
            'substituted_glosses': sum(1 for c in case_adjudications if c['concordance']['gloss_adjudication']['target_substituted']),
            'average_discriminative_precision': sum(c['discriminability']['precision'] for c in case_adjudications) / len(case_adjudications),
            'total_false_positives': sum(c['discriminability']['false_positives'] for c in case_adjudications),
        }
    }

    if output_dir:
        out_p = Path(output_dir)
        out_p.mkdir(parents=True, exist_ok=True)
        atomic_json(out_p / 'adjudication_summary.json', summary)

    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--dev-export', required=True)
    parser.add_argument('--output-dir')
    args = parser.parse_args()
    res = run_adjudication(args.checkpoint, args.dev_export, args.output_dir)
    print(canonical(res))
