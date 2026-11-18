#!/usr/bin/env python3
"""Render a Blender frame range in resumable chunks."""
import argparse,shutil,subprocess
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("blend");p.add_argument("--blender",default="blender");p.add_argument("--start",type=int,required=True);p.add_argument("--end",type=int,required=True);p.add_argument("--chunk",type=int,default=24);p.add_argument("--output",default="//renders/frames/frame_");p.add_argument("--format",default="PNG",choices=["PNG","JPEG","OPEN_EXR"]);p.add_argument("--log-dir",default="render-logs");a=p.parse_args()
 exe=shutil.which(a.blender) or a.blender;blend=Path(a.blend).resolve()
 if not blend.is_file():raise SystemExit("Blend file not found: "+str(blend))
 if a.start<1 or a.end<a.start or a.chunk<1:raise SystemExit("Invalid frame range/chunk")
 logs=Path(a.log_dir);logs.mkdir(parents=True,exist_ok=True);prefix=a.output
 if prefix.startswith("//"):prefix=str((blend.parent/prefix[2:]).resolve())
 Path(prefix).parent.mkdir(parents=True,exist_ok=True);ext="exr" if a.format=="OPEN_EXR" else a.format.lower()
 for first in range(a.start,a.end+1,a.chunk):
  last=min(a.end,first+a.chunk-1);missing=[f for f in range(first,last+1) if not Path(f"{prefix}{f:04d}.{ext}").is_file()]
  if not missing:print(f"SKIP {first}-{last}: frames already exist");continue
  runs=[];s=prev=missing[0]
  for f in missing[1:]:
   if f!=prev+1:runs.append((s,prev));s=f
   prev=f
  runs.append((s,prev))
  for s,e in runs:
   log=logs/f"frames_{s:06d}_{e:06d}.log";cmd=[exe,"-b",str(blend),"-s",str(s),"-e",str(e),"-o",prefix,"-F",a.format,"-a"]
   print("RUN"," ".join(cmd))
   with log.open("w",encoding="utf-8") as out:r=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT)
   if r.returncode:raise SystemExit(f"Blender failed for {s}-{e}; inspect {log}")
 print("RENDER_RANGE_COMPLETE",a.start,a.end)
if __name__=="__main__":main()
