"""Explicit-expression primary kernel. No device or memory imports."""
import context_applicability_contract as c


def value(hypothesis, ctx):
    if hypothesis == '0':
        return 0
    if hypothesis == '1':
        return 1
    if hypothesis == 'c0':
        return ctx[0]
    if hypothesis == 'not c0':
        return 1 - ctx[0]
    if hypothesis == 'c1':
        return ctx[1]
    if hypothesis == 'not c1':
        return 1 - ctx[1]
    raise ValueError('unknown hypothesis')


def analyze(records):
    witnesses = {h: [r['evidence_id'] for r in records
                     if (r['raw'] ^ value(h, r['context'])) != r['reference']]
                 for h in c.FAMILY}
    return {'survivors': [h for h in c.FAMILY if not witnesses[h]],
            'rejection_witnesses': witnesses}


def predict(survivors, ctx):
    if not c.context(ctx):
        return {'status': 'unknown_context', 'votes': [], 'mapping': None}
    votes = [value(h, ctx) for h in survivors]
    result = votes[0] if votes and all(v == votes[0] for v in votes) else None
    return {'status': 'unsupported' if not votes else 'mapping_ambiguous' if result is None else 'consensus',
            'votes': votes, 'mapping': result}
