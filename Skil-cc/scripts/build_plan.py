#!/usr/bin/env python3
"""Build a machine-readable timed production plan from SCREENPLAY.md."""
from pathlib import Path
import argparse, json
from datetime import datetime, timezone
from screenplay import parse_screenplay

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",default="Skil-cc/projects/active")
    ap.add_argument("--out",default=None)
    args=ap.parse_args()
    root=Path(args.project)
    production=json.loads((root/"PRODUCTION.json").read_text(encoding="utf-8"))
    screenplay=(root/"SCREENPLAY.md").read_text(encoding="utf-8")
    scenes=parse_screenplay(screenplay)
    if not scenes: raise SystemExit("No timed scenes found. See references/SCREENPLAY-FORMAT.md")
    plan={"schema_version":1,"generated_at":datetime.now(timezone.utc).isoformat(),
          "source":{"screenplay":"SCREENPLAY.md","characters":"CHARACTERS.md","world":"WORLD.md","assets":"ASSET-MANIFEST.json"},
          "production":production,
          "runtime":{"start_seconds":scenes[0]["start"],"end_seconds":scenes[-1]["end"],
                     "duration_seconds":scenes[-1]["end"]-scenes[0]["start"],
                     "fps":production.get("fps",24),
                     "frame_count":(scenes[-1]["end"]-scenes[0]["start"])*production.get("fps",24)},
          "scenes":scenes}
    out=Path(args.out) if args.out else root/"production-plan.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"Created {out} | {len(scenes)} scenes | {sum(len(s['shots']) for s in scenes)} shots | {plan['runtime']['duration_seconds']}s")
if __name__=="__main__": main()
