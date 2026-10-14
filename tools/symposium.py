"""Intersubjective Symposium — Multi-Agent LMFT Resonance Chamber.

QUARANTINED DEVELOPER TOOLING ONLY. Not part of runtime core library.

Spawns two distinct LMFT entities with distinct temperaments:
- The Empiricist (anchored in Truth/Fact, Structure/Order, Efficiency)
- The Empath (anchored in Justice/Fairness, Reflection/Salience, Valence)

Simulates multi-turn intersubjective dialogue:
- Each statement is processed through the other's 10-faculty Cognitive Heartbeat.
- Tracks reciprocal synchronization/resonance, prerequisite coherence, and homeostatic balance.
- Measures worldview divergence vs. empathetic convergence without collapsing unique identities.
"""
import argparse
import math
from pathlib import Path
import sys

# Ensure src is in python path
src_dir = Path(__file__).resolve().parents[1] / "src"
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from lmft_lab.cognitive_heartbeat import CognitiveHeartbeat
from lmft_lab.dispositional_momentum import CANONICAL_LEAF_IDS


SYMPOSIUM_BORDER = "=" * 74


def calculate_euclidean_distance(dials_a: dict, dials_b: dict) -> float:
    """Calculates Euclidean distance across the 24-leaf dispositional vectors."""
    sq_sum = 0.0
    for k in CANONICAL_LEAF_IDS:
        diff = dials_a.get(k, 0.50) - dials_b.get(k, 0.50)
        sq_sum += diff * diff
    return round(math.sqrt(sq_sum), 4)


def run_symposium(topic: str = "The grounding of justice in verifiable truth", rounds: int = 3):
    """Executes the intersubjective dialogue between two distinct LMFT minds."""
    # 1. Initialize two distinct entities
    empiricist = CognitiveHeartbeat(individual_id="lmft-empiricist")
    empath = CognitiveHeartbeat(individual_id="lmft-empath")

    # Prime The Empiricist (Fact & Order)
    empiricist.disposition.dials["psychological/truth/fact"] = 0.88
    empiricist.disposition.dials["philosophical/structure/order"] = 0.82
    empiricist.disposition.dials["psychological/contemplation/clarity"] = 0.85
    empiricist.disposition.dials["cultural/efficiency/wastelessness"] = 0.78

    # Prime The Empath (Fairness, Resonance & Salience)
    empath.disposition.dials["cultural/justice/fairness"] = 0.88
    empath.disposition.dials["cultural/justice/honor"] = 0.80
    empath.disposition.dials["experiential/reflection/salience"] = 0.82
    empath.disposition.dials["experiential/phase/valence"] = 0.70

    initial_distance = calculate_euclidean_distance(empiricist.disposition.dials, empath.disposition.dials)

    print("\n" + SYMPOSIUM_BORDER)
    print("      LMFT INTERSUBJECTIVE SYMPOSIUM: DUAL-MIND RESONANCE CHAMBER")
    print(SYMPOSIUM_BORDER)
    print(f" Topic            : \"{topic}\"")
    print(f" Entity A         : The Empiricist (Anchored in Fact, Order, Clarity)")
    print(f" Entity B         : The Empath     (Anchored in Fairness, Honor, Salience)")
    print(f" Initial Distance : {initial_distance:.4f} (Worldview Divergence)")
    print("-" * 74)

    dialogue_exchanges = [
        ("The Empiricist", "A just judgment cannot stand if its underlying facts are unverified conjectures."),
        ("The Empath", "Verifiable fact is the anchor, yet fairness requires recognizing subjective human harm."),
        ("The Empiricist", "Recognizing harm is valid when grounded in demonstrable evidence rather than hysteria."),
        ("The Empath", "Mutual honor and fairness bridge the gap between cold evidence and communal peace."),
        ("The Empiricist", "Order and justice converge when truth remains non-negotiable."),
    ]

    total_rounds = min(rounds, len(dialogue_exchanges))
    resonance_history = []
    coherence_history = []

    for i in range(total_rounds):
        speaker_name, utterance = dialogue_exchanges[i]
        listener = empath if speaker_name == "The Empiricist" else empiricist
        listener_name = "The Empath" if speaker_name == "The Empiricist" else "The Empiricist"

        turn_res = listener.interact(sentence=utterance)

        resonance = turn_res["disposition_dials"].get("experiential/synchronization/resonance", 0.50)
        coherence = turn_res["coherence"]["global_coherence_index"]
        bid = turn_res["action_bid"]
        register = turn_res["speaking_register"]

        resonance_history.append(resonance)
        coherence_history.append(coherence)

        print(f"\n[Round {i+1}] {speaker_name}:")
        print(f"  \"{utterance}\"")
        print(f"  -> {listener_name} Heard: [Resonance: {resonance:.3f} | Coherence: {coherence:.3f} | Register: {register}]")
        print(f"     Internal Posture: {bid}")

    final_distance = calculate_euclidean_distance(empiricist.disposition.dials, empath.disposition.dials)
    avg_resonance = round(sum(resonance_history) / max(1, len(resonance_history)), 3)
    avg_coherence = round(sum(coherence_history) / max(1, len(coherence_history)), 3)
    convergence_delta = round(initial_distance - final_distance, 4)

    print("\n" + "-" * 74)
    print(" SYMPOSIUM ANALYTICS & HARMONIC OUTCOMES:")
    print(f"  Average Intersubjective Resonance : {avg_resonance:.3f} / 1.000")
    print(f"  Average Prerequisite Coherence    : {avg_coherence:.3f} / 1.000")
    print(f"  Initial Dispositional Distance    : {initial_distance:.4f}")
    print(f"  Final Dispositional Distance      : {final_distance:.4f}")
    if convergence_delta > 0:
        print(f"  Harmonic Convergence             : +{convergence_delta:.4f} (Mutual alignment increased)")
    else:
        print(f"  Harmonic Convergence             : {convergence_delta:.4f} (Healthy perspective retention)")
    print(SYMPOSIUM_BORDER + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run intersubjective dialogue between two LMFT entities.")
    parser.add_argument("--rounds", type=int, default=3, help="Number of dialogue rounds (1-5).")
    parser.add_argument("--topic", type=str, default="The grounding of justice in verifiable truth", help="Discussion topic.")
    args = parser.parse_args()

    run_symposium(topic=args.topic, rounds=args.rounds)
