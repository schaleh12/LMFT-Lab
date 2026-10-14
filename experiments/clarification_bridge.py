"""Closed-Loop Supervised Clarification Bridge Benchmark.

Evaluates automated end-to-end question detection, proposal generation, deterministic
validation gate enforcement (Rule D003), and atomic runtime state advancement.

Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted evaluation.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.judgment import probe, newborn, SAMPLES
from lmft_lab.runtime import advance, initial_state, software_manifest, FixtureModels
from lmft_lab.clarification_bridge import (
    scan_open_questions,
    default_evidence_validator,
    LocalClarificationProposer,
    execute_bridge_cycle,
    OrdinaryMemoryClarificationComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "clarification-bridge-benchmark-1"


def run_clarification_bridge_study(output_dir=None):
    """Executes closed-loop bridge benchmark across missing-evidence and conflicting-evidence cycles."""
    # 1. Initialize individual
    state = initial_state("bridge-indiv", True, software_manifest(None, "fixture"))
    models = FixtureModels()
    comparator = OrdinaryMemoryClarificationComparator(state)
    
    study_events = []
    
    # 2. Cycle 1: Submit observation without evidence -> triggers 'missing-evidence' clarification
    obs1 = {
        "schema_version": 1,
        "id": "obs-bridge-01",
        "sender": "operator",
        "source": "authored-fixture",
        "type": "observation",
        "content": {"text": "Evaluate first synthetic channel agreement."},
    }
    state = advance(state, (1, obs1, None, json.dumps(obs1)), models)
    comparator.state = advance(comparator.state, (1, obs1, None, json.dumps(obs1)), models)
    assert digest(state) == digest(comparator.state)
    
    q1 = scan_open_questions(state)
    assert len(q1) == 1
    assert q1[0]["issue"] == "missing-evidence"
    study_events.append({"event": "observation_1", "open_questions": q1})
    
    # 3. Bridge Cycle 1: Automated proposal, validation, and reply submission
    proposer = LocalClarificationProposer()
    state, logs1 = execute_bridge_cycle(state, proposer, models=models)
    comparator.state, c_logs1 = comparator.step(proposer)
    assert digest(state) == digest(comparator.state)
    assert digest(logs1) == digest(c_logs1)
    assert len(scan_open_questions(state)) == 0
    assert probe(state["judgment"])["decision"] == "support"
    study_events.append({"event": "bridge_cycle_1", "logs": logs1, "judgment": probe(state["judgment"])})
    
    # 4. Cycle 2: Submit contradictory evidence manually -> triggers 'conflicting-evidence' clarification
    ch_b, ref_b = SAMPLES["sample-b"]
    obs2 = {
        "schema_version": 1,
        "id": "obs-bridge-02",
        "sender": "operator",
        "source": "authored-fixture",
        "type": "observation",
        "content": {
            "text": "Submit contrary sample-b.",
            "evidence": {"sample_id": "sample-b", "channel": ch_b, "reference": ref_b},
        },
    }
    state = advance(state, (state["cursor"] + 1, obs2, None, json.dumps(obs2)), models)
    comparator.state = advance(comparator.state, (comparator.state["cursor"] + 1, obs2, None, json.dumps(obs2)), models)
    assert digest(state) == digest(comparator.state)
    
    q2 = scan_open_questions(state)
    assert len(q2) == 1
    assert q2[0]["issue"] == "conflicting-evidence"
    study_events.append({"event": "observation_2_conflict", "open_questions": q2})
    
    # 5. Bridge Cycle 2: Automated resolution with third eligible sample
    state, logs2 = execute_bridge_cycle(state, proposer, models=models)
    comparator.state, c_logs2 = comparator.step(proposer)
    assert digest(state) == digest(comparator.state)
    assert digest(logs2) == digest(c_logs2)
    assert len(scan_open_questions(state)) == 0
    study_events.append({"event": "bridge_cycle_2", "logs": logs2, "judgment": probe(state["judgment"])})
    
    # 6. Verify seed invariant
    assert len(list(_inventory())) == 40
    
    summary = {
        "kind": KIND,
        "individual_id": state["individual_id"],
        "total_cycles_executed": 4,
        "open_questions_resolved": 2,
        "final_judgment": probe(state["judgment"]),
        "consumer_parity": True,
        "evaluation_digest": digest(state),
        "study_events": study_events,
    }
    
    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "clarification-bridge-summary.json", summary)
        
    return summary


def main():
    parser = argparse.ArgumentParser(description="Closed-Loop Supervised Clarification Bridge Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()
    
    res = run_clarification_bridge_study(output_dir=args.output_dir)
    print("\n=== Closed-Loop Clarification Bridge Results ===")
    print(f"Individual: {res['individual_id']}")
    print(f"Total cycles executed: {res['total_cycles_executed']}")
    print(f"Open questions resolved: {res['open_questions_resolved']}")
    print(f"Final Judgment Decision: {res['final_judgment']['decision']} (score: {res['final_judgment']['score']})")
    print(f"Consumer Parity Verified: {res['consumer_parity']}")
    print("================================================\n")


if __name__ == "__main__":
    main()
