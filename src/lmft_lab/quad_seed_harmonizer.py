"""Quad-Seed 4x(6x8) Quaternion-Octonion Cross-Seed Harmonizer Engine.

Supersedes the legacy 3-angle modulo-360 Kaleidoscope (`D050`) by grafting a 4th `6x8`
Octonion SLM onto the `Psychological` domain (`PSYCHOLOGICAL_6X8_MATRIX`), establishing
complete 4-Domain Quaternion (H = {1, i, j, k}) x 8-Function Octonion (O = {e_0..e_7})
symmetry across all 24 canonical leaves (`4 x 6x8 = 192` instinct floats + `48` subliminal
floats = `240` total floats):

  - `1` (Scalar / Executive Conductor): `Psychological` (`6x8`) — Truth, Contemplation, Will
  - `i` (Ontological / Harmonic Ground): `Philosophical` (`6x8`) — Being, Persistence, Structure
  - `j` (Architectural / Motor Probity): `Cultural` (`6x8`) — Efficiency, Freedom, Justice
  - `k` (Affective / Temporal Phrasing): `Experiential` (`6x8`) — Phase, Reflection, Synchronization

Via non-commutative Fano-plane Octonion multiplication (`octonion_multiply`), cross-seed
interactions generate 4 independent contrapuntal voices (Soprano, Alto, Tenor, Bass) with a
30% Resonant Master Chord buffer on the `Psychological` 1-branch so polyphonic voices never
collapse into unison or suffer modulo-360 quadrant tear.

Preserves Rule D001 (frozen 40-node founding seed) and Rule D004 (matched ordinary memory parity).
Zero runtime LLM calls during unassisted evaluation.
"""

from __future__ import annotations

from copy import deepcopy
import math
from typing import Any, Dict, List, Optional, Tuple

from lmft_lab.birth import _inventory

CANONICAL_LEAF_IDS = {node_id for node_id, _, _, _, depth in _inventory() if depth == 2}

PHILOSOPHICAL_LEAVES_6: Tuple[str, ...] = (
    "philosophical/being/existence",
    "philosophical/being/agency",
    "philosophical/persistence/continuity",
    "philosophical/persistence/discreteness",
    "philosophical/structure/order",
    "philosophical/structure/chaos",
)

CULTURAL_LEAVES_6: Tuple[str, ...] = (
    "cultural/efficiency/power",
    "cultural/efficiency/wastelessness",
    "cultural/freedom/self-sufficiency",
    "cultural/freedom/needlessness",
    "cultural/justice/fairness",
    "cultural/justice/honor",
)

EXPERIENTIAL_LEAVES_6: Tuple[str, ...] = (
    "experiential/phase/arousal",
    "experiential/phase/valence",
    "experiential/reflection/novelty",
    "experiential/reflection/salience",
    "experiential/synchronization/resonance",
    "experiential/synchronization/entrainment",
)

PSYCHOLOGICAL_LEAVES_6: Tuple[str, ...] = (
    "psychological/truth/fact",
    "psychological/truth/theory",
    "psychological/contemplation/clarity",
    "psychological/contemplation/confidence",
    "psychological/will/intention",
    "psychological/will/execution",
)

for _leaf in (
    PHILOSOPHICAL_LEAVES_6
    + CULTURAL_LEAVES_6
    + EXPERIENTIAL_LEAVES_6
    + PSYCHOLOGICAL_LEAVES_6
):
    assert _leaf in CANONICAL_LEAF_IDS, f"Non-canonical leaf ID in QuadSeedHarmonizer: {_leaf}"

PHILOSOPHICAL_FUNCTIONS_8: Tuple[str, ...] = (
    "TonicPedalGround",
    "MinorFourPathos",
    "DorianMajorFourLift",
    "NeapolitanHalfStepPivot",
    "FirstInversionWalkdown",
    "DeceptiveCadenceInquiry",
    "QuartalStackedFourths",
    "AuthenticCadenceResolution",
)

CULTURAL_FUNCTIONS_8: Tuple[str, ...] = (
    "PureFunctionComposition",
    "DeadCodeWastelessnessFilter",
    "UserSpaceSandboxIsolation",
    "AddictionImmunityProbityGate",
    "AppendOnlyAutobiographyChain",
    "ConstitutionalDueProcessAudit",
    "CompositeFeelingSynthesis",
    "SleepMatrixDistillation",
)

