"""Existing edge contribution, exact scalar equivalence and downstream limits."""
from copy import deepcopy
import importlib.util
from pathlib import Path
import pytest
from lmft_lab import consistent_attention as circuit,attention
from lmft_lab.runtime_store import digest


def harness():
    spec=importlib.util.spec_from_file_location("seed_harness","experiments/run_seed_contribution.py")
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module


@pytest.mark.parametrize("key",["x"+str(i) for i in range(1,11)])
def test_exact_scalar_scores_actions_and_narrow_edge_ablation(key):
    h=harness(); state=h.prior(); case,records=h.inputs(key); h.retain(state,records)
    before=digest(state); full,traces=circuit.select(state,case)
    scalar,scalar_traces=h.scalar_select(state,case)
    assert full==scalar
    altered=deepcopy(state); altered["mode"]="consistent-no-clarity"
    ablated,ab_traces=circuit.select(altered,case); scalar_ab,scalar_ab_traces=h.scalar_select(state,case,True)
    assert ablated==scalar_ab
    actual=[r for r in traces if "score" in r]; expected=[r for r in scalar_traces if "score" in r]
    for left,right in zip(actual,expected): assert left["score"]==right["score"]
    for left,right in zip([r for r in ab_traces if "score" in r],[r for r in scalar_ab_traces if "score" in r]): assert left["score"]==right["score"]
    for full_row,ab_row in zip(actual,[r for r in ab_traces if "score" in r]):
        f,a=full_row["propagation"],ab_row["propagation"]
        assert digest(f["direct_frame"])==digest(a["direct_frame"])
        differences=[(x,y) for x,y in zip(f["relationships"],a["relationships"]) if x!=y]
        assert len(differences)==1
        x,y=differences[0]; assert x["source_id"]==attention.C and x["target_id"]==circuit.E
        assert x["active"] and not y["active"]
        assert {k:v for k,v in x.items() if k!="active"}=={k:v for k,v in y.items() if k!="active"}
    assert digest(state)==before


def test_utility_hurts_and_downstream_decisions_tie_without_repairs():
    h=harness(); full=[h.evaluate(h.prior(),key,"intact") for key in h.DEFS]
    ab=[h.evaluate(h.prior(),key,"ablated") for key in h.DEFS]
    assert sum(r["newly_resolved_questions"] for r in full)==4
    assert sum(r["newly_resolved_questions"] for r in ab)==7
    assert [r["after"]["decision"] for r in full]==[r["after"]["decision"] for r in ab]==h.EXPECTED_DECISIONS
    assert all(all(r["checks"].values()) for r in full+ab)


def test_no_fresh_learning_or_oracle_during_selection(monkeypatch):
    h=harness(); state=h.prior(); case,records=h.inputs("x1"); h.retain(state,records)
    monkeypatch.setattr(h,"selected_reply",lambda *args:pytest.fail("hidden reply accessed"))
    full,_=circuit.select(state,case); scalar,_=h.scalar_select(state,case)
    assert full==scalar
    assert state["weights"]=={"A":.25,"B":.75,"D":.5}
    assert state["branches"]["shielded"]["score"]==1/3 and state["branches"]["unshielded"]["score"]==-1/3


def test_attainable_support_grid_exact_scalar_reduction():
    from itertools import product
    h=harness(); values=((),(True,),(False,),(False,True))
    case,_=h.inputs("x1")
    for field in ("shielded","payload_valid"):
        parts=circuit.PARTS[field]
        for combinations in product(values,repeat=len(parts)):
            for route in ("A","B","D"):
                state=h.prior(); records=[]
                for part,observations in zip(parts,combinations):
                    for i,value in enumerate(observations): records.append(h.record(field+part+str(i),"x1",field,part,value))
                h.retain(state,records); public=deepcopy(case)
                for candidate in public["candidates"]: candidate["route"]=route
                for disabled in (False,True):
                    state["mode"]="consistent-no-clarity" if disabled else "consistent-full"
                    actual,traces=circuit.select(state,public); expected,scalar=h.scalar_select(state,public,disabled)
                    assert actual==expected
                    assert [r["score"] for r in traces if "score" in r]==[r["score"] for r in scalar if "score" in r]


def test_persisted_public_inputs_preserve_explicit_case_order(tmp_path):
    import json
    from lmft_lab.runtime_store import atomic_json
    h=harness(); order=["x1","x2","x10"]
    public={key:{"case":h.inputs(key)[0],"initial_records":h.inputs(key)[1]} for key in order}
    atomic_json(tmp_path/"frozen-prior.json",h.prior())
    atomic_json(tmp_path/"frozen-case-inputs.json",{"case_order":order,"cases":public})
    h.worker(tmp_path)
    results=json.loads((tmp_path/"restarted-evaluations.json").read_text())
    assert [r["case_id"] for r in results["conditions"]["intact"]]==order
