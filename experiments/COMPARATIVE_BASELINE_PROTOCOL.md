# Comparative Baseline Benchmark Protocol

## 1. Research Purpose & Hypotheses
As mandated by [AGENTS.md](file:///c:/Users/schal/OneDrive/Desktop/LMFT%20based%20general%20AI/LMFT-Lab/AGENTS.md#L30-L33) (*"Compare future cognitive claims against simpler baselines, including an LLM with ordinary structured memory and propagation-disabled controls"*), this study evaluates the LMFT persistent capacity architecture against two conventional, non-fuzzy baselines across the complete 33-instance SemCor development corpus (`development.json`, *order* / *orders*).

### Baselines Defined
1. **Baseline A (Exact Key-Value Dictionary Lookup)**:
   - Maps exact syntactic context anchor strings directly to gold WordNet sense keys.
   - Evaluates whether continuous fuzzy node activations provide any discriminative accuracy benefit over a plain hash table dictionary.
2. **Baseline B (Naive Bag-of-Words Token Matcher)**:
   - Matches sentences based on unweighted token set intersections (simulating historical Phase B bag-of-words co-occurrence).
   - Evaluates susceptibility to false positives and out-of-context collisions.

### Preregistered Hypotheses
1. **Classification Accuracy Parity (H1)**: On exact-match instances, Baseline A (Key-Value) will achieve precision equivalent to LMFT (100% precision), demonstrating that discrete sense disambiguation can be achieved by simple associative tables.
2. **Bag-of-Words Vulnerability (H2)**: Baseline B (Bag-of-Words) will exhibit substantial false positive rates (>25%) and ambiguities due to lack of syntactic context bounding.
3. **Continuous Stance Differentiation (H3)**: The unique capability of LMFT lies not in discrete classification, but in continuous multi-axis posture regulation (all 24 canonical leaves), harmonic concordance ($H > 0.85$), and contextual register actuation, which discrete baselines cannot produce.
4. **Matched Ordinary-Memory Baseline Parity (H4)**: Primary and ordinary-memory comparators will achieve byte-for-byte evaluation parity (Rule D004), confirming checkpoint nonmutation and determinism.

---

## 2. Evaluation Specification
- **Dataset**: All 33 SemCor development instances (`development.json`, SHA256: `77782985661f8426b3095e1573ae540da988a81c9d4e3b7b6c5c36280dd46c90`).
- **Memory Checkpoints**: Batch 1 (`97406aab...`) and Batch 2 (`6da29752...`).
- **Inference Mode**: 100% unassisted offline evaluation (zero runtime model calls).
- **Metrics**: Accuracy, Precision on Fired Cases, False Positive Rate, Ambiguity Rate, Behavioral Stance Resolution, and Execution Latency.
