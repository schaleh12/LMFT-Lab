"""Tests for Kaleidoscopic Linguistic Prismatic Generator Prototype."""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "experiments"))

from lmft_lab.birth import _inventory
import kaleidoscopic_generator as kg
import tripartite_funnel as tf
import meditative_regulation as mr


def test_calculate_lens_angles_abstention():
    """Abstention produces zeroed angles and quiescent stasis lenses."""
    funnel_rec = {'epistemic_abstention': True}
    res = kg.calculate_lens_angles(funnel_rec, {})
    assert res['theta_contemplation'] == 0.0
    assert res['theta_truth'] == 0.0
    assert res['theta_will'] == 0.0
    assert res['contemplation_lens'] == 'Quiescent Stasis'
    assert res['harmonic_concordance'] == 1.0


def test_calculate_lens_angles_active():
    """Active instance calculates distinct angles and valid harmonic concordance."""
    funnel_rec = {
        'epistemic_abstention': False,
        'unified_psychological_cluster': {
            'psychological/contemplation/clarity': 0.85,
            'psychological/contemplation/confidence': 0.95,
            'psychological/truth/theory': 0.90,
            'psychological/truth/fact': 1.00,
            'psychological/will/intention': 0.85,
            'psychological/will/execution': 0.78,
        },
    }
    regulation_dials = {
        'experiential/phase/valence': 0.80,
        'experiential/phase/arousal': 0.82,
        'philosophical/structure/order': 0.75,
        'cultural/justice/honor': 0.89,
    }
    angles = kg.calculate_lens_angles(funnel_rec, regulation_dials)
    assert 0.0 <= angles['theta_contemplation'] < 360.0
    assert 0.0 <= angles['theta_truth'] < 360.0
    assert 0.0 <= angles['theta_will'] < 360.0
    assert 0.0 <= angles['harmonic_concordance'] <= 1.0
    assert 'Lens' in angles['contemplation_lens'] or '(' in angles['contemplation_lens']


def test_synthesize_actionable_social_strategy_authoritative():
    """Authoritative stance synthesizes Chivalrous register and grounded directive strategy."""
    lens_data = {
        'contemplation_lens': 'Lucid Dawn (Crisp analytical detachment)',
        'truth_lens': 'Empirical Revelation (Direct grounded testimony)',
        'will_lens': 'Sovereign Decree (Authoritative protective stewardship)',
    }
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:10:03::',
        'explanation': 'military instruction',
    }
    strat = kg.synthesize_actionable_social_strategy(lens_data, pred, 'authoritative_directive_execution')
    assert strat['speaking_register'] == 'Authoritative & Chivalrous'
    assert 'military instruction' in strat['actionable_social_strategy']
    assert 'military instruction' in strat['dialogue_exemplar']


def test_synthesize_actionable_social_strategy_communal():
    """Communal stance synthesizes Reassuring register and foundational peace strategy."""
    lens_data = {
        'contemplation_lens': 'Sunlit Zenith (Warm expansive communion)',
        'truth_lens': 'Holistic Synthesis (Seamless multi-coordinate unity)',
        'will_lens': 'Harmonic Consensus (Diplomatic communal reconciliation)',
    }
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:26:00::',
        'explanation': 'societal peace and stability',
    }
    strat = kg.synthesize_actionable_social_strategy(lens_data, pred, 'stable_ontological_equilibrium')
    assert strat['speaking_register'] == 'Communal & Reassuring'
    assert 'societal peace and stability' in strat['actionable_social_strategy']
    assert 'shared foundation' in strat['dialogue_exemplar']


def test_compute_kaleidoscopic_response():
    """Full kaleidoscopic response integrates lenses, vectors, and dialogue."""
    funnel_rec = {
        'epistemic_abstention': False,
        'unified_psychological_cluster': {
            'psychological/contemplation/clarity': 0.85,
            'psychological/contemplation/confidence': 0.95,
            'psychological/truth/theory': 0.90,
            'psychological/truth/fact': 1.00,
            'psychological/will/intention': 0.85,
            'psychological/will/execution': 0.78,
        },
    }
    regulation_rec = {
        'all_24_canonical_leaf_dials': {
            'experiential/phase/valence': 0.80,
            'experiential/phase/arousal': 0.82,
            'philosophical/structure/order': 0.75,
            'cultural/justice/honor': 0.89,
        },
        'regulated_stance': 'authoritative_directive_execution',
    }
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:10:03::',
        'explanation': 'orders given to subordinates',
    }
    resp = kg.compute_kaleidoscopic_response(funnel_rec, regulation_rec, pred)
    assert resp['epistemic_abstention'] is False
    assert 'theta_contemplation' in resp['prism_vector']
    assert 'Kaleidoscope Prismatic Chord' in resp['prismatic_gloss']
    assert resp['social_exchange_actuation']['speaking_register'] == 'Authoritative & Chivalrous'
