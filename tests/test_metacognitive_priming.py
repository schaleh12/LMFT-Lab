"""Tests for metacognitive priming console prototype."""
import json
from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
from lmft_lab.birth import _inventory
import metacognitive_priming as mp


def test_canonical_philosophical_nodes_preserved():
    # Verify that all philosophical target nodes are exact canonical nodes in birth.py
    inventory_map = {node_id: label for node_id, label, domain, _, depth in _inventory() if domain == 'philosophical' and depth == 2}
    for key, path in mp.PHILOSOPHICAL_LEAF_NODES.items():
        assert path in inventory_map
        assert inventory_map[path].lower() == key


def test_compute_priming_dials_directive():
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:10:03::',
        'explanation': 'instructions from the military force',
    }
    priming = mp.compute_priming_dials(pred)
    assert priming['epistemic_abstention'] is False
    assert priming['dominant_stance'] == 'authoritative_directive_execution'
    assert priming['dials'][mp.PHILOSOPHICAL_LEAF_NODES['agency']] == 0.85
    assert priming['dials'][mp.PHILOSOPHICAL_LEAF_NODES['order']] == 0.75
    assert priming['dyadic_biases']['being_agency_vs_existence'] > 0.3


def test_compute_priming_dials_magnitude():
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:07:01::',
        'explanation': 'a level or magnitude',
    }
    priming = mp.compute_priming_dials(pred)
    assert priming['dominant_stance'] == 'quantitative_continuum_awareness'
    assert priming['dials'][mp.PHILOSOPHICAL_LEAF_NODES['continuity']] == 0.85
    assert priming['dials'][mp.PHILOSOPHICAL_LEAF_NODES['discreteness']] == 0.15


def test_compute_priming_dials_abstention():
    pred = {
        'decision': 'abstain',
        'selected_sense': None,
        'explanation': 'No matching persistent contextual anchor.',
    }
    priming = mp.compute_priming_dials(pred)
    assert priming['epistemic_abstention'] is True
    assert priming['dominant_stance'] == 'neutral_open'
    assert all(v == 0.0 for v in priming['dials'].values())
    assert all(v == 0.0 for v in priming['dyadic_biases'].values())


def test_run_priming_study_integration(tmp_path):
    checkpoint = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v5-20261013-001\neutral-state\checkpoint.json')
    dev_export = Path(r'C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json')

    if not checkpoint.exists() or not dev_export.exists():
        pytest.skip('External archive files not found on local path')

    summary = mp.run_priming_study(checkpoint, dev_export, output_dir=tmp_path)

    assert summary['kind'] == 'metacognitive-priming-1'
    assert summary['total_instances_primed'] == 33
    assert summary['consumer_parity'] is True
    assert summary['stance_distribution']['authoritative_directive_execution'] == 5
    assert summary['stance_distribution']['stable_ontological_equilibrium'] == 7
    assert summary['stance_distribution']['quantitative_continuum_awareness'] == 3
    assert summary['stance_distribution']['discrete_sequential_operation'] == 2
    assert summary['stance_distribution']['neutral_open'] == 13

    assert (tmp_path / 'metacognitive_priming_summary.json').exists()
    assert (tmp_path / 'full_priming_records.json').exists()


def test_hexadic_palette_and_chromatic_aura():
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:10:03::',
        'explanation': 'instructions from the military force',
    }
    priming = mp.compute_priming_dials(pred)
    assert 'chromatic_aura' in priming
    assert priming['chromatic_aura']['hex'].startswith('#')
    assert len(priming['chromatic_aura']['rgb']) == 3

    materia = priming['materia_profile']
    assert materia['agency']['color'] == 'red'
    assert materia['agency']['materia'] == 'summoning'
    assert materia['agency']['archetype'] == 'queen'
    assert materia['agency']['dimension'] == 'extra-dimensional'

    assert materia['existence']['color'] == 'cyan'
    assert materia['existence']['materia'] == 'sun_magic'
    assert materia['existence']['archetype'] == 'king'

    assert materia['order']['color'] == 'magenta'
    assert materia['order']['materia'] == 'medium'
    assert materia['order']['archetype'] == 'bishop'

    assert materia['chaos']['color'] == 'green'
    assert materia['chaos']['materia'] == 'instrument'
    assert materia['chaos']['archetype'] == 'knight'

    assert materia['continuity']['color'] == 'blue'
    assert materia['continuity']['materia'] == 'soil_magic'
    assert materia['continuity']['archetype'] == 'pawn'

    assert materia['discreteness']['color'] == 'yellow'
    assert materia['discreteness']['materia'] == 'command'
    assert materia['discreteness']['archetype'] == 'rook'


