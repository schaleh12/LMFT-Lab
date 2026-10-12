"""Exact registered later reports; registration is not a truth claim."""
from . import correction_fixture as fixture
from .runtime_store import digest

def late_record(case):
    return {'evidence_id': 'late/' + case['case_id'] + '/shielded/check1',
            'case_id': case['case_id'], 'scope': 'batch-1', 'question': 'shielded',
            'part': 'check1', 'value': False, 'source': fixture.SOURCE}

class LateRegistry:
    SOURCE = fixture.SOURCE

    def __init__(self):
        self.calls = 0

    def admitted(self, record):
        self.calls += 1
        fields = {'evidence_id', 'case_id', 'scope', 'question', 'part', 'value', 'source'}
        if (type(record) is not dict or set(record) != fields
                or type(record['value']) is not bool
                or any(type(record[k]) is not str for k in fields - {'value'})):
            return False
        return any(digest(record) == digest(late_record(fixture.public_case(k))) for k in ('c1', 'c9'))
