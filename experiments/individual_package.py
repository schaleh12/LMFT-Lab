"""Standalone Individual Packaging & Migration Benchmark.

Evaluates atomic export, cryptographic SHA256 integrity validation, Rule D001 seed invariant
verification, and round-trip restoration of trained LMFT individuals.

Preserves Rule D001 (frozen 40-node seed geometry) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted evaluation.
"""
import argparse
from copy import deepcopy
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory, create_birth_state
from lmft_lab.judgment import newborn
from lmft_lab.individual_package import (
    export_individual,
    import_individual,
    get_canonical_seed_fingerprint,
    OrdinaryMemoryPackageComparator,
)
from lmft_lab.runtime_store import digest, atomic_json

ROOT = Path(__file__).resolve().parents[1]
KIND = "individual-package-benchmark-1"


def make_full_test_individual():
    """Builds a rich trained individual state with birth, capacity, and ledgers."""
    birth = create_birth_state("migratable-individual-alpha", birth_event_id="birth-alpha-001", random_seed=42)
    return {
        "individual_id": "migratable-individual-alpha",
        "birth": {
            "individual_id": birth.individual_id,
            "birth_event_id": birth.birth_event_id,
            "seed_version": birth.seed_version,
            "initialization_version": birth.initialization_version,
        },
        "judgment": newborn(),
        "capacity": {
            "total_rules": 8,
            "rules": [
                {"rule_id": "r1", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "commercial bank", "weight": 0.6929},
                {"rule_id": "r2", "lemma": "bank", "target_sense_key": "bank%1:17:01::", "core_pattern": "river bank", "weight": 0.6387},
                {"rule_id": "r3", "lemma": "order", "target_sense_key": "order%1:10:00::", "core_pattern": "court order", "weight": 0.6929},
                {"rule_id": "r4", "lemma": "order", "target_sense_key": "order%1:14:00::", "core_pattern": "rank and order", "weight": 0.6387},
            ],
        },
        "questions": {
            "out-1": {"issue": "missing-evidence", "answered_by": "reply-1"},
        },
        "cycle": 12,
        "cursor": 12,
    }


def run_individual_package_study(output_dir=None):
    """Executes export, tampering rejection, and verified round-trip benchmarks."""
    comparator = OrdinaryMemoryPackageComparator()
    state = make_full_test_individual()
    
    out_dir = Path(output_dir) if output_dir else Path("outputs/temp_pkg")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    pkg_file = out_dir / "individual_alpha.lmft.json"
    
    # 1. Export Individual
    exported_manifest = export_individual(state, pkg_file, description="Benchmark Export Individual Alpha")
    file_size_bytes = pkg_file.stat().st_size
    signature = exported_manifest["integrity_signature"]
    
    # 2. Verify Import Fidelity
    restored_state = import_individual(pkg_file, verify_seed=True)
    assert restored_state["individual_id"] == state["individual_id"]
    assert restored_state["cycle"] == 12
    assert restored_state["capacity"]["total_rules"] == 8
    
    # 3. Tampering Test: Alter cycle count
    tampered_file = out_dir / "tampered_cycle.lmft.json"
    tampered_data = json.loads(pkg_file.read_text(encoding="utf-8"))
    tampered_data["cycle"] = 999
    tampered_file.write_text(json.dumps(tampered_data), encoding="utf-8")
    
    tamper_detected = False
    try:
        import_individual(tampered_file)
    except ValueError as e:
        if "Integrity verification failure" in str(e):
            tamper_detected = True
    assert tamper_detected, "Tampered cycle failed to trigger integrity rejection!"
    
    # 4. Seed Mutation Test: Alter seed fingerprint
    seed_mutated_file = out_dir / "seed_mutated.lmft.json"
    mutated_data = json.loads(pkg_file.read_text(encoding="utf-8"))
    mutated_data["seed_fingerprint"] = "forged_41_node_seed"
    mutated_data["integrity_signature"] = digest({k: v for k, v in mutated_data.items() if k != "integrity_signature"})
    seed_mutated_file.write_text(json.dumps(mutated_data), encoding="utf-8")
    
    seed_violation_detected = False
    try:
        import_individual(seed_mutated_file, verify_seed=True)
    except ValueError as e:
        if "Seed geometry violation" in str(e):
            seed_violation_detected = True
    assert seed_violation_detected, "Forged seed failed to trigger Rule D001 violation!"
    
    # 5. Baseline Comparator Parity (Rule D004)
    comp_pkg_file = out_dir / "comparator_alpha.lmft.json"
    comp_restored = comparator.round_trip(state, comp_pkg_file)
    
    p_clean = deepcopy(restored_state)
    c_clean = deepcopy(comp_restored)
    p_clean.pop("package_provenance", None)
    c_clean.pop("package_provenance", None)
    assert digest(p_clean) == digest(c_clean)
    
    # 6. Verify seed invariant in current process
    assert len(list(_inventory())) == 40
    
    summary = {
        "kind": KIND,
        "exported_package_file": str(pkg_file.resolve()),
        "file_size_bytes": file_size_bytes,
        "integrity_signature": signature,
        "round_trip_verified": True,
        "tamper_protection_verified": tamper_detected,
        "seed_invariant_enforced": seed_violation_detected,
        "consumer_parity": True,
        "evaluation_digest": digest(p_clean),
    }
    
    if output_dir:
        atomic_json(out_dir / "individual-package-summary.json", summary)
        
    return summary


def main():
    parser = argparse.ArgumentParser(description="Standalone Individual Packaging & Migration Benchmark")
    parser.add_argument("--output-dir", type=str, help="Directory to save benchmark summary")
    args = parser.parse_args()
    
    res = run_individual_package_study(output_dir=args.output_dir)
    print("\n=== Standalone Individual Packaging Results ===")
    print(f"Export Package: {res['exported_package_file']}")
    print(f"Package Size: {res['file_size_bytes']} bytes")
    print(f"SHA256 Signature: {res['integrity_signature'][:16]}...")
    print(f"Round-Trip Verified: {res['round_trip_verified']}")
    print(f"Tamper Rejection Verified: {res['tamper_protection_verified']}")
    print(f"Seed Invariant Enforced (Rule D001): {res['seed_invariant_enforced']}")
    print(f"Consumer Parity Verified (Rule D004): {res['consumer_parity']}")
    print("================================================\n")


if __name__ == "__main__":
    main()
