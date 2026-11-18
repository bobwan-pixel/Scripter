#!/usr/bin/env python3
"""Validate Skil-cc 5-10 minute screenplay source and production metadata."""
from pathlib import Path
import argparse, json, sys
from screenplay import parse_screenplay

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--project",default="Skil-cc/projects/active")
    args=ap.parse_args()
    root=Path(args.project); errors=[]; warnings=[]
    prod_path=root/"PRODUCTION.json"; script_path=root/"SCREENPLAY.md"
    if not prod_path.exists(): errors.append("Missing PRODUCTION.json")
    if not script_path.exists(): errors.append("Missing SCREENPLAY.md")
    if errors:
        print("\n".join("ERROR: "+x for x in errors)); return 1
    try: prod=json.loads(prod_path.read_text(encoding="utf-8"))
    except Exception as e: errors.append(f"Invalid PRODUCTION.json: {e}"); prod={}
    try: script=script_path.read_text(encoding="utf-8")
    except Exception as e: errors.append(f"Cannot read screenplay: {e}"); script=""
    if "STATUS: TEMPLATE" in script: errors.append("SCREENPLAY.md is still a template. Add the approved film screenplay.")
    scenes=parse_screenplay(script)
    if not scenes: errors.append("No timed scenes found. Use: ## SCENE 01 | 00:00-00:45 | INT. LOCATION | DAY")
    minimum=int(prod.get("minimum_runtime_seconds",300)); maximum=int(prod.get("maximum_runtime_seconds",600))
    fps=int(prod.get("fps",24))
    if not 300 <= minimum <= maximum <= 600: errors.append("Runtime bounds must stay inside 300-600 seconds.")
    if fps not in (24,25,30,48,50,60): warnings.append(f"Unusual FPS setting: {fps}")
    previous_end=None
    for scene in scenes:
        if scene["end"] <= scene["start"]: errors.append(f"Scene {scene['number']:02d} has invalid duration.")
        if previous_end is not None:
            if scene["start"] < previous_end: errors.append(f"Scene {scene['number']:02d} overlaps the previous scene.")
            elif scene["start"] > previous_end: warnings.append(f"Gap before scene {scene['number']:02d}: {scene['start']-previous_end}s.")
        previous_end=scene["end"]
        if not scene["shots"]: warnings.append(f"Scene {scene['number']:02d} has no timed shots.")
        last_shot_end=None
        for shot in scene["shots"]:
            if shot["end"] <= shot["start"]: errors.append(f"Scene {scene['number']:02d}, shot {shot['number']:02d} has invalid duration.")
            if shot["start"] < scene["start"] or shot["end"] > scene["end"]: errors.append(f"Shot {shot['number']:02d} is outside scene {scene['number']:02d}.")
            if last_shot_end is not None and shot["start"] < last_shot_end: errors.append(f"Shots overlap in scene {scene['number']:02d}.")
            last_shot_end=shot["end"]
    if scenes:
        runtime=scenes[-1]["end"]-scenes[0]["start"]
        if runtime < minimum or runtime > maximum: errors.append(f"Screenplay runtime is {runtime}s, outside configured {minimum}-{maximum}s.")
        print(f"Scenes: {len(scenes)} | Shots: {sum(len(s['shots']) for s in scenes)} | Dialogue lines: {sum(len(s['dialogue']) for s in scenes)}")
        print(f"Runtime: {runtime}s ({runtime//60}:{runtime%60:02d}) | FPS: {fps} | Frames: {runtime*fps}")
    manifest=root/"ASSET-MANIFEST.json"
    if manifest.exists():
        try: json.loads(manifest.read_text(encoding="utf-8"))
        except Exception as e: errors.append(f"Invalid ASSET-MANIFEST.json: {e}")
    else: warnings.append("ASSET-MANIFEST.json is missing.")
    for w in warnings: print("WARNING:",w)
    for e in errors: print("ERROR:",e)
    print("VALIDATION:", "FAILED" if errors else "PASSED")
    return 1 if errors else 0

if __name__=="__main__": sys.exit(main())
