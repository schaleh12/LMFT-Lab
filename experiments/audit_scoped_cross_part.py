"""Post-hoc counterexample; excluded from preregistered primary metrics."""
import argparse
from pathlib import Path
from lmft_lab import scoped_attention as s, scoped_fixture as f
from lmft_lab.runtime_store import atomic_json


def audit():
    records=[r for r in f.initial_records("q6") if r["question"]=="payload_valid" or r["part"]=="check2" or r["value"] is False]
    assert all(f.registered_evidence(r) for r in records)
    result={"label":"post-hoc cross-part disagreement diagnostic; excluded from primary metrics","records":records,"conditions":{}}
    for mode in ("scoped-full","scoped-memory"):
        current=s.newborn(mode)
        current["ledger"]={r["evidence_id"]:{"record":r} for r in records}
        chosen,traces=s.select(current,f.public_case("q6"))
        result["conditions"][mode]={"support":s.support(current,f.public_case("q6"),"shielded"),"selected":chosen,"traces":traces}
    return result

if __name__=="__main__":
    parser=argparse.ArgumentParser();parser.add_argument("--output",required=True);args=parser.parse_args()
    output=Path(args.output)
    if output.exists():raise FileExistsError("Preserve earlier audit outputs; choose a fresh path")
    result=audit();atomic_json(output,result)
    for mode,item in result["conditions"].items():
        print(mode,"resolved:",item["support"]["resolved"],"selected:",item["selected"])