def test_dimensional_resonance_and_epistemic_mirror():
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:07:01::',
        'explanation': 'a level or magnitude',
    }
    priming = mp.compute_priming_dials(pred)
    res = priming['dimensional_resonance']
    assert 'continuity_pawn_fire' in res['hyper_dimensional_persistence']

    mirror = priming['epistemic_mirror']
    assert mirror['theory'] == 'a level or magnitude'
    assert 'Observed' in mirror['fact']
    assert mirror['clarity'] > 0.0
    assert mirror['confidence'] == 1.0


def test_full_corpus_multi_checkpoint_priming(tmp_path):
    cp1 = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v5-20261013-001\neutral-state\checkpoint.json')
    cp2 = Path(r'C:\Users\schal\AppData\Local\LMFT-Lab\research-archives\slm-representation-interface-v6-20261013-001\neutral-state\checkpoint.json')
    dev_export = Path(r'C:\Users\schal\AppData\Local\Temp\lmft-semcor-order-development-v1-dzil94yr\development.json')

    if not (cp1.exists() and cp2.exists() and dev_export.exists()):
        pytest.skip('External archive files not found on local path')

    summary = mp.run_priming_study([cp1, cp2], dev_export, output_dir=tmp_path)

    assert summary['total_instances_primed'] == 33
    assert summary['consumer_parity'] is True
    # In full corpus, zero abstentions
    assert 'neutral_open' not in summary['stance_distribution']
    assert summary['stance_distribution']['authoritative_directive_execution'] == 10
    assert summary['stance_distribution']['stable_ontological_equilibrium'] == 9
    assert summary['stance_distribution']['discrete_sequential_operation'] == 6
    assert summary['stance_distribution']['quantitative_continuum_awareness'] == 4
    assert summary['stance_distribution']['balanced_contextual_stance'] == 4


def test_shadow_pathology_and_kingdom_profiles():
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:10:03::',
        'explanation': 'instructions from the military force',
    }
    priming = mp.compute_priming_dials(pred)

    shadow = priming['shadow_profile']
    assert shadow['agency']['pathology'] == 'psychosis'
    assert shadow['existence']['pathology'] == 'paranoia'
    assert shadow['order']['pathology'] == 'prejudice'
    assert shadow['chaos']['pathology'] == 'corruption'
    assert shadow['continuity']['pathology'] == 'mania_greed'
    assert shadow['discreteness']['pathology'] == 'narcissism'

    kingdom = priming['kingdom_profile']
    assert kingdom['agency']['kingdom'] == 'mammal'
    assert kingdom['agency']['environment'] == 'light'
    assert kingdom['existence']['kingdom'] == 'reptile'
    assert kingdom['existence']['environment'] == 'sun'
    assert kingdom['order']['kingdom'] == 'fish'
    assert kingdom['order']['environment'] == 'ocean'
    assert kingdom['chaos']['kingdom'] == 'bird'
    assert kingdom['chaos']['environment'] == 'sky'
    assert kingdom['continuity']['kingdom'] == 'insect'
    assert kingdom['continuity']['environment'] == 'soil'
    assert kingdom['discreteness']['kingdom'] == 'amphibian'
    assert kingdom['discreteness']['environment'] == 'shadow'


def test_poetic_action_bid():
    pred = {
        'decision': 'single',
        'selected_sense': 'order%1:10:03::',
        'explanation': 'instructions from the military force',
    }
    priming = mp.compute_priming_dials(pred)
    bid = priming['poetic_action_bid']
    assert 'Queen' in bid
    assert 'Mammal' in bid
    assert 'psychosis' in bid
    assert 'instructions from the military force' in bid
    assert priming['chromatic_aura']['hex'] in bid



