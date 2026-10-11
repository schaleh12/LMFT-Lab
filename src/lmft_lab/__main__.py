"""Run a bounded local-model observation through LMFT."""
import argparse
import json
import sys
from pathlib import Path
from .birth import create_birth_state
from .local_models import LocalModels, load_config
from .model_assets import ModelError
from .processing import process_observation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=Path("config/local_models.json"))
    parser.add_argument("--observation", required=True)
    parser.add_argument("--event-id", required=True)
    parser.add_argument("--individual-id", default="local-demo")
    parser.add_argument("--birth-event-id", default="local-demo-birth")
    parser.add_argument("--offline", action="store_true")
    parser.add_argument("--trace", type=Path, required=True, help="new JSON trace file; never overwritten")
    args = parser.parse_args()
    try:
        config = load_config(args.config)
        state = create_birth_state(args.individual_id, birth_event_id=args.birth_event_id,
                                   random_seed=config["generation"]["seed"])
        # Exclusive creation avoids overwriting a prior run, even on failure.
        args.trace.parent.mkdir(parents=True, exist_ok=True)
        with args.trace.open("x", encoding="utf-8") as output:
            code = 0
            try:
                with LocalModels(config, offline=args.offline) as models:
                    trace = process_observation(state, args.observation, event_id=args.event_id, models=models)
            except ModelError as exc:
                trace = getattr(exc, "processing_trace", {"status": "failed", "error": str(exc)})
                code = 1
            json.dump(trace, output, ensure_ascii=False, indent=2, allow_nan=False)
            output.write("\n")
        print(f"{trace['status']}: {args.trace}")
        if code:
            print(trace.get("error", "model failure"), file=sys.stderr)
        else:
            print(trace["contemplation"]["summary"])
            print("No persistent judgment or constitutional changes.")
        return code
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"LMFT configuration/input error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
