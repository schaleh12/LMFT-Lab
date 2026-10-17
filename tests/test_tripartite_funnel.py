"""Tests for Tripartite Psychological Funnel Engine."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from lmft_lab.birth import _inventory
import tripartite_funnel as tf
import meditative_regulation as mr


def test_canonical_leaves_match_inventory():
    """All 24 canonical leaves in the funnel map must match birth.py exactly."""
    inventory_leaf_ids = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}
    expected = set(mr.CANONICAL_LEAF_MAP.keys())
    assert expected == inventory_leaf_ids
    assert len(expected) == 24


def test_transform_cultural_to_will():
    """Cultural leaves transform into Will (Intention and Execution)."""
    cultural_dials = {
        'cultural/efficiency/power': 0.85,
        'cultural/efficiency/wastelessness': 0.90,
        'cultural/justice/honor': 0.80,
        'cultural/justice/fairness': 0.75,
        'cultural/freedom/self-sufficiency': 0.90,
        'cultural/freedom/needlessness': 0.85,
    }
    will = tf.transform_cultural_to_will(cultural_dials)
    assert 'psychological/will/intention' in will
    assert 'psychological/will/execution' in will
    assert 0.0 <= will['psychological/will/intention'] <= 1.0
    assert 0.0 <= will['psychological/will/execution'] <= 1.0
    assert will['will_posture_descriptor'] == 'Noble Resolute Action'


def test_transform_philosophical_to_truth():
    """Philosophical leaves transform into Truth (Theory and Fact)."""
    phil_dials = {
        'philosophical/being/agency': 0.85,
        'philosophical/being/existence': 0.40,
        'philosophical/structure/order': 0.75,
        'philosophical/structure/chaos': 0.10,
        'philosophical/persistence/continuity': 0.50,
        'philosophical/persistence/discreteness': 0.50,
    }
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:10:03::',
        'explanation': 'military instruction',
    }
    truth = tf.transform_philosophical_to_truth(phil_dials, pred)
    assert truth['psychological/truth/fact'] == 1.00
    assert truth['psychological/truth/theory'] > 0.60
    assert truth['truth_epistemic_grade'] == 'Empirically Grounded Truth'
    assert truth['theory_text'] == 'military instruction'


def test_transform_experiential_to_contemplation():
    """Experiential leaves transform into Contemplation (Clarity and Confidence)."""
    exp_dials = {
        'experiential/reflection/novelty': 0.15,
        'experiential/reflection/salience': 0.85,
        'experiential/phase/valence': 0.80,
        'experiential/phase/arousal': 0.75,
        'experiential/synchronization/resonance': 0.95,
        'experiential/synchronization/entrainment': 0.95,
    }
    contemplation = tf.transform_experiential_to_contemplation(exp_dials)
    assert contemplation['psychological/contemplation/clarity'] > 0.70
    assert contemplation['psychological/contemplation/confidence'] > 0.80
    assert contemplation['contemplation_state_descriptor'] == 'Luminous Clarity'


def test_compute_tripartite_funnel_abstention():
    """Abstention produces quiescent stasis with zeroed will and fact."""
    pred = {'decision': 'abstain', 'selected_sense': None}
    funnel = tf.compute_tripartite_funnel({}, pred)
    assert funnel['epistemic_abstention'] is True
    assert funnel['funnel_status'] == 'quiescent_stasis'
    assert funnel['unified_psychological_cluster']['psychological/will/intention'] == 0.0
    assert funnel['unified_psychological_cluster']['psychological/truth/fact'] == 0.0


def test_compute_tripartite_funnel_active():
    """Active instance produces coherent convergence across all 3 funnels."""
    full_24 = {
        'cultural/efficiency/power': 0.765,
        'cultural/efficiency/wastelessness': 0.712,
        'cultural/justice/honor': 0.893,
        'cultural/justice/fairness': 0.775,
        'cultural/freedom/self-sufficiency': 0.95,
        'cultural/freedom/needlessness': 0.85,
        'philosophical/being/agency': 0.85,
        'philosophical/being/existence': 0.55,
        'philosophical/structure/order': 0.75,
        'philosophical/structure/chaos': 0.10,
        'philosophical/persistence/continuity': 0.5,
        'philosophical/persistence/discreteness': 0.5,
        'experiential/reflection/novelty': 0.15,
        'experiential/reflection/salience': 0.85,
        'experiential/phase/valence': 0.8,
        'experiential/phase/arousal': 0.82,
        'experiential/synchronization/resonance': 0.95,
        'experiential/synchronization/entrainment': 0.95,
        'psychological/will/intention': 0.85,
        'psychological/will/execution': 0.787,
        'psychological/truth/theory': 0.9,
        'psychological/truth/fact': 1.0,
        'psychological/contemplation/clarity': 0.75,
        'psychological/contemplation/confidence': 1.0,
    }
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:10:03::',
        'explanation': 'military directives',
    }
    funnel = tf.compute_tripartite_funnel(full_24, pred)
    assert funnel['epistemic_abstention'] is False
    assert funnel['funnel_status'] == 'active_funnel_convergence'
    assert 'Luminous Clarity' in funnel['funnel_synthesis']
    assert 'Empirically Grounded Truth' in funnel['funnel_synthesis']
    assert len(funnel['unified_psychological_cluster']) == 6
