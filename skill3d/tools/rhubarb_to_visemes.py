#!/usr/bin/env python3
"""Convert Rhubarb Lip Sync JSON mouth cues into Skill3D Blender viseme events.

Rhubarb CLI example:
  rhubarb -r phonetic -f json -d dialogue.txt -o rhubarb.json voice.wav
Then:
  python rhubarb_to_visemes.py rhubarb.json --out visemes.json --fps 24
The mapping is a practical approximation. Review the mouth track against the actual recording.
"""
import argparse,json
from pathlib import Path

MAP={"A":"MBP","B":"TEETH","C":"E","D":"A","E":"O","F":"U","G":"FV","H":"L_TH","X":"REST"}

def main():
    p=argparse.ArgumentParser()
    p.add_argument("input",help="Rhubarb JSON output")
    p.add_argument("--out",default="visemes.json")
    p.add_argument("--fps",type=float,default=24)
    p.add_argument("--object",default="SK3D_Mouth")
    a=p.parse_args()
    src=Path(a.input)
    if not src.is_file(): raise SystemExit("Rhubarb JSON not found: "+str(src))
    data=json.loads(src.read_text(encoding="utf-8"))
    cues=data.get("mouthCues")
    if not isinstance(cues,list): raise SystemExit("Input does not contain a Rhubarb mouthCues array")
    events=[]
    for cue in cues:
        shape=str(cue.get("value","")).upper()
        if shape not in MAP: raise SystemExit("Unknown Rhubarb mouth cue: "+shape)
        start=float(cue["start"]); end=float(cue["end"])
        if start<0 or end<=start: raise SystemExit("Invalid cue time range")
        events.append({"start":start,"end":end,"viseme":MAP[shape],"source_shape":shape})
    result={"fps":a.fps,"object":a.object,"events":events,"mapping":MAP,"approximate":True}
    out=Path(a.out);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(json.dumps({"output":str(out.resolve()),"events":len(events),"fps":a.fps,"mapping":MAP},ensure_ascii=False,indent=2))
    print("Review timing and shape mapping against the original audio before final render.")
if __name__=="__main__": main()
