"""Coordinator-only commanded reference and wiring fixture; no learner imports."""
from copy import deepcopy
import context_applicability_contract as c

WORLDS = ('pass', 'invert', 'switch0-high', 'switch0-low', 'switch1-high', 'switch1-low')
TEMPLATES = ('complete', 'cross', 'contradiction', 'second_absent', 'first_absent', 'duplicate', 'foreign')


def measure(wiring, ctx, commanded):
    # Synthetic reference is independently commanded; wiring only affects raw channel.
    reference = commanded
    if wiring == 'pass':
        raw = commanded
    elif wiring == 'invert':
        raw = 1 - commanded
    elif wiring == 'switch0-high':
        raw = (1 - commanded) if ctx[0] == 1 else commanded
    elif wiring == 'switch0-low':
        raw = (1 - commanded) if ctx[0] == 0 else commanded
    elif wiring == 'switch1-high':
        raw = (1 - commanded) if ctx[1] == 1 else commanded
    elif wiring == 'switch1-low':
        raw = (1 - commanded) if ctx[1] == 0 else commanded
    else:
        raise ValueError('unknown private wiring')
    return raw, reference


def calibrations(wiring, schedule, flip):
    raw, reference = measure(wiring, [0, 0], flip)
    initial = c.calibration('cal-0', [0, 0], raw, reference, 'initial')
    ctx, available = c.SCHEDULES[schedule]
    follow = None
    if available:
        raw, reference = measure(wiring, ctx, 1 - flip)
        follow = c.calibration('cal-1', ctx, raw, reference, 'followup')
    return initial, follow


def evaluation(wiring):
    cases = []; labels = []
    for ctx in c.CONTEXTS:
        for target in (0, 1):
            raw, reference = measure(wiring, ctx, target)
            for template in TEMPLATES:
                key = f'e{len(cases):03}'
                first = c.record(key+'a', key, 'first', target)
                second = c.record(key+'b', key, 'second', raw)
                records = [first, second]
                if template == 'cross':
                    first['value'] = 1 - target
                elif template == 'contradiction':
                    records.append(c.record(key+'c', key, 'second', 1 - raw))
                elif template == 'second_absent':
                    records = [first]
                elif template == 'first_absent':
                    records = [second]
                elif template == 'duplicate':
                    records = [first, second, deepcopy(first), deepcopy(second)]
                elif template == 'foreign':
                    second['scope'] = 'foreign'
                cases.append({'id': key, 'scope': 'evaluation', 'context': list(ctx), 'records': records})
                labels.append({'context': list(ctx), 'target': reference, 'template': template,
                               'oracle_resolved': template in ('complete', 'duplicate')})
    return cases, labels
