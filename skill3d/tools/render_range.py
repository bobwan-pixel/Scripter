#!/usr/bin/env python3
"""Render a Blender frame range in resumable chunks using Blender's Python API.

Example:
 python render_range.py project.blend --blender blender --start 1 --end 240 --chunk 24 --output //renders/frames/frame_
Existing non-empty frame files are skipped. Each chunk is rendered in one Blender process.
"""
import argparse,json,shutil,subprocess
from pathlib import Path

def main():
 p=argparse.ArgumentParser()
 p.add_argument("blend")
 p.add_argument("--blender",default="blender")
 p.add_argument("--start",type=int,required=True)
 p.add_argument("--end",type=int,required=True)
 p.add_argument("--chunk",type=int,default=24)
 p.add_argument("--output",default="//renders/frames/frame_")
 p.add_argument("--format",default="PNG",choices=["PNG","JPEG","OPEN_EXR"])
 p.add_argument("--log-dir",default="render-logs")
 a=p.parse_args()
 exe=shutil.which(a.blender) or a.blender
 blend=Path(a.blend).resolve()
 if not blend.is_file():raise SystemExit("Blend file not found: "+str(blend))
 if a.start<1 or a.end<a.start or a.chunk<1:raise SystemExit("Invalid frame range/chunk")
 logs=Path(a.log_dir);logs.mkdir(parents=True,exist_ok=True)
 prefix=a.output
 if prefix.startswith("//"):prefix=str((blend.parent/prefix[2:]).resolve())
 Path(prefix).parent.mkdir(parents=True,exist_ok=True)
 ext={"PNG":"png","JPEG":"jpg","OPEN_EXR":"exr"}[a.format]
 for first in range(a.start,a.end+1,a.chunk):
  last=min(a.end,first+a.chunk-1)
  missing=[f for f in range(first,last+1) if not Path(f"{prefix}{f:04d}.{ext}").is_file()]
  if not missing:
   print(f"SKIP {first}-{last}: frames already exist")
   continue
  runs=[];s=prev=missing[0]
  for frame in missing[1:]:
   if frame!=prev+1:runs.append((s,prev));s=frame
   prev=frame
  runs.append((s,prev))
  for s,e in runs:
   script=logs/f"render_chunk_{s:06d}_{e:06d}.py"
   log=logs/f"frames_{s:06d}_{e:06d}.log"
   code=f"""import bpy, os, traceback
scene=bpy.context.scene
scene.render.image_settings.file_format={a.format!r}
scene.render.use_file_extension=True
prefix={prefix!r}
try:
 for frame in range({s}, {e}+1):
  scene.frame_set(frame)
  scene.render.filepath=prefix+f'{{frame:04d}}'
  bpy.ops.render.render(write_still=True)
  print('SKILL3D_FRAME_RENDERED', frame, scene.render.filepath, flush=True)
except Exception:
 traceback.print_exc()
 raise
"""
   script.write_text(code,encoding="utf-8")
   cmd=[exe,"-b",str(blend),"--python",str(script)]
   print("RUN"," ".join(cmd),flush=True)
   with log.open("w",encoding="utf-8") as out:r=subprocess.run(cmd,stdout=out,stderr=subprocess.STDOUT)
   if r.returncode:
    tail=log.read_text(encoding="utf-8",errors="replace").splitlines()[-80:]
    if tail:print("\n".join(tail))
    raise SystemExit(f"Blender failed for {s}-{e}; inspect {log}")
   absent=[f for f in range(s,e+1) if not Path(f"{prefix}{f:04d}.{ext}").is_file()]
   if absent:raise SystemExit(f"Blender exited successfully but frames are missing: {absent}")
 print("RENDER_RANGE_COMPLETE",a.start,a.end)
if __name__=="__main__":main()
