"""Comparative Baseline Benchmark for LMFT.

Compares the unassisted LMFT capacity and kaleidoscopic prismatic engine
against two simpler baselines across all 33 SemCor development instances:
  - Baseline A: Exact Key-Value Dictionary Lookup (associative table)
  - Baseline B: Naive Bag-of-Words Token Co-occurrence Matcher

Enforces Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during evaluation.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys
import time

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from lmft_lab.local_models import strict_json
from lmft_lab.runtime_store import Store, digest, atomic_json
import kaleidoscopic_generator as kg
import meditative_regulation as mr
import metacognitive_priming as mp
import persistent_disambiguation as pd
import tripartite_funnel as tf

ROOT = Path(__file__).resolve().parents[1]
KIND = "comparative-baseline-benchmark-1"

DEFAULT_CHECKPOINTS = [
    Path(r"C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v5-20261013-001\neutral-state\checkpoint.json"),
    Path(r"C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v6-20261013-001\neutral-state\checkpoint.json"),
]
DEFAULT_DEV_PATH = Path(r"C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json")

STOP_WORDS = {"the", "a", "an", "in", "of", "to", "and", "for", "on", "that", "with", "is", "was", "as", "by", "at"}


class BaselineA_KeyValue:
    """Exact Key-Value Dictionary Baseline: direct string lookup without continuous dials."""
    def __init__(self, compiled_rules):
        self.table = {}
        for r in compiled_rules:
            key = r["exact_quote"].strip().lower()
            if key not in self.table:
                self.table[key] = {
                    "sense_key": r["target_sense_key"],
                    "gloss": r["gloss"],
                }

    def predict(self, sentence_tokens):
        s_text = " ".join(sentence_tokens).lower()
        matches = []
        for quote, entry in self.table.items():
            if quote in s_text:
                matches.append(entry)

        matched_senses = sorted({m["sense_key"] for m in matches})
        if not matched_senses:
            return {"decision": "abstain", "selected_sense": None, "explanation": "No key matched"}
        elif len(matched_senses) == 1:
            return {"decision": "single", "selected_sense": matched_senses[0], "explanation": matches[0]["gloss"]}
        else:
            return {"decision": "ambiguous", "selected_sense": None, "explanation": "Multiple conflicting keys matched"}


class BaselineB_BagOfWords:
    """Naive Bag-of-Words Baseline: unweighted content token overlap without syntactic boundaries."""
    def __init__(self, compiled_rules):
        self.entries = []
        for r in compiled_rules:
            words = set(re.findall(r"\w+", r["exact_quote"].lower())) - STOP_WORDS
            if words:
                self.entries.append({
                    "words": words,
                    "sense_key": r["target_sense_key"],
                    "gloss": r["gloss"],
                })

    def predict(self, sentence_tokens):
        s_words = set(re.findall(r"\w+", " ".join(sentence_tokens).lower())) - STOP_WORDS
        matches = []
        for e in self.entries:
            if e["words"].issubset(s_words):
                matches.append(e)

        matched_senses = sorted({m["sense_key"] for m in matches})
        if not matched_senses:
            return {"decision": "abstain", "selected_sense": None, "explanation": "No token subset matched"}
        elif len(matched_senses) == 1:
            return {"decision": "single", "selected_sense": matched_senses[0], "explanation": matches[0]["gloss"]}
        else:
            return {"decision": "ambiguous", "selected_sense": None, "explanation": "Multiple conflicting senses matched"}


def evaluate_system(predictor, examples, is_lmft=False):
    """Evaluates a predictor across examples and returns standard performance metrics."""
    correct_singletons = 0
    wrong_singletons = 0
    abstentions = 0
    ambiguities = 0
    predictions = []

    t0 = time.perf_counter()
    for ex in examples:
        gold = ex["target_sense_key"]
        tokens = ex["surface_tokens"]

        if is_lmft:
            item = {"id": ex["example_id"], "tokens": tokens, "target_indices": [ex["target_index"]]}
            pred = pd.predict_item(predictor, item)
        else:
            pred = predictor.predict(tokens)

        decision = pred["decision"]
        sense = pred["selected_sense"]

        if decision == "single":
            if sense == gold:
                correct_singletons += 1
            else:
                wrong_singletons += 1
        elif decision == "abstain":
            abstentions += 1
        elif decision == "ambiguous":
            ambiguities += 1

        predictions.append({
            "example_id": ex["example_id"],
            "gold_sense": gold,
            "decision": decision,
            "selected_sense": sense,
        })

    elapsed = time.perf_counter() - t0
    total = len(examples)
    fired = correct_singletons + wrong_singletons
    precision_fired = (correct_singletons / fired) if fired > 0 else 0.0
    accuracy = correct_singletons / total if total > 0 else 0.0
    fp_rate = wrong_singletons / total if total > 0 else 0.0
    ambiguity_rate = ambiguities / total if total > 0 else 0.0

    return {
        "total_instances": total,
        "correct_singletons": correct_singletons,
        "wrong_singletons": wrong_singletons,
        "abstentions": abstentions,
        "ambiguities": ambiguities,
        "accuracy": round(accuracy, 4),
        "precision_on_fired": round(precision_fired, 4),
        "false_positive_rate": round(fp_rate, 4),
        "ambiguity_rate": round(ambiguity_rate, 4),
        "elapsed_seconds": round(elapsed, 4),
        "continuous_stance_actuation": is_lmft,
        "predictions": predictions,
    }


def run_comparative_benchmark(checkpoints=None, dev_path=None, output_dir=None):
    """Executes the full comparative benchmark under Rule D004 matched ordinary memory baseline parity."""
    cp_list = [Path(p) for p in (checkpoints or DEFAULT_CHECKPOINTS)]
    dev_file = Path(dev_path or DEFAULT_DEV_PATH)

    if not dev_file.is_file():
        raise FileNotFoundError(f"Dev export missing: {dev_file}")

    all_rows = strict_json(dev_file.read_text(encoding="utf-8"))
    primary_records = []
    memory_records = []
    checkpoint_hashes = {}

    for cp in cp_list:
        if not cp.is_file():
            raise FileNotFoundError(f"Checkpoint missing: {cp}")
        store = Store(cp.parent)
        primary_state = store.read()
        memory_state = strict_json(cp.read_text(encoding="utf-8"))["state"]

        if digest(primary_state) != digest(memory_state):
            raise ValueError(f"Consumer parity failure at {cp}")

        primary_records.extend(primary_state["records"])
        memory_records.extend(memory_state["records"])
        checkpoint_hashes[str(cp)] = hashlib.sha256(cp.read_bytes()).hexdigest()

    # Compile rules for primary and ordinary memory
    primary_rules = pd.compile_rules(primary_records, all_rows)
    memory_rules = pd.compile_rules(memory_records, all_rows)

    if digest(primary_rules) != digest(memory_rules):
        raise ValueError("Rule compilation parity failure")

    # Evaluate Primary
    lmft_primary = evaluate_system(primary_rules, all_rows, is_lmft=True)
    base_a_primary = evaluate_system(BaselineA_KeyValue(primary_rules), all_rows, is_lmft=False)
    base_b_primary = evaluate_system(BaselineB_BagOfWords(primary_rules), all_rows, is_lmft=False)

    # Evaluate Ordinary Memory Comparator
    lmft_memory = evaluate_system(memory_rules, all_rows, is_lmft=True)
    base_a_memory = evaluate_system(BaselineA_KeyValue(memory_rules), all_rows, is_lmft=False)
    base_b_memory = evaluate_system(BaselineB_BagOfWords(memory_rules), all_rows, is_lmft=False)

    # Verify Rule D004 parity
    if digest(lmft_primary["predictions"]) != digest(lmft_memory["predictions"]):
        raise ValueError("LMFT parity failure")
    if digest(base_a_primary["predictions"]) != digest(base_a_memory["predictions"]):
        raise ValueError("Baseline A parity failure")
    if digest(base_b_primary["predictions"]) != digest(base_b_memory["predictions"]):
        raise ValueError("Baseline B parity failure")

    comparison_table = {
        "LMFT_Capacity_Engine": {
            "accuracy": lmft_primary["accuracy"],
            "precision_on_fired": lmft_primary["precision_on_fired"],
            "false_positive_rate": lmft_primary["false_positive_rate"],
            "ambiguity_rate": lmft_primary["ambiguity_rate"],
            "abstentions": lmft_primary["abstentions"],
            "continuous_stance_actuation": lmft_primary["continuous_stance_actuation"],
            "elapsed_seconds": lmft_primary["elapsed_seconds"],
        },
        "BaselineA_KeyValue_Store": {
            "accuracy": base_a_primary["accuracy"],
            "precision_on_fired": base_a_primary["precision_on_fired"],
            "false_positive_rate": base_a_primary["false_positive_rate"],
            "ambiguity_rate": base_a_primary["ambiguity_rate"],
            "abstentions": base_a_primary["abstentions"],
            "continuous_stance_actuation": base_a_primary["continuous_stance_actuation"],
            "elapsed_seconds": base_a_primary["elapsed_seconds"],
        },
        "BaselineB_BagOfWords_Matcher": {
            "accuracy": base_b_primary["accuracy"],
            "precision_on_fired": base_b_primary["precision_on_fired"],
            "false_positive_rate": base_b_primary["false_positive_rate"],
            "ambiguity_rate": base_b_primary["ambiguity_rate"],
            "abstentions": base_b_primary["abstentions"],
            "continuous_stance_actuation": base_b_primary["continuous_stance_actuation"],
            "elapsed_seconds": base_b_primary["elapsed_seconds"],
        },
    }

    summary = {
        "kind": KIND,
        "development_sha256": hashlib.sha256(dev_file.read_bytes()).hexdigest(),
        "checkpoint_hashes": checkpoint_hashes,
        "total_instances": len(all_rows),
        "consumer_parity": True,
        "evaluation_digest": digest(lmft_primary["predictions"]),
        "comparison_table": comparison_table,
    }

    if output_dir:
        out_path = Path(output_dir)
        out_path.mkdir(parents=True, exist_ok=True)
        atomic_json(out_path / "comparative-benchmark-summary.json", summary)

    return summary


def main():
    parser = argparse.ArgumentParser(description="LMFT Comparative Baseline Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()

    res = run_comparative_benchmark(output_dir=args.output_dir)
    print("\n=== Comparative Baseline Benchmark Results ===")
    print(f"Total instances evaluated: {res['total_instances']}")
    print(f"Consumer Parity Verified: {res['consumer_parity']}")
    print("\nSystem Comparison Table:")
    for sys_name, metrics in res["comparison_table"].items():
        print(f"\n[{sys_name}]")
        for k, v in metrics.items():
            print(f"  {k}: {v}")
    print("\n==============================================\n")


if __name__ == "__main__":
    main()