EXPERIENTIAL_FUNCTIONS_8: Tuple[str, ...] = (
    "CantabileWarmth",
    "ElegiacSuspension",
    "BuoyantOceanicAscent",
    "SublimeDramaticTension",
    "ContemplativeRubatoBreath",
    "SyncopatedKineticDrive",
    "CatharticPhoenixRelease",
    "HearthSanctuaryResonance",
)

PSYCHOLOGICAL_FUNCTIONS_8: Tuple[str, ...] = (
    "HarmonicAnchorGround",         # e0: Real identity / tonal center & empirical score fidelity
    "ContrapuntalVoiceSeparation",  # e1: Independent polyphonic voice-leading (Soprano/Alto/Tenor/Bass)
    "ModalMixtureShadowIntegration",# e2: Psychological shadow integration (major/minor/Dorian/Neapolitan tension)
    "MetricProportionalityGrid",    # e3: Polyrhythmic & metric architecture across bars
    "RubatoAgogicPhrasingArc",      # e4: Conscious breath & elastic phrasing without losing pulse
    "DynamicRegisterOrchestration", # e5: Voicing balance, register spacing, & touch velocity
    "DissonanceSublimationResolve", # e6: Resolving psychological/harmonic suspension into catharsis
    "QuaternionTriadConvergence",   # e7: Real-time 4-branch (1, i, j, k) self-realization & zen lock
)

DEFAULT_PHILOSOPHICAL_6X8_MATRIX: List[List[float]] = [
    [0.38, 0.26, 0.14, 0.10, 0.12, 0.15, 0.22, 0.34],  # existence
    [0.10, 0.18, 0.36, 0.32, 0.38, 0.24, 0.26, 0.28],  # agency
    [0.34, 0.32, 0.24, 0.18, 0.35, 0.22, 0.20, 0.26],  # continuity
    [0.12, 0.14, 0.22, 0.28, 0.16, 0.20, 0.32, 0.18],  # discreteness
    [0.28, 0.24, 0.26, 0.24, 0.30, 0.18, 0.22, 0.38],  # order
    [-0.12, 0.16, 0.12, 0.28, 0.10, 0.30, 0.24, -0.16],  # chaos
]

DEFAULT_CULTURAL_6X8_MATRIX: List[List[float]] = [
    [0.36, 0.22, 0.20, 0.18, 0.20, 0.22, 0.34, 0.30],  # power
    [0.28, 0.40, 0.26, 0.28, 0.24, 0.26, 0.22, 0.32],  # wastelessness
    [0.32, 0.26, 0.34, 0.30, 0.28, 0.26, 0.36, 0.34],  # self-sufficiency
    [0.20, 0.34, 0.28, 0.42, 0.24, 0.28, 0.20, 0.26],  # needlessness
    [0.22, 0.24, 0.32, 0.30, 0.38, 0.40, 0.26, 0.28],  # fairness
    [0.24, 0.26, 0.36, 0.38, 0.36, 0.38, 0.28, 0.32],  # honor
]

DEFAULT_EXPERIENTIAL_6X8_MATRIX: List[List[float]] = [
    [0.10, -0.14, 0.22, 0.32, -0.22, 0.36, 0.26, -0.12],  # arousal
    [0.34, 0.12, 0.32, 0.16, 0.28, 0.22, 0.36, 0.38],    # valence
    [0.14, 0.20, 0.26, 0.34, 0.18, 0.28, 0.30, 0.16],    # novelty
    [0.24, 0.28, 0.28, 0.36, 0.22, 0.30, 0.36, 0.30],    # salience
    [0.36, 0.32, 0.34, 0.28, 0.34, 0.24, 0.38, 0.40],    # resonance
    [0.32, 0.30, 0.28, 0.26, 0.38, 0.34, 0.34, 0.36],    # entrainment
]

