# LMFT-Lab Developer Tooling & Observability Suite

> [!IMPORTANT]
> **DEVELOPER OBSERVABILITY & INTERACTION TOOLING ONLY**
> Files in this `tools/` directory are quarantined developer aids, diagnostic sandboxes, and visualizers.
> They are **NOT** part of the core `src/lmft_lab` runtime library or shipping package.
> Packaging manifests explicitly target `src/lmft_lab`, leaving this directory cleanly quarantined.

---

## Tool Roster

### 1. The Brain Observatory (`observatory.html`)
- **Type**: Zero-dependency standalone HTML5/SVG/Canvas dashboard.
- **Usage**: Double-click to open in any web browser (Chrome, Edge, Firefox, Safari).
- **Features**:
  - Drag-and-drop or upload any `.lmft.json` individual package.
  - Interactive 40-node founding tree visualizer (color-coded by domain: Cultural, Philosophical, Experiential, Psychological).
  - 24-Leaf Disposition Radar (live polar/spider chart of internal equilibrium).
  - Cognitive Telemetry Gauges (Affective Plasticity $\alpha$, Prerequisite Coherence Index, Homeostatic Balance Score).
  - Episodic Memory & Consolidation Replay Scrubber.

### 2. Interactive Living REPL (`talk_to_lmft.py`)
- **Type**: Interactive terminal pair-interaction interface.
- **Usage**:
  ```bash
  python tools/talk_to_lmft.py
  # Or load a saved individual:
  python tools/talk_to_lmft.py --load path/to/individual.lmft.json
  ```
- **Features**:
  - Live conversational inputs processed turn-by-turn through the 10-faculty Cognitive Heartbeat.
  - Real-time Mental Telemetry box on every turn (plasticity, coherence, homeostasis, speaking register).
  - Built-in commands: `/sleep [cycles]`, `/status`, `/save <path>`, `/load <path>`, `/quit`.

### 3. Sandboxed "Mindprint" Diagnostic Battery (`mindprint_diagnostic.py`)
- **Type**: Non-destructive, read-only digital twin evaluation battery.
- **Usage**:
  ```bash
  python tools/mindprint_diagnostic.py
  # Or test a specific individual:
  python tools/mindprint_diagnostic.py --package path/to/individual.lmft.json
  ```
- **Safety Guarantee**:
  - Mounts packages **strictly read-only**.
  - Clones an ephemeral in-memory digital twin in volatile RAM.
  - Runs 4 stress challenges: Volatility Shock Dampening, Prerequisite Coherence Defense, Episodic Memory Consolidation, and Idle Drift Relaxation.
  - Emits an official **Mindprint Diagnostic Card** and dissolves the digital twin from RAM with **zero mutation** of the source file.

### 4. Intersubjective "Symposium" (`symposium.py`)
- **Type**: Multi-agent resonance chamber.
- **Usage**:
  ```bash
  python tools/symposium.py --rounds 5
  ```
- **Features**:
  - Spawns two distinct LMFT temperaments (e.g., *The Empiricist* vs. *The Empath*).
  - Runs a structured multi-turn dialogue where each entity evaluates the other's propositions through its prerequisite gate and affective homeostasis governor.
  - Tracks mutual coherence, reciprocal resonance, and worldview divergence/convergence.
