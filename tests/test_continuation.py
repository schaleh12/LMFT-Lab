"""Continued revision, frozen control, cache and question lifecycle regressions."""
from copy import deepcopy
import json
import pytest
from experiments.continuation_inputs import SCENARIOS, initial, batches, message
from lmft_lab import outcome_correction as c, outcome_fixture as f
from lmft_lab.runtime import initial_state, software_manifest, advance, run
from lmft_lab.runtime_store import Store, digest


def step(state,m):
    return advance(state,(state["cursor"]+1,m,None,json.dumps(m)),None)


def prepared(name,mode="outcome-lmft",frozen=False):
    manifest=software_manifest(None,"fixture")
    if frozen:manifest["freeze_outcomes_after_correction"]=True
    state=initial_state("continuation",True,manifest,mode)
    for m in initial(name):state=step(state,m)
    return state


@pytest.mark.parametrize("name",SCENARIOS)
@pytest.mark.parametrize("condition",["lmft","memory","frozen"])
def test_stage_scores_counts_and_invariants(name,condition):
    state=prepared(name,"outcome-memory" if condition=="memory" else "outcome-lmft",condition=="frozen")
    before=deepcopy(state);spec=SCENARIOS[name];key=spec["key"]
    for label,items in batches(name):
        old=deepcopy(state)
        for m in items:state=step(state,m)
        current=state["judgment"];result=c.snapshot(current)["shielded"]
        if label.startswith("new-"):
            i=int(label[4:]);score,count,decision=spec["corrected"] if condition=="frozen" else spec["expected"][i]
            assert (result["score"],result["count"],result["decision"])==(float(score),count,decision)
            assert state["receipts"][-2]["status"] == ("evaluation_cache_hit" if condition=="frozen" else "evaluated")
            assert state["receipts"][-1]["status"] == "evaluation_cache_hit"
        if label in ("duplicates","conflicts","scope"):
            assert c.snapshot(old["judgment"])["shielded"]==result
            assert old["questions"]==state["questions"]
        if label in ("duplicates","conflicts"):
            assert old["judgment"]["ledger"]==current["ledger"]
            assert old["judgment"]["recomputations"]==current["recomputations"]
        assert all(current["ledger"][eid]==entry for eid,entry in before["judgment"]["ledger"].items())
        assert current["corrections"]==before["judgment"]["corrections"]
    if condition=="frozen":
        assert c.state_ref(state["judgment"])==c.state_ref(before["judgment"])
    assert len(state["judgment"]["ledger"])==len(state["judgment"]["heads"])+1
    assert state["birth"]==before["birth"]


def test_reopen_after_correction_without_new_request_budget():
    state=prepared("same-category");qid=state["judgment"]["cases"]["o12-warm"]["request"]
    assert state["questions"][qid]["status"]=="resolved_by_correction"
    for m in batches("same-category")[0][1]:state=step(state,m)
    assert state["questions"][qid]["status"]=="open"
    assert state["questions"][qid]["reopened_by"]=="o8/event-1"
    assert len(state["questions"])==1
    assert state["outbox"][-1]["type"]=="response"
    assert c.snapshot(state["judgment"])["shielded"]["score"]==.2


def test_new_evidence_does_not_restore_old_corrected_head():
    state=prepared("crossing")
    state=step(state,message("new","evidence",f.initial_records("o8")[0]))
    assert state["judgment"]["heads"]["o2/event-1"]=="replacement/o2-a"
    assert set(state["judgment"]["branches"]["shielded"]["evidence"])=={"o2/event-1","o8/event-1"}


def test_freeze_is_after_accepted_not_rejected_correction():
    state=initial_state("gate",True,{"freeze_outcomes_after_correction":True},"outcome-lmft")
    state=step(state,message("initial","evidence",f.initial_records("o5")[0]))
    state=step(state,message("rejected","correction",f.corrections("o5")[0]))
    state=step(state,message("new","evidence",f.initial_records("o8")[0]))
    assert c.snapshot(state["judgment"])["shielded"]["count"]==2


def test_frozen_control_cannot_change_on_restart(tmp_path):
    state=prepared("crossing",frozen=True)
    state["manifest"].update(outcome_correction_policy=c.load_policy(), experiment="outcome-lmft", fixture_rule=c.RULE)
    store=Store(tmp_path);store.commit(state)
    with pytest.raises(ValueError,match="Code/config/control changed"):
        run(tmp_path,mode="fixture",experiment="outcome-lmft",freeze_outcomes_after_correction=False)
    assert digest(store.inspect())==digest(state)


def test_probes_and_new_evidence_do_not_read_hidden_truth(monkeypatch):
    monkeypatch.setattr(f,"actual_success",lambda *a:pytest.fail("hidden outcome leakage"))
    state=prepared("crossing")
    for _,items in batches("crossing"):
        for m in items:state=step(state,m)
    before=digest(state)
    c.predict(state["judgment"],f.public_case("o2","fresh-1"))
    assert digest(state)==before


@pytest.mark.parametrize("point",["before_replace","after_replace"])
def test_atomic_new_outcome_after_correction(tmp_path,point):
    state=prepared("same-category");store=Store(tmp_path);store.commit(state)
    m=batches("same-category")[0][1][0];changed=step(state,m)
    def fault(where):
        if where==point:raise RuntimeError("interrupted")
    with pytest.raises(RuntimeError):store.commit(changed,fault=fault)
    restored=store.inspect()
    assert digest(restored)==digest(state if point=="before_replace" else changed)
    if point=="before_replace":restored=step(restored,m)
    assert restored["judgment"]==changed["judgment"] and restored["questions"]==changed["questions"]
    assert step(restored,m)["judgment"]==changed["judgment"]
