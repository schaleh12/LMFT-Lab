"""Unit tests for Multi-Lemma Polysemy Arbiter & Sentence-Level Composition Engine.

Verifies:
1. Clean multi-target resolution across compound sentences containing both 'order' and 'bank'.
2. Zero cross-anchor contamination or keyword bleed.
3. Harmonic multi-register composition through the Tripartite Funnel.
4. Honest abstention on unanchored or out-of-distribution contexts.
5. Matched ordinary-memory baseline parity (Rule D004).
6. Invariance of the canonical 40 founding nodes (Rule D001).
"""
import pytest
from lmft_lab.birth import _inventory
from lmft_lab.multi_lemma_arbiter import (
    evaluate_sentence,
    OrdinaryMemoryArbiter,
    ORDER_CAPACITY_RULES,
    BANK_CAPACITY_RULES,
)


COMPOUND_BENCHMARK_CASES = [
    # Case 1: Commercial Bank (Financial) + Court Order (Command)
    {
        "id": "compound-case-01",
        "text": "The commercial bank received a strict court order to freeze the assets.",
        "expected_targets": [
            {"lemma": "bank", "sense": "bank%1:14:00::", "decision": "single"},
            {"lemma": "order", "sense": "order%1:10:00::", "decision": "single"},
        ],
        "expected_register": "Authoritative & Methodical Synthesis",
    },
    # Case 2: River Bank (Embankment) + Placed an Order (Commercial)
    {
        "id": "compound-case-02",
        "text": "They placed an order for fishing gear while camping along the river bank.",
        "expected_targets": [
            {"lemma": "order", "sense": "order%1:10:01::", "decision": "single"},
            {"lemma": "bank", "sense": "bank%1:17:01::", "decision": "single"},
        ],
        "expected_register": "Communal & Methodical Synthesis",
    },
    # Case 3: Canal Bank (Embankment) + Rank and Order (Sequence)
    {
        "id": "compound-case-03",
        "text": "The patrol marched in rank and order along the steep bank of the canal.",
        "expected_targets": [
            {"lemma": "order", "sense": "order%1:14:00::", "decision": "single"},
            {"lemma": "bank", "sense": "bank%1:17:01::", "decision": "single"},
        ],
        "expected_register": "Communal & Methodical Synthesis",
    },
    # Case 4: Blood Bank (Reserve) + Emergency Order of Supplies (Commercial Requisition)
    {
        "id": "compound-case-04",
        "text": "The regional blood bank urgently requested an order of emergency plasma supplies.",
        "expected_targets": [
            {"lemma": "bank", "sense": "bank%1:14:01::", "decision": "single"},
            {"lemma": "order", "sense": "order%1:10:01::", "decision": "single"},
        ],
        "expected_register": "Authoritative & Methodical Synthesis",
    },
    # Case 5: Investment Bank (Financial) + Order of Magnitude (Degree/Scale)
    {
        "id": "compound-case-05",
        "text": "The investment bank calculated that the market shift was an order of magnitude higher.",
        "expected_targets": [
            {"lemma": "bank", "sense": "bank%1:14:00::", "decision": "single"},
            {"lemma": "order", "sense": "order%1:07:01::", "decision": "single"},
        ],
        "expected_register": "Equilibrated & Methodical Synthesis",
    },
]

SINGLE_AND_CONTROL_CASES = [
    # Single target: Bank only
    {
        "id": "single-bank",
        "text": "She deposited money at the commercial bank yesterday morning.",
        "expected_targets": [
            {"lemma": "bank", "sense": "bank%1:14:00::", "decision": "single"},
        ],
        "expected_register": "Methodical & Pragmatic",
    },
    # Single target: Order only
    {
        "id": "single-order",
        "text": "The judge issued a court order during the morning session.",
        "expected_targets": [
            {"lemma": "order", "sense": "order%1:10:00::", "decision": "single"},
        ],
        "expected_register": "Authoritative & Chivalrous",
    },
    # Ambiguous / unanchored: Both targets present but zero matching anchors
    {
        "id": "ambiguous-targets",
        "text": "He walked past the bank thinking about an order he had heard about.",
        "expected_targets": [
            {"lemma": "bank", "sense": None, "decision": "abstain"},
            {"lemma": "order", "sense": None, "decision": "abstain"},
        ],
        "expected_register": "Neutral Observant Silence",
    },
    # Out of domain: Neither target present
    {
        "id": "out-of-domain",
        "text": "A warm breeze gently swayed the pines on the mountain crest.",
        "expected_targets": [],
        "expected_register": "Neutral Observant Silence",
    },
]


def test_compound_sentences_resolution():
    """Verifies that compound sentences resolve all targets accurately with zero cross-talk."""
    for case in COMPOUND_BENCHMARK_CASES:
        res = evaluate_sentence(case["text"])
        assert res["total_targets_detected"] == len(case["expected_targets"]), f"Target count mismatch on {case['id']}"
        
        for exp, act in zip(case["expected_targets"], res["target_resolutions"]):
            assert act["lemma"] == exp["lemma"]
            assert act["decision"] == exp["decision"]
            assert act["selected_sense"] == exp["sense"], f"Sense mismatch for {exp['lemma']} in {case['id']}"

        assert res["composition"]["composite_register"] == case["expected_register"], f"Register mismatch in {case['id']}"


def test_single_and_control_cases():
    """Verifies single-target resolution and calibrated honest abstentions."""
    for case in SINGLE_AND_CONTROL_CASES:
        res = evaluate_sentence(case["text"])
        assert res["total_targets_detected"] == len(case["expected_targets"]), f"Target count mismatch on {case['id']}"
        
        for exp, act in zip(case["expected_targets"], res["target_resolutions"]):
            assert act["lemma"] == exp["lemma"]
            assert act["decision"] == exp["decision"]
            assert act["selected_sense"] == exp["sense"]

        assert res["composition"]["composite_register"] == case["expected_register"]


def test_ordinary_memory_baseline_parity():
    """Verifies byte-for-byte decision parity with the matched ordinary-memory baseline (Rule D004)."""
    baseline = OrdinaryMemoryArbiter()
    
    all_cases = COMPOUND_BENCHMARK_CASES + SINGLE_AND_CONTROL_CASES
    for case in all_cases:
        lmft_res = evaluate_sentence(case["text"])
        mem_res = baseline.evaluate(case["text"])
        
        assert lmft_res["total_targets_detected"] == mem_res["total_targets_detected"]
        for lr, mr in zip(lmft_res["target_resolutions"], mem_res["target_resolutions"]):
            assert lr["lemma"] == mr["lemma"]
            assert lr["token_index"] == mr["token_index"]
            assert lr["decision"] == mr["decision"]
            assert lr["selected_sense"] == mr["selected_sense"]


def test_frozen_seed_invariant_preserved():
    """Verifies that the canonical 40-node founding seed remains strictly invariant (Rule D001)."""
    inventory = list(_inventory())
    assert len(inventory) == 40
    domains = {item[2] for item in inventory}
    assert domains == {"cultural", "philosophical", "experiential", "psychological"}
    
    # Verify contemplation
    contemplation = [item for item in inventory if item[1] == "Contemplation"]
    assert len(contemplation) == 1
    assert contemplation[0][3] == "psychological"
