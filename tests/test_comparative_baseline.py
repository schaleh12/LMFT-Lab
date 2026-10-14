"""Unit tests for Comparative Baseline Benchmark Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

import comparative_baseline_benchmark as cbb


def test_baseline_a_key_value_lookup():
    """Baseline A accurately retrieves senses on exact quote and abstains on unknown."""
    rules = [
        {"exact_quote": "order of the court", "target_sense_key": "order%1:10:00::", "gloss": "judicial decree"},
        {"exact_quote": "on the order of", "target_sense_key": "order%1:07:01::", "gloss": "magnitude"},
    ]
    base_a = cbb.BaselineA_KeyValue(rules)

    pred1 = base_a.predict(["The", "judge", "issued", "an", "order", "of", "the", "court", "."])
    assert pred1["decision"] == "single"
    assert pred1["selected_sense"] == "order%1:10:00::"

    pred_abstain = base_a.predict(["The", "river", "flowed", "peacefully", "."])
    assert pred_abstain["decision"] == "abstain"
    assert pred_abstain["selected_sense"] is None


def test_baseline_b_bag_of_words_matcher():
    """Baseline B matches content word subsets and detects ambiguity on collision."""
    rules = [
        {"exact_quote": "court order", "target_sense_key": "order%1:10:00::", "gloss": "judicial decree"},
        {"exact_quote": "military order", "target_sense_key": "order%1:10:03::", "gloss": "military command"},
    ]
    base_b = cbb.BaselineB_BagOfWords(rules)

    pred_court = base_b.predict(["The", "court", "gave", "an", "urgent", "order", "."])
    assert pred_court["decision"] == "single"
    assert pred_court["selected_sense"] == "order%1:10:00::"

    # Sentence with both keywords triggers ambiguity
    pred_ambig = base_b.predict(["The", "military", "and", "the", "court", "gave", "an", "order", "."])
    assert pred_ambig["decision"] == "ambiguous"
    assert pred_ambig["selected_sense"] is None


def test_comparative_benchmark_parity_and_metrics():
    """Full comparative benchmark achieves Rule D004 parity and verifies H1 and H2."""
    summary = cbb.run_comparative_benchmark()

    assert summary["consumer_parity"] is True
    assert summary["total_instances"] == 33

    table = summary["comparison_table"]
    assert "LMFT_Capacity_Engine" in table
    assert "BaselineA_KeyValue_Store" in table
    assert "BaselineB_BagOfWords_Matcher" in table

    # H1: Baseline A achieves accuracy parity with LMFT
    assert table["LMFT_Capacity_Engine"]["accuracy"] == 1.0
    assert table["BaselineA_KeyValue_Store"]["accuracy"] == 1.0

    # H2: Baseline B suffers from ambiguities
    assert table["BaselineB_BagOfWords_Matcher"]["ambiguity_rate"] > 0.0
    assert table["BaselineB_BagOfWords_Matcher"]["accuracy"] < 1.0

    # H3: Only LMFT provides continuous stance actuation
    assert table["LMFT_Capacity_Engine"]["continuous_stance_actuation"] is True
    assert table["BaselineA_KeyValue_Store"]["continuous_stance_actuation"] is False
