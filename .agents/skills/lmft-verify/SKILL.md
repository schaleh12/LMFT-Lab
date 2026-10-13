---
name: lmft-verify
description: Run the LMFT-Lab test suite, preflight checks, and regression verification under strict reproducibility rules.
---

# LMFT-Lab Verification Protocol

Use this skill when checking working tree integrity, executing regression tests, or verifying that changes comply with the repository contracts.

## 1. Startup Order & Baseline Integrity
Always verify context in this order before modifying or testing code:
1. `AGENTS.md` - stable working contract and frozen seed constraints.
2. `PROJECT_STATE.md` - current active milestone snapshot, evidence limits, and next task.
3. `DECISIONS.md` - consequential decisions and status.

## 2. Running Regression Tests
The project requires `PYTHONPATH=src` for all test runs to ensure child worker processes resolve package modules correctly.

Execute in PowerShell from the repository root:
```powershell
$env:PYTHONPATH='src'; .\.venv\Scripts\python.exe -m pytest -q
```

To run a targeted test file:
```powershell
$env:PYTHONPATH='src'; .\.venv\Scripts\python.exe -m pytest tests/<test_file>.py -q
```

## 3. Strict Verification Invariants
- **Frozen Seed:** Never modify, rename, reorder, or expand the 40 founding nodes in `Minimal Specification Section 4`.
- **Historical Evidence:** Never delete, overwrite, or mutate historical experiment results or archive folders under `outputs/`.
- **Ordinary Memory Baselines:** Maintain matched-memory controls and report equivalence or negative results truthfully.
- **Process Restart Parity:** Verify that persisted state and restarted processes match uninterrupted references where required.