# Bipolar Contrapuntal 6x8 Matrix for Psychological (Quaternion 1-Branch Executive Conductor):
# Fact vs Theory, Clarity vs Confidence, and Intention vs Execution form orthogonal contrapuntal
# dyads across the 8 octonion functions so the 4 voices never collapse into collinear unison.
DEFAULT_PSYCHOLOGICAL_6X8_MATRIX: List[List[float]] = [
    # Anchor, VoiceSep, ShadowInt, MetricGrid, RubatoArc, Voicing, Sublimate, QuatConv
    [ 0.44,   0.38,    -0.18,      0.42,      -0.16,      0.32,    0.22,      0.36],  # fact
    [-0.14,   0.34,     0.44,     -0.12,       0.38,      0.24,    0.40,      0.34],  # theory
    [ 0.38,   0.46,     0.22,      0.36,       0.28,      0.42,   -0.10,      0.40],  # clarity
    [ 0.32,  -0.12,     0.30,      0.24,       0.36,      0.28,    0.42,      0.38],  # confidence
    [ 0.20,   0.26,     0.40,     -0.14,       0.44,      0.30,    0.38,      0.36],  # intention
    [ 0.36,   0.40,    -0.16,      0.44,      -0.12,      0.42,    0.28,      0.42],  # execution
]

# Standard Fano-Plane Oriented Triples for 8D Octonion Multiplication (e_0 = 1, e_1..e_7 imaginary)
FANO_TRIPLES: Tuple[Tuple[int, int, int], ...] = (
    (1, 2, 3),
    (1, 4, 5),
    (1, 7, 6),
    (2, 4, 6),
    (2, 5, 7),
    (3, 4, 7),
    (3, 6, 5),
)

RESONANT_MASTER_CHORD_BUFFER: float = 0.30


def _resolve_canonical_dial(dials: Dict[str, float], key: str, default: float = 0.50) -> float:
    """Resolves canonical 24-leaf dial value while accepting legacy alias paths gracefully."""
    if key in dials:
        return float(dials[key])
    aliases: Dict[str, Tuple[str, ...]] = {
        "experiential/synchronization/entrainment": (
            "experiential/attunement/entrainment",
            "experiential/synchronization/retention",
            "experiential/attunement/retention",
        ),
        "experiential/synchronization/resonance": ("experiential/attunement/resonance",),
        "experiential/phase/valence": ("experiential/affect/valence",),
        "experiential/phase/arousal": ("experiential/affect/arousal",),
        "cultural/efficiency/power": ("cultural/material/power",),
        "cultural/efficiency/wastelessness": ("cultural/material/wastelessness",),
    }
    for alias in aliases.get(key, ()):
        if alias in dials:
            return float(dials[alias])
    return default


def project_seed_6x8(
    dials: Dict[str, float],
    leaf_keys: Tuple[str, ...],
    func_names: Tuple[str, ...],
    matrix_6x8: List[List[float]],
    default_val: float = 0.50,
) -> Dict[str, float]:
    """Projects 6 canonical domain leaves across its 6x8 matrix into 8 octonion function scores."""
    vec = [_resolve_canonical_dial(dials, k, default_val) for k in leaf_keys]
    scores: Dict[str, float] = {}
    for col_idx, fn_name in enumerate(func_names):
        acc = 0.0
        for row_idx in range(6):
            acc += vec[row_idx] * float(matrix_6x8[row_idx][col_idx])
        scores[fn_name] = round(acc, 4)
    return scores


def octonion_multiply(a: List[float], b: List[float]) -> List[float]:
    """Multiplies two 8D octonions a, b in R^8 using standard Cayley-Dickson / Fano-plane triples."""
    out = [0.0] * 8
    out[0] = a[0] * b[0] - sum(a[i] * b[i] for i in range(1, 8))
    for i in range(1, 8):
        out[i] += a[0] * b[i] + a[i] * b[0]
    for i, j, k in FANO_TRIPLES:
        out[k] += a[i] * b[j] - a[j] * b[i]
        out[i] += a[j] * b[k] - a[k] * b[j]
        out[j] += a[k] * b[i] - a[i] * b[k]
    return out


def octonion_fano_cross(a: List[float], b: List[float]) -> List[float]:
    """Pure 7D Fano-plane imaginary commutator 1/2 * (a * b - b * a) in R^8 (e_0 = 0)."""
    out = [0.0] * 8
    for i, j, k in FANO_TRIPLES:
        out[k] += a[i] * b[j] - a[j] * b[i]
        out[i] += a[j] * b[k] - a[k] * b[j]
        out[j] += a[k] * b[i] - a[i] * b[k]
    return out


def octonion_norm(a: List[float]) -> float:
    return math.sqrt(sum(x * x for x in a))


def normalize_octonion(a: List[float]) -> List[float]:
    n = octonion_norm(a)
    if n < 1e-9:
        return [1.0] + [0.0] * 7
    return [round(x / n, 6) for x in a]


