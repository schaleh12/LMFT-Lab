"""Independent truth-table/mask kernel; never imports/calls the primary kernel."""
import context_applicability_contract as c

# Context columns 00,01,10,11. Explicit tables, not primary expression evaluation.
TABLES = ((0, 0, 0, 0), (1, 1, 1, 1), (0, 0, 1, 1),
          (1, 1, 0, 0), (0, 1, 0, 1), (1, 0, 1, 0))


def analyze(records):
    mask = 63
    witnesses = [[] for _ in TABLES]
    for row in records:
        column = row['context'][0] * 2 + row['context'][1]
        needed = int(row['raw'] != row['reference'])
        allowed = 0
        for index, table in enumerate(TABLES):
            if table[column] == needed:
                allowed |= 1 << index
            else:
                witnesses[index].append(row['evidence_id'])
        mask &= allowed
    return {'survivors': [name for i, name in enumerate(c.FAMILY) if mask & (1 << i)],
            'rejection_witnesses': dict(zip(c.FAMILY, witnesses))}


def predict(survivors, ctx):
    if not c.context(ctx):
        return {'status': 'unknown_context', 'votes': [], 'mapping': None}
    column = ctx[0] * 2 + ctx[1]
    active = {c.FAMILY.index(name) for name in survivors}
    votes = [row[column] for i, row in enumerate(TABLES) if i in active]
    distinct = set(votes)
    if not distinct:
        return {'status': 'unsupported', 'votes': votes, 'mapping': None}
    if len(distinct) != 1:
        return {'status': 'mapping_ambiguous', 'votes': votes, 'mapping': None}
    return {'status': 'consensus', 'votes': votes, 'mapping': distinct.pop()}
