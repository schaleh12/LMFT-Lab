# Metacognitive Priming Console Prototype — Protocol

**Authoritative Specification — Milestone 5 (2026-10-13)**

## 1. Research Purpose & Conceptual Alignment

This protocol implements the prototype bridging persistent capacity disambiguation with the frozen LMFT Philosophical seed nodes, fulfilling the user's conceptual specification of the Philosophical branch as a **gamified metacognitive disposition console for an autonomous helper android**.

As clarified in design alignment:
- The Philosophical branch is not an encyclopedic lexical classification bin, but an internal **metacognitive stance wheel** that primes situational awareness for conditional consideration.
- When the LMFT processes an external scenario (e.g. interpreting polysemous natural language), persistent capacity memory resolves the grounded semantic reading without LLM inference.
- That resolved meaning then deterministically activates the appropriate dyadic dials across the Philosophical seed:
  1. **Structure Dyad (`Order` vs `Chaos`)**: Stance towards systemic stability and organization versus disruption and absurdity.
  2. **Being Dyad (`Agency` vs `Existence`)**: Stance towards directive action, volition, and execution versus static state-of-affairs and ontological conditions.
  3. **Persistence Dyad (`Continuity` vs `Discreteness`)**: Stance towards continuous quantitative magnitude versus discrete serial steps.

---

## 2. Invariant Constraints & Rules

1. **Frozen Canonical 40-Node Seed (Rule D001):** The 40 canonical founding nodes, exact names, paths, and parent-child hierarchy in `birth.py` are strictly frozen. No nodes may be renamed, removed, rearranged, or added.
   Target nodes:
   - `philosophical/being/agency`
   - `philosophical/being/existence`
   - `philosophical/structure/order`
   - `philosophical/structure/chaos`
   - `philosophical/persistence/continuity`
   - `philosophical/persistence/discreteness`
2. **Zero Runtime LLM Calls:** Priming computation is 100% deterministic local Python execution.
3. **Calibrated Epistemic Abstention:** When persistent capacity memory abstains on unseen contexts, the console must not guess or inject arbitrary primes; it reports a neutral stance with an explicit `epistemic_abstention: true` flag.
4. **Matched Ordinary-Memory Baseline (Rule D004):** The priming calculation must produce byte-for-byte identical output digests across primary capacity stores and ordinary structured-memory baselines.
5. **Neutral Checkpoint Nonmutation:** Evaluating priming on input instances must not alter the underlying checkpoint SHA256.

---

## 3. Priming Transfer Function & Dyadic Algebra

For any disambiguated item producing sense $S \in \text{WordNet}$ with confidence $c \in [0, 1]$:
1. **Being Dyad**:
   - For directive/action senses (`order%1:10:03::`, `order%1:10:01::`):
     $\text{priming}(\text{agency}) = 0.85 \times c$, $\text{priming}(\text{existence}) = 0.40 \times c$.
   - For state/condition senses (`order%1:26:00::`):
     $\text{priming}(\text{agency}) = 0.20 \times c$, $\text{priming}(\text{existence}) = 0.85 \times c$.
2. **Structure Dyad**:
   - For stability/law/arrangement senses (`order%1:26:00::`, `order%1:26:02::`):
     $\text{priming}(\text{order}) = 0.80 \times c$, $\text{priming}(\text{chaos}) = 0.05 \times c$.
   - For directive command under institutional order (`order%1:10:03::`):
     $\text{priming}(\text{order}) = 0.70 \times c$, $\text{priming}(\text{chaos}) = 0.10 \times c$.
3. **Persistence Dyad**:
   - For continuous magnitude senses (`order%1:07:01::`):
     $\text{priming}(\text{continuity}) = 0.85 \times c$, $\text{priming}(\text{discreteness}) = 0.15 \times c$.
   - For discrete serial succession senses (`order%1:14:00::`, `order%1:10:02::`):
     $\text{priming}(\text{continuity}) = 0.20 \times c$, $\text{priming}(\text{discreteness}) = 0.85 \times c$.
4. **Abstention State**:
   - If decision is `abstain`, all priming values remain 0.0, with stance labeled `"neutral_open"`.
