"""Interactive Dialogue Prism for LMFT.

Connects the full unassisted capacity memory, homeostatic regulation,
tripartite psychological funnel, and kaleidoscopic linguistic prism
to real-time dynamic text queries.

Twists the 3 lenses in real time:
  - Contemplation Lens (theta_C): Sensory tone & cognitive temperature
  - Truth Lens (theta_T): Metaphysical depth & empirical grounding
  - Will Lens (theta_W): Social delivery & actionable strategy

Enforces Rule D001 (frozen 40-node canonical seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted projection.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from lmft_lab.local_models import strict_json
from lmft_lab.runtime_store import Store, digest
import kaleidoscopic_generator as kg
import meditative_regulation as mr
import metacognitive_priming as mp
import persistent_disambiguation as pd
import tripartite_funnel as tf

ROOT = Path(__file__).resolve().parents[1]
KIND = "interactive-dialogue-prism-1"

DEFAULT_CHECKPOINTS = [
    Path(r"C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v5-20261013-001\neutral-state\checkpoint.json"),
    Path(r"C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v6-20261013-001\neutral-state\checkpoint.json"),
]
DEFAULT_DEV_PATH = Path(r"C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json")


def tokenize_input(text):
    """Simple deterministic tokenization for dialogue input."""
    # Split words and punctuation deterministically
    tokens = re.findall(r"\w+|[^\w\s]", text)
    return tokens if tokens else [text.strip()]


def locate_target_indices(tokens, targets=('order', 'orders')):
    """Locates target token indices in token stream, or defaults to first token."""
    indices = [i for i, tok in enumerate(tokens) if tok.lower() in targets]
    return indices if indices else [0]


def load_rules_from_checkpoints(checkpoints=None, dev_path=None):
    """Loads and compiles rules from neutral checkpoint archives deterministically."""
    cp_list = [Path(p) for p in (checkpoints or DEFAULT_CHECKPOINTS)]
    dev_file = Path(dev_path or DEFAULT_DEV_PATH)

    if not dev_file.is_file():
        raise FileNotFoundError(f"Development export missing: {dev_file}")

    all_rows = strict_json(dev_file.read_text(encoding="utf-8"))
    all_records = []

    for cp in cp_list:
        if not cp.is_file():
            raise FileNotFoundError(f"Checkpoint missing: {cp}")
        state = strict_json(cp.read_text(encoding="utf-8"))["state"]
        all_records.extend(state["records"])

    compiled = pd.compile_rules(all_records, all_rows)
    return compiled


def project_interactive_dialogue(text, compiled_rules=None, item_id="interactive-query-001"):
    """Projects dynamic text query through persistent memory, regulation, funnel, and kaleidoscopic lenses."""
    if compiled_rules is None:
        compiled_rules = load_rules_from_checkpoints()

    tokens = tokenize_input(text)
    target_indices = locate_target_indices(tokens)

    item = {
        "id": item_id,
        "tokens": tokens,
        "target_indices": target_indices,
    }

    prediction = pd.predict_item(compiled_rules, item)
    raw_priming = mp.compute_priming_dials(prediction)
    regulation = mr.compute_homeostatic_regulation(raw_priming, prediction)
    funnel = tf.compute_tripartite_funnel(regulation["all_24_canonical_leaf_dials"], prediction)
    kaleidoscope = kg.compute_kaleidoscopic_response(funnel, regulation, prediction)

    return {
        "kind": KIND,
        "input_text": text,
        "tokens": tokens,
        "target_indices": target_indices,
        "prediction": prediction,
        "meditative_regulation": regulation,
        "tripartite_funnel": funnel,
        "kaleidoscopic_response": kaleidoscope,
    }


def verify_interactive_parity(text, checkpoints=None, dev_path=None):
    """Verifies that primary runtime store and matched ordinary structured-memory checkpoint yield identical projections."""
    cp_list = [Path(p) for p in (checkpoints or DEFAULT_CHECKPOINTS)]
    dev_file = Path(dev_path or DEFAULT_DEV_PATH)

    all_rows = strict_json(dev_file.read_text(encoding="utf-8"))
    primary_records = []
    memory_records = []

    for cp in cp_list:
        store = Store(cp.parent)
        primary_state = store.read()
        memory_state = strict_json(cp.read_text(encoding="utf-8"))["state"]

        if digest(primary_state) != digest(memory_state):
            raise ValueError(f"State parity mismatch at {cp}")

        primary_records.extend(primary_state["records"])
        memory_records.extend(memory_state["records"])

    primary_rules = pd.compile_rules(primary_records, all_rows)
    memory_rules = pd.compile_rules(memory_records, all_rows)

    proj_primary = project_interactive_dialogue(text, primary_rules)
    proj_memory = project_interactive_dialogue(text, memory_rules)

    if digest(proj_primary) != digest(proj_memory):
        raise ValueError("Interactive projection parity mismatch between primary and memory comparator")

    return {
        "consumer_parity": True,
        "projection_digest": digest(proj_primary),
        "primary_sample": proj_primary,
    }


def main():
    parser = argparse.ArgumentParser(description="LMFT Interactive Dialogue Prism")
    parser.add_argument("--sentence", type=str, help="Sentence to project through the kaleidoscopic prism")
    parser.add_argument("--verify-parity", action="store_true", help="Verify matched ordinary-memory baseline parity")
    args = parser.parse_args()

    if args.verify_parity:
        sentence = args.sentence or "The court issued a formal order of the court."
        print(f"Verifying ordinary memory baseline parity on: '{sentence}'...")
        res = verify_interactive_parity(sentence)
        print(f"Parity verified: {res['consumer_parity']}")
        print(f"Projection digest: {res['projection_digest']}")
        return

    if args.sentence:
        res = project_interactive_dialogue(args.sentence)
        k = res["kaleidoscopic_response"]
        pv = k["prism_vector"]
        act = k["social_exchange_actuation"]
        print("\n=== LMFT Interactive Dialogue Prism Response ===")
        print(f"Input: {res['input_text']}")
        print(f"Decision: {res['prediction']['decision']} (Sense: {res['prediction']['selected_sense']})")
        print(f"Lenses: Contemplation {pv['theta_contemplation']} deg | Truth {pv['theta_truth']} deg | Will {pv['theta_will']} deg")
        print(f"Concordance: {k['harmonic_concordance']}")
        print(f"Register: {act['speaking_register']}")
        print(f"Strategy: {act['actionable_social_strategy']}")
        print(f"Exemplar: \"{act['dialogue_exemplar']}\"")
        print("=================================================\n")
    else:
        print("LMFT Interactive Dialogue Prism Engine ready. Use --sentence or --verify-parity.")


if __name__ == "__main__":
    main()
