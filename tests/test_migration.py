"""Historical fixture and rejection tests for explicit seed migration."""

from copy import deepcopy
from dataclasses import asdict
import json
from pathlib import Path
import re

import pytest

from lmft_lab.birth import create_birth_state, SEED_VERSION
from lmft_lab.migration import LEGACY_ID_MAP, migrate_legacy_birth_record


def legacy_record():
    record = asdict(create_birth_state("individual", birth_event_id="birth", random_seed=42))
    record["seed_version"] = "minimal-v0.1-seed-1"
    # Independently reconstruct historical identity from the preserved diagram.
    spec = Path(__file__).resolve().parents[1] / "docs" / "MINIMAL_LMFT_SPEC.md"
    diagram = spec.read_text(encoding="utf-8").split("GFT V0.1 SEED GEOMETRY", 1)[1].split("```", 1)[0]
    paths = {}
    inventory = []
    for line in diagram.splitlines():
        match = re.search(r"[├└]── (.+)", line)
        if match:
            depth = match.start() // 4
            label = match.group(1)
            parent = paths.get(depth - 1)
            node_id = (parent + "/" if parent else "") + label.lower()
            paths[depth] = node_id
            inventory.append((node_id, parent, label))
    assert len(inventory) == 40
    for node, (node_id, parent, label) in zip(record["nodes"], inventory):
        node.update(id=node_id, parent_id=parent, label=label)
    return record


def test_migration_preserves_input_provenance_and_neutral_values():
    source = legacy_record()
    before = deepcopy(source)
    result = migrate_legacy_birth_record(source)
    assert source == before
    assert result.state == create_birth_state("individual", birth_event_id="birth", random_seed=42)
    assert result.target_seed_version == SEED_VERSION == "lmft-v0.1-seed-1"
    assert len(result.renamed_ids) == len(LEGACY_ID_MAP) == 3
    assert migrate_legacy_birth_record(json.loads(json.dumps(source))) == result


@pytest.mark.parametrize("corruption", ["version", "mixed", "missing", "extra", "baseline", "bool", "label", "parent"])
def test_rejects_unsupported_or_mixed_records(corruption):
    record = legacy_record()
    if corruption == "version": record["seed_version"] = SEED_VERSION
    if corruption == "mixed": record["nodes"][-1]["id"] = "psychological/contemplation/confidence"
    if corruption == "missing": record["nodes"] = record["nodes"][:-1]
    if corruption == "extra": record["unresolved"] = []
    if corruption == "baseline": record["nodes"][0]["values"]["baseline"] = 0.1
    if corruption == "bool": record["version"] = False
    if corruption == "label": record["nodes"][-3]["label"] = "Contemplation"
    if corruption == "parent": record["nodes"][-1]["parent_id"] = "psychological/contemplation"
    before = deepcopy(record)
    with pytest.raises(ValueError): migrate_legacy_birth_record(record)
    assert record == before


def test_migrated_state_accepts_canonical_inputs_and_rejects_old_ids():
    from lmft_lab.activation import activate_direct
    from lmft_lab.propagation import Association, propagate_activation

    state = migrate_legacy_birth_record(legacy_record()).state
    parent = "psychological/contemplation"
    child = parent + "/clarity"
    edge = Association("test-edge", parent, child, 1.0, 0.1, 0.5, "fixture", "fixture")
    result = propagate_activation(state, {parent: 0.8}, (edge,), event_id="input",
                                  source_instance="fixture", relationship_source="fixture")
    assert result.activations[child] == pytest.approx(0.2)
    assert result.direct_frame.seed_version == SEED_VERSION
    for old_id in LEGACY_ID_MAP:
        with pytest.raises(ValueError):
            activate_direct(state, {old_id: 0.8}, event_id="input", source_instance="fixture")
