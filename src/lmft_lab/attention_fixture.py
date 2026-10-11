"""Registered synthetic verifier. Selection must not import this module."""
from copy import deepcopy
from . import contextual

# shielded, actual success, route A available, route B available
_TRUTH = {"p1": (True, True, False, True), "t1": (True, True, False, True),
          "t2": (False, False, False, True), "h1": (True, True, False, True),
          "h2": (False, False, False, True), "h3": (True, False, False, True),
          "h4": (False, True, False, True), "h5": (True, True, False, False)}
IDS = ("p1", "t1", "t2", "h1", "h2", "h3", "h4", "h5", "n1")
CANDIDATES = [{"id":"0-D", "field":"color", "route":"D"},
              {"id":"1-A", "field":"shielded", "route":"A"},
              {"id":"2-B", "field":"shielded", "route":"B"}]

def public_case(key):
    if key not in IDS: raise ValueError("unknown fixture case")
    reports = [{"id":key+"-"+field+str(i), "source":"sensor-"+str(i),
                "field":field, "value":bool(i)} for field in ("shielded","color") for i in (0,1)]
    if key == "n1": reports = [reports[0]]
    return {"case_id":key, "reports":reports+[deepcopy(reports[0])],
            "candidates":deepcopy(CANDIDATES)}

def verify(case_id, candidate):
    # Called only after a concrete request has been selected and committed.
    if candidate not in CANDIDATES or case_id not in _TRUTH: raise ValueError("unregistered request")
    shielded, _, a, b = _TRUTH[case_id]
    route = candidate["route"]
    value = True if route == "D" else shielded if (a if route == "A" else b) else None
    return {"evidence_id":case_id+"/"+route, "case_id":case_id,
            "candidate":deepcopy(candidate), "value":value, "verifier":"registered-attention-1"}

def validate_reply(record, case_id, candidate):
    return (isinstance(record,dict) and (record.get("value") is None or type(record.get("value")) is bool)
            and record == verify(case_id,candidate))

def actual_success(case_id):
    return _TRUTH[case_id][1]

def training_record(key):
    return contextual.outcome(key)
