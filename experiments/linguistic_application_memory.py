"""Ordinary example memory: independent per-label candidate construction/scans."""
from linguistic_application import features, cue_id


def memory_table(examples):
    token_rows = [(e, features(e)) for e in examples]
    labels = sorted(set(e['sense'] for e in examples))
    table = {}
    for label in labels:
        candidates = set()
        for example, tokens in token_rows:
            if example['sense'] != label:
                continue
            for left in tokens:
                candidates.add((left,))
                for right in tokens:
                    if left < right:
                        candidates.add((left, right))
        rules = []
        for cue in sorted(candidates):
            positives, negatives, documents = [], [], set()
            for example, tokens in token_rows:
                if all(word in tokens for word in cue):
                    if example['sense'] == label:
                        positives.append(example['id'])
                        documents.add(example['document_id'])
                    else:
                        negatives.append(example['id'])
            reasons = ([] if not negatives else ['counterexample'])
            if len(documents) < 2:
                reasons.append('insufficient_documents')
            rules.append({'id': cue_id(label, cue), 'cue': list(cue),
                          'positive': sorted(positives), 'negative': sorted(negatives),
                          'positive_documents': sorted(documents),
                          'status': 'active' if not reasons else 'rejected', 'reasons': reasons})
        table[label] = {'lifecycle': 'active' if any(r['status'] == 'active' for r in rules)
                        else 'unsupported', 'rules': rules}
    return table