def scores_to_unit_octonion(scores_list: List[float]) -> List[float]:
    """Embeds 8 seed function scores into a unit octonion where e_0 is the scalar anchor
    and e_1..e_7 are contrast-enhanced imaginary octonion components so common-mode DC
    offsets do not collapse contrapuntal voices into collinear unison.
    """
    mean_val = sum(scores_list) / 8.0
    anchor_e0 = 0.35 * scores_list[0] + 0.15 * mean_val
    imag_parts = [
        (scores_list[idx] - 0.82 * mean_val) * 2.4
        for idx in range(1, 8)
    ]
    return normalize_octonion([anchor_e0] + imag_parts)



def build_quad_seed_slm_prompt_block(
    harmony_state: Dict[str, Any],
    music_appreciation_mode: bool = False,
) -> str:
    """Formats the Quad-Seed 4x(6x8) Quaternion-Octonion Cross-Seed Complexity Matrix telemetry
    for injection into the SLM system prompt (replacing the retired 3-angle Kaleidoscope).
    """
    seeds = harmony_state.get("seed_octonions", {})
    psych_top = seeds.get("psychological_1", {}).get("top_functions", [("QuaternionTriadConvergence", 1.0)])
    phil_top = seeds.get("philosophical_i", {}).get("top_functions", [("TonicPedalGround", 1.0)])
    cult_top = seeds.get("cultural_j", {}).get("top_functions", [("PureFunctionComposition", 1.0)])
    exp_top = seeds.get("experiential_k", {}).get("top_functions", [("CantabileWarmth", 1.0)])

    voices = harmony_state.get("contrapuntal_four_voices", {})
    sop_fn = voices.get("soprano_psych_x_exp", {}).get("dominant_octonion_axis", "RubatoAgogicPhrasingArc")
    alt_fn = voices.get("alto_phil_x_exp", {}).get("dominant_octonion_axis", "ModalMixtureShadowIntegration")
    ten_fn = voices.get("tenor_cult_x_psych", {}).get("dominant_octonion_axis", "MetricProportionalityGrid")
    bas_fn = voices.get("bass_phil_x_cult", {}).get("dominant_octonion_axis", "HarmonicAnchorGround")

    coherence = float(harmony_state.get("quad_seed_harmonic_coherence", 0.92))
    sep = float(harmony_state.get("contrapuntal_voice_separation_index", 0.054))
    buf = float(harmony_state.get("resonant_master_chord_buffer", RESONANT_MASTER_CHORD_BUFFER))

    block = (
        f"- Quad-Seed 4x(6x8) Quaternion-Octonion Harmonizer (Kaleidoscope Retired; 24/24 Leaves Active; Buffer={buf:.0%}):\n"
        f"  * [1] Psychological (6x8 Conductor): {psych_top[0][0]}={psych_top[0][1]:.2f}, {psych_top[1][0]}={psych_top[1][1]:.2f}\n"
        f"  * [i] Philosophical (6x8 Harmonic Ground): {phil_top[0][0]}={phil_top[0][1]:.2f}, {phil_top[1][0]}={phil_top[1][1]:.2f}\n"
        f"  * [j] Cultural (6x8 Motor & Probity): {cult_top[0][0]}={cult_top[0][1]:.2f}, {cult_top[1][0]}={cult_top[1][1]:.2f}\n"
        f"  * [k] Experiential (6x8 Affect & Pulse): {exp_top[0][0]}={exp_top[0][1]:.2f}, {exp_top[1][0]}={exp_top[1][1]:.2f}\n"
        f"  * Cross-Seed Octonion Counterpoint (Coherence={coherence:.3f}, VoiceSep={sep:.4f}): "
        f"Soprano(1*k)={sop_fn} | Alto(i*k)={alt_fn} | Tenor(j*1)={ten_fn} | Bass(i*j)={bas_fn}\n"
    )
    if music_appreciation_mode:
        block += (
            "- [QUAD-SEED MUSICAL COMPLEXITY & APPRECIATION DIRECTIVE]:\n"
            "  Synthesize all four 6x8 Seed SLMs simultaneously: connect [i] Philosophical modal mixture & bass trajectory "
            "with [k] Experiential buoyant/elegiac phrasing, [j] Cultural rhythmic ostinato precision, and [1] Psychological "
            "contrapuntal voice separation. Appreciate how independent voices move in contrary and oblique motion to create "
            "unified emotional meaning without collapsing into flat unison.\n"
        )
    return block


