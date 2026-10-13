"""CLI runner and process restart verification harness for persistent contextual disambiguation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys

from lmft_lab.local_models import strict_json
from lmft_lab.runtime_store import digest, atomic_json
import persistent_disambiguation as pd


def verify_restart(checkpoint_path, dev_path):
    """Executes evaluation in a fresh child process to verify complete process restart parity."""
    cmd = [
        sys.executable,
        str(Path(pd.__file__).resolve()),
        '--checkpoint', str(checkpoint_path),
        '--dev-export', str(dev_path),
    ]
    env = {**os.environ, 'PYTHONPATH': f"{pd.ROOT / 'src'};{pd.ROOT / 'experiments'}"}
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, timeout=60)
    if proc.returncode != 0:
        raise RuntimeError(f"Child process restart failed:\n{proc.stderr}")
    return strict_json(proc.stdout)


def run(checkpoint_path, dev_path, output_dir):
    chk_p = Path(checkpoint_path).resolve()
    dev_p = Path(dev_path).resolve()
    out_p = Path(output_dir).resolve()
    out_p.mkdir(parents=True, exist_ok=True)

    # 1. Capture before-state
    before_chk_sha = hashlib.sha256(chk_p.read_bytes()).hexdigest()
    before_dev_sha = hashlib.sha256(dev_p.read_bytes()).hexdigest()

    # 2. Run in-process study
    summary = pd.run_disambiguation_study(chk_p, dev_p, out_p)

    # 3. Verify in separate fresh process
    restart_summary = verify_restart(chk_p, dev_p)

    # 4. Assert nonmutation and restart invariance
    after_chk_sha = hashlib.sha256(chk_p.read_bytes()).hexdigest()
    if after_chk_sha != before_chk_sha:
        raise ValueError("Checkpoint mutation detected! State must be read-only during inference.")

    if summary['evaluation_digest'] != restart_summary['evaluation_digest']:
        raise ValueError("Restart divergence detected between in-process and fresh-process runs.")

    summary['restart_verification'] = {
        'restart_succeeded': True,
        'checkpoint_nonmutation': True,
        'checkpoint_sha256': before_chk_sha,
        'development_sha256': before_dev_sha,
        'evaluation_digest': summary['evaluation_digest'],
    }

    atomic_json(out_p / 'verified_summary.json', summary)
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--checkpoint', required=True)
    parser.add_argument('--dev-export', required=True)
    parser.add_argument('--output-dir', required=True)
    args = parser.parse_args()
    res = run(args.checkpoint, args.dev_export, args.output_dir)
    print(pd.canonical(res))
