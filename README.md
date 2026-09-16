# GFT-Lab

Experimental development environment for Genetic Fuzzy Tree (GFT) based artificial intelligence.

## Project goals

- Develop inspectable Genetic Fuzzy Tree reasoning systems.
- Experiment with fuzzy reasoning and genetic evolution.
- Develop co-evolving GFT architectures.
- Keep GFT reasoning separate from the LLM language/translation layer.
- Record reproducible evolutionary experiments.

## Recreate the development environment

Use CPython 3.12 (the recorded local baseline is 3.12.3). From the repository
root on Windows, run:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -c "import numpy, scipy, deap, skfuzzy, networkx, pytest; print('Imports OK')"
```

On macOS/Linux, use `python3.12 -m venv .venv` and replace
`.\.venv\Scripts\python.exe` with `.venv/bin/python` in the remaining commands.
Activation is optional because these commands use the virtual environment's
Python explicitly. The local `.venv` directory is ignored by Git.

`pyproject.toml` declares Python 3.12 compatibility and the five direct runtime
dependencies, with pytest in a separate development dependency group. The
requirements files pin the installed direct and transitive package versions:
`requirements.txt` is runtime-only; `requirements-dev.txt` includes runtime and
test dependencies. Use the latter for reproducible development setup with the
existing pip 24.0; no additional environment manager is required.

The minimal Python package lives in `src/gft_lab`. Pytest adds `src` to its import
path so tests use this checkout. Distribution packaging and a build backend are
deferred; use the requirements commands above rather than `pip install .`.
The placeholder project version is `0.0.0`. Outside pytest, importing `gft_lab`
currently requires adding `src` to Python's import path.

The pins record the working Windows CPython 3.12.3 environment, not a
cross-platform, hash-verified lock. Other platforms have not yet been validated;
the Windows-only colorama dependency has a platform marker. Package versions
are fixed, but Python patch versions and native numerical libraries can still
affect experimental results. Record those details alongside experiment seeds
and configuration when experiments are introduced.

Dependency updates should be deliberate: update the declarations and pinned
snapshots together, verify imports and `pip check`, and run the relevant tests.
Run tests with `.\.venv\Scripts\python.exe -m pytest` (or the macOS/Linux
equivalent). Currently the only test checks that the local package imports;
there is no GFT implementation or behavioral test suite yet.

## Repository layout

```text
src/gft_lab/  Minimal Python package; future GFT implementation
tests/       Automated tests; currently a package import sanity check
docs/        Research specifications, hypotheses, and design documentation
experiments/ Controlled experiments and reproducibility records
```

See [the documentation index](docs/INDEX.md) for established decisions and open
research questions, and [the experiment guidelines](experiments/README.md) for
reproducibility requirements. These directories establish places for future work;
they do not define a GFT architecture or an evolutionary experiment.