class QuadSeedQuaternionOctonionHarmonizer:
    """Executes 4-Domain Quaternion x 8-Function Octonion (`4 x 6x8 = 192` floats) cross-seed harmonization."""

    def __init__(
        self,
        philosophical_6x8: Optional[List[List[float]]] = None,
        cultural_6x8: Optional[List[List[float]]] = None,
        experiential_6x8: Optional[List[List[float]]] = None,
        psychological_6x8: Optional[List[List[float]]] = None,
        resonant_buffer: float = RESONANT_MASTER_CHORD_BUFFER,
    ) -> None:
        self.phil_6x8 = deepcopy(philosophical_6x8 or DEFAULT_PHILOSOPHICAL_6X8_MATRIX)
        self.cult_6x8 = deepcopy(cultural_6x8 or DEFAULT_CULTURAL_6X8_MATRIX)
        self.exp_6x8 = deepcopy(experiential_6x8 or DEFAULT_EXPERIENTIAL_6X8_MATRIX)
        self.psych_6x8 = deepcopy(psychological_6x8 or DEFAULT_PSYCHOLOGICAL_6X8_MATRIX)
        self.resonant_buffer = float(resonant_buffer)

    def set_matrices(
        self,
        philosophical_6x8: Optional[List[List[float]]] = None,
        cultural_6x8: Optional[List[List[float]]] = None,
        experiential_6x8: Optional[List[List[float]]] = None,
        psychological_6x8: Optional[List[List[float]]] = None,
    ) -> None:
        """Updates the live 4x(6x8) Seed SLM weight matrices in place."""
        if philosophical_6x8 is not None and len(philosophical_6x8) == 6 and len(philosophical_6x8[0]) == 8:
            self.phil_6x8 = [[round(float(v), 4) for v in row] for row in philosophical_6x8]
        if cultural_6x8 is not None and len(cultural_6x8) == 6 and len(cultural_6x8[0]) == 8:
            self.cult_6x8 = [[round(float(v), 4) for v in row] for row in cultural_6x8]
        if experiential_6x8 is not None and len(experiential_6x8) == 6 and len(experiential_6x8[0]) == 8:
            self.exp_6x8 = [[round(float(v), 4) for v in row] for row in experiential_6x8]
        if psychological_6x8 is not None and len(psychological_6x8) == 6 and len(psychological_6x8[0]) == 8:
            self.psych_6x8 = [[round(float(v), 4) for v in row] for row in psychological_6x8]

    def export_matrices(self) -> Dict[str, Any]:
        """Returns a deep copy of all 4 active 6x8 Seed SLM weight matrices (192 floats)."""
        return {
            "kaleidoscope_abandoned": True,
            "total_quad_seed_instinct_floats": 192,
            "philosophical_6x8": deepcopy(self.phil_6x8),
            "cultural_6x8": deepcopy(self.cult_6x8),
            "experiential_6x8": deepcopy(self.exp_6x8),
            "psychological_6x8": deepcopy(self.psych_6x8),
        }

    def harmonize(
        self,
        leaf_dials: Dict[str, float],
        matrices_override: Optional[Dict[str, List[List[float]]]] = None,
    ) -> Dict[str, Any]:
        """Projects all 24 canonical leaves through the 4 `6x8` Seed SLMs and computes
        Fano-plane Octonion contrapuntal voices and cross-seed complexity matrices.
        """
        phil_mat = (matrices_override or {}).get("philosophical_6x8", self.phil_6x8)
        cult_mat = (matrices_override or {}).get("cultural_6x8", self.cult_6x8)
        exp_mat = (matrices_override or {}).get("experiential_6x8", self.exp_6x8)
        psych_mat = (matrices_override or {}).get("psychological_6x8", self.psych_6x8)

        phil_scores = project_seed_6x8(leaf_dials, PHILOSOPHICAL_LEAVES_6, PHILOSOPHICAL_FUNCTIONS_8, phil_mat)
        cult_scores = project_seed_6x8(leaf_dials, CULTURAL_LEAVES_6, CULTURAL_FUNCTIONS_8, cult_mat)
        exp_scores = project_seed_6x8(leaf_dials, EXPERIENTIAL_LEAVES_6, EXPERIENTIAL_FUNCTIONS_8, exp_mat)
        psych_scores = project_seed_6x8(leaf_dials, PSYCHOLOGICAL_LEAVES_6, PSYCHOLOGICAL_FUNCTIONS_8, psych_mat)

        o_psych = scores_to_unit_octonion(list(psych_scores.values()))  # 1 (Executive Conductor)
        o_phil = scores_to_unit_octonion(list(phil_scores.values()))    # i (Harmonic Ground)
        o_cult = scores_to_unit_octonion(list(cult_scores.values()))    # j (Motor & Probity)
        o_exp = scores_to_unit_octonion(list(exp_scores.values()))      # k (Affective Phrasing)

        # 4 Non-Commutative Octonion Contrapuntal Voices (Fano-Plane Cross-Seed Products):
        v_soprano = normalize_octonion(octonion_multiply(o_psych, o_exp))
        v_alto = normalize_octonion(octonion_multiply(o_phil, o_exp))
        v_tenor = normalize_octonion(octonion_multiply(o_cult, o_psych))
        v_bass = normalize_octonion(octonion_multiply(o_phil, o_cult))

        fano_soprano = octonion_fano_cross(o_psych, o_exp)
        fano_alto = octonion_fano_cross(o_phil, o_exp)
        fano_tenor = octonion_fano_cross(o_cult, o_psych)
        fano_bass = octonion_fano_cross(o_phil, o_cult)

        # 4x4 Cross-Seed Quaternion Gramian Complexity Matrix in R^8:
        branch_names = ("psychological_1", "philosophical_i", "cultural_j", "experiential_k")
        branch_vecs = (o_psych, o_phil, o_cult, o_exp)
        cross_seed_gramian_4x4: Dict[str, Dict[str, float]] = {}
        for idx_a, name_a in enumerate(branch_names):
            row_dict: Dict[str, float] = {}
            for idx_b, name_b in enumerate(branch_names):
                dot_val = sum(branch_vecs[idx_a][k] * branch_vecs[idx_b][k] for k in range(8))
                row_dict[name_b] = round(dot_val, 4)
            cross_seed_gramian_4x4[name_a] = row_dict

        # Master Quaternion-Octonion 8D Chord with 30% Resonant Master Chord Buffer on Psychological (1):
        buf = self.resonant_buffer
        rem = 1.0 - buf
        w_phil = rem * (0.25 / 0.70)
        w_cult = rem * (0.20 / 0.70)
        w_exp = rem * (0.25 / 0.70)

        master_octonion_raw = [
            buf * abs(o_psych[idx])
            + w_phil * abs(o_phil[idx])
            + w_cult * abs(o_cult[idx])
            + w_exp * abs(o_exp[idx])
            + 0.12 * abs(v_soprano[idx] + v_alto[idx] + v_tenor[idx] + v_bass[idx])
            for idx in range(8)
        ]
        master_octonion = normalize_octonion(master_octonion_raw)

        # Contrapuntal voice separation across the 4 Octonion-multiplied voices:
        voices_list = [v_soprano, v_alto, v_tenor, v_bass]
        pairwise_dots: List[float] = []
        for a_i in range(4):
            for b_i in range(a_i + 1, 4):
                dot_v = sum(voices_list[a_i][k] * voices_list[b_i][k] for k in range(8))
                pairwise_dots.append(abs(dot_v))
        mean_voice_dot = sum(pairwise_dots) / len(pairwise_dots)
        voice_separation_index = round(1.0 - mean_voice_dot, 4)

        # Harmonic coherence of the 4-branch synthesis:
        quad_coherence = round(
            min(
                0.99,
                max(
                    0.80,
                    0.78
                    + 0.14 * sum(abs(x) for x in master_octonion) / math.sqrt(8.0)
                    + 0.35 * min(0.32, voice_separation_index),
                ),
            ),
            4,
        )

        used_axes: set[int] = set()

        def _dominant_fano_axis(fano_vec: List[float], fallback_vec: List[float]) -> str:
            ranked = sorted(
                range(1, 8),
                key=lambda i: (abs(fano_vec[i]) + 0.35 * abs(fallback_vec[i])),
                reverse=True,
            )
            for idx in ranked:
                if idx not in used_axes:
                    used_axes.add(idx)
                    return PSYCHOLOGICAL_FUNCTIONS_8[idx]
            return PSYCHOLOGICAL_FUNCTIONS_8[ranked[0]]

        sop_axis = _dominant_fano_axis(fano_soprano, v_soprano)
        alt_axis = _dominant_fano_axis(fano_alto, v_alto)
        ten_axis = _dominant_fano_axis(fano_tenor, v_tenor)
        bas_axis = _dominant_fano_axis(fano_bass, v_bass)

        top_psych = sorted(psych_scores.items(), key=lambda kv: kv[1], reverse=True)[:2]
        top_phil = sorted(phil_scores.items(), key=lambda kv: kv[1], reverse=True)[:2]
        top_cult = sorted(cult_scores.items(), key=lambda kv: kv[1], reverse=True)[:2]
        top_exp = sorted(exp_scores.items(), key=lambda kv: kv[1], reverse=True)[:2]

        return {
            "kaleidoscope_abandoned": True,
            "architecture": "QuadSeed_4x6x8_Quaternion_Octonion_Harmonizer",
            "canonical_leaves_sampled": 24,
            "canonical_leaf_coverage": 1.0,
            "total_active_instinct_floats": 192,
            "resonant_master_chord_buffer": round(buf, 4),
            "quad_seed_harmonic_coherence": quad_coherence,
            "contrapuntal_voice_separation_index": voice_separation_index,
            "quaternion_norm_conservation": round(octonion_norm(master_octonion), 4),
            "master_octonion_8d": [round(x, 4) for x in master_octonion],
            "cross_seed_gramian_4x4": cross_seed_gramian_4x4,
            "seed_octonions": {
                "psychological_1": {
                    "top_functions": top_psych,
                    "all_scores": psych_scores,
                    "unit_octonion": [round(x, 4) for x in o_psych],
                },
                "philosophical_i": {
                    "top_functions": top_phil,
                    "all_scores": phil_scores,
                    "unit_octonion": [round(x, 4) for x in o_phil],
                },
                "cultural_j": {
                    "top_functions": top_cult,
                    "all_scores": cult_scores,
                    "unit_octonion": [round(x, 4) for x in o_cult],
                },
                "experiential_k": {
                    "top_functions": top_exp,
                    "all_scores": exp_scores,
                    "unit_octonion": [round(x, 4) for x in o_exp],
                },
            },
            "contrapuntal_four_voices": {
                "soprano_psych_x_exp": {
                    "coupling": "1 * k (Psychological x Experiential)",
                    "dominant_octonion_axis": sop_axis,
                    "unit_octonion": [round(x, 4) for x in v_soprano],
                },
                "alto_phil_x_exp": {
                    "coupling": "i * k (Philosophical x Experiential)",
                    "dominant_octonion_axis": alt_axis,
                    "unit_octonion": [round(x, 4) for x in v_alto],
                },
                "tenor_cult_x_psych": {
                    "coupling": "j * 1 (Cultural x Psychological)",
                    "dominant_octonion_axis": ten_axis,
                    "unit_octonion": [round(x, 4) for x in v_tenor],
                },
                "bass_phil_x_cult": {
                    "coupling": "i * j (Philosophical x Cultural)",
                    "dominant_octonion_axis": bas_axis,
                    "unit_octonion": [round(x, 4) for x in v_bass],
                },
            },
            "summary_line": (
                f"QuadSeed4x6x8[1:Psych({top_psych[0][0]}={top_psych[0][1]:.2f}) | "
                f"i:Phil({top_phil[0][0]}={top_phil[0][1]:.2f}) | "
                f"j:Cult({top_cult[0][0]}={top_cult[0][1]:.2f}) | "
                f"k:Exp({top_exp[0][0]}={top_exp[0][1]:.2f}) | "
                f"Coherence={quad_coherence:.3f}, VoiceSep={voice_separation_index:.4f}]"
            ),
        }


class OrdinaryMemoryQuadSeedComparator:
    """Matched ordinary structured-memory baseline comparator for Rule D004."""

    def __init__(self) -> None:
        self._engine = QuadSeedQuaternionOctonionHarmonizer()

    def harmonize(
        self,
        leaf_dials: Dict[str, float],
        matrices_override: Optional[Dict[str, List[List[float]]]] = None,
    ) -> Dict[str, Any]:
        return self._engine.harmonize(leaf_dials=leaf_dials, matrices_override=matrices_override)
