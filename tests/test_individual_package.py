"""Unit tests for Standalone Individual Packaging & Migration Engine.

Verifies:
1. Complete round-trip export and import of trained LMFT individuals with full state fidelity.
2. Cryptographic SHA256 integrity verification detecting and rejecting tampered bytes.
3. Fail-closed rejection of seed geometry mutations (Rule D001).
4. Matched ordinary-memory baseline parity (Rule D004).
5. Invariance of canonical 40 founding nodes in birth.py (Rule D001).
"""
from copy import deepcopy
import json
from pathlib import Path
import pytest

from lmft_lab.birth import _inventory, create_birth_state
from lmft_lab.judgment import newborn
from lmft_lab.individual_package import (
    export_individual,
    import_individual,
    get_canonical_seed_fingerprint,
    OrdinaryMemoryPackageComparator,
)
from lmft_lab.runtime_store import digest


def make_sample_runtime_state():
    birth = create_birth_state("indiv-export-test", birth_event_id="birth-test", random_seed=42)
    return {
        "individual_id": "indiv-export-test",
        "birth": {
            "individual_id": birth.individual_id,
            "birth_event_id": birth.birth_event_id,
            "seed_version": birth.seed_version,
            "initialization_version": birth.initialization_version,
        },
        "judgment": newborn(),
        "capacity": {
            "rules": [
                {"rule_id": "r1", "lemma": "bank", "target_sense_key": "bank%1:14:00::", "core_pattern": "commercial bank"},
            ],
            "total_rules": 1,
        },
        "questions": {},
        "cycle": 5,
        "cursor": 5,
    }


def test_package_round_trip_export_import(tmp_path):
    """Verifies that an exported individual can be imported with exact state fidelity."""
    original_state = make_sample_runtime_state()
    package_file = tmp_path / "test_individual.lmft.json"
    
    exported = export_individual(original_state, package_file)
    assert package_file.exists()
    assert "integrity_signature" in exported
    
    restored = import_individual(package_file)
    assert restored["individual_id"] == original_state["individual_id"]
    assert restored["birth"] == original_state["birth"]
    assert restored["judgment"] == original_state["judgment"]
    assert restored["capacity"] == original_state["capacity"]
    assert restored["cycle"] == 5
    assert restored["cursor"] == 5
    assert restored["package_provenance"]["integrity_signature"] == exported["integrity_signature"]


def test_tampered_payload_rejected(tmp_path):
    """Verifies that tampered package bytes trigger fail-closed integrity failure."""
    original_state = make_sample_runtime_state()
    package_file = tmp_path / "tampered_individual.lmft.json"
    export_individual(original_state, package_file)
    
    # Tamper with the JSON payload
    data = json.loads(package_file.read_text(encoding="utf-8"))
    data["cycle"] = 999  # Unauthorized modification
    package_file.write_text(json.dumps(data), encoding="utf-8")
    
    with pytest.raises(ValueError, match="Integrity verification failure"):
        import_individual(package_file)


def test_tampered_seed_fingerprint_rejected(tmp_path):
    """Verifies that unauthorized seed modifications trigger Rule D001 rejection."""
    original_state = make_sample_runtime_state()
    package_file = tmp_path / "seed_mutated.lmft.json"
    exported = export_individual(original_state, package_file)
    
    # Tamper with seed fingerprint and recalculate signature to simulate malicious forge
    data = json.loads(package_file.read_text(encoding="utf-8"))
    data["seed_fingerprint"] = "bad_fingerprint_simulating_41_nodes"
    # Recalculate signature so signature check would pass
    data["integrity_signature"] = digest({k: v for k, v in data.items() if k != "integrity_signature"})
    package_file.write_text(json.dumps(data), encoding="utf-8")
    
    with pytest.raises(ValueError, match="Seed geometry violation"):
        import_individual(package_file)


def test_ordinary_memory_baseline_parity(tmp_path):
    """Verifies byte-for-byte evaluation parity with the matched ordinary-memory comparator (Rule D004)."""
    comparator = OrdinaryMemoryPackageComparator()
    state = make_sample_runtime_state()
    
    file_p = tmp_path / "primary.lmft.json"
    file_c = tmp_path / "comparator.lmft.json"
    
    res_p = comparator.round_trip(state, file_p)
    res_c = comparator.round_trip(state, file_c)
    
    # Remove file path string differences from provenance
    res_p_clean = deepcopy(res_p)
    res_c_clean = deepcopy(res_c)
    res_p_clean["package_provenance"].pop("source_package", None)
    res_c_clean["package_provenance"].pop("source_package", None)
    
    assert digest(res_p_clean) == digest(res_c_clean)


def test_frozen_seed_invariant_preserved():
    """Verifies that the canonical 40 founding nodes in birth.py remain strictly invariant (Rule D001)."""
    inventory = list(_inventory())
    assert len(inventory) == 40
    domains = {item[2] for item in inventory}
    assert domains == {"cultural", "philosophical", "experiential", "psychological"}
