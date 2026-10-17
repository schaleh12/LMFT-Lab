"""Unit tests for Quad-Seed 4x(6x8) Quaternion-Octonion Cross-Seed Harmonizer."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from lmft_lab.birth import _inventory
from lmft_lab.quad_seed_harmonizer import (
    CANONICAL_LEAF_IDS,
    CULTURAL_LEAVES_6,
    EXPERIENTIAL_LEAVES_6,
    PHILOSOPHICAL_LEAVES_6,
    PSYCHOLOGICAL_LEAVES_6,
    OrdinaryMemoryQuadSeedComparator,
    QuadSeedQuaternionOctonionHarmonizer,
    build_quad_seed_slm_prompt_block,
    normalize_octonion,
    octonion_multiply,
    octonion_norm,
)
from lmft_lab.runtime_store import digest


def test_quad_seed_canonical_24_leaf_partition():
    """All 4 6x8 seeds partition the 24 canonical leaves with zero overlap or omission (Rule D001)."""
    seed_leaves = (
        set(PHILOSOPHICAL_LEAVES_6)
        | set(CULTURAL_LEAVES_6)
        | set(EXPERIENTIAL_LEAVES_6)
        | set(PSYCHOLOGICAL_LEAVES_6)
    )
    assert len(PHILOSOPHICAL_LEAVES_6) == 6
    assert len(CULTURAL_LEAVES_6) == 6
    assert len(EXPERIENTIAL_LEAVES_6) == 6
    assert len(PSYCHOLOGICAL_LEAVES_6) == 6
    assert len(seed_leaves) == 24
    assert seed_leaves == CANONICAL_LEAF_IDS


def test_octonion_fano_multiplication_norm_and_non_commutativity():
    """Fano-plane octonion multiplication is norm-preserving and non-commutative on imaginary axes."""
    a = normalize_octonion([0.4, 0.3, -0.2, 0.5, 0.1, -0.3, 0.2, 0.4])
    b = normalize_octonion([0.2, -0.4, 0.5, 0.1, -0.2, 0.4, -0.3, 0.3])
    ab = octonion_multiply(a, b)
    ba = octonion_multiply(b, a)
    assert abs(octonion_norm(ab) - 1.0) < 1e-4
    # Non-commutative imaginary parts
    assert any(abs(ab[i] - ba[i]) > 1e-3 for i in range(1, 8))


def test_quad_seed_harmonizer_and_d004_parity():
    """QuadSeedQuaternionOctonionHarmonizer retires Kaleidoscope, preserves 30% buffer, and matches D004 comparator."""
    engine = QuadSeedQuaternionOctonionHarmonizer()
    comp = OrdinaryMemoryQuadSeedComparator()

    dials = {k: 0.78 for k in CANONICAL_LEAF_IDS}
    dials["experiential/synchronization/entrainment"] = 0.84
    dials["psychological/contemplation/clarity"] = 0.83

    res = engine.harmonize(dials)
    comp_res = comp.harmonize(dials)

    assert res["kaleidoscope_abandoned"] is True
    assert res["canonical_leaves_sampled"] == 24
    assert res["total_active_instinct_floats"] == 192
    assert res["resonant_master_chord_buffer"] == 0.30
    assert res["quad_seed_harmonic_coherence"] >= 0.85
    assert res["contrapuntal_voice_separation_index"] > 0.04
    assert abs(res["quaternion_norm_conservation"] - 1.0) < 1e-3
    assert digest(res) == digest(comp_res)

    prompt_block = build_quad_seed_slm_prompt_block(res, music_appreciation_mode=True)
    assert "Quad-Seed 4x(6x8) Quaternion-Octonion Harmonizer" in prompt_block
    assert "Kaleidoscope Retired" in prompt_block
    assert "[QUAD-SEED MUSICAL COMPLEXITY & APPRECIATION DIRECTIVE]" in prompt_block
