#!/usr/bin/env python3
"""Check Blender/FFmpeg availability and ask Blender to report its build/device context."""
import argparse,json,shutil,subprocess,sys
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("--blender",default="blender");p.add_argument("--out",default="blender-preflight.json");a=p.parse_args()
 exe=shutil.which(a.blender) or (a.blender if Path(a.blender).is_file() else None)
 r={"blender_executable":exe,"ffmpeg":shutil.which("ffmpeg"),"ffprobe":shutil.which("ffprobe"),"python":sys.version,"platform":sys.platform}
 if exe:
  v=subprocess.run([exe,"--version"],capture_output=True,text=True,timeout=30);r["blender_version"]=(v.stdout or v.stderr).splitlines()[0]
  code="import bpy,json; print('SKILL3D_PREFLIGHT='+json.dumps({'version':bpy.app.version_string,'background':bpy.app.background}))"
  q=subprocess.run([exe,"-b","--factory-startup","--python-expr",code],capture_output=True,text=True,timeout=90)
  r.update({"probe_exit_code":q.returncode,"probe_stdout":q.stdout[-4000:],"probe_stderr":q.stderr[-4000:]})
 else:r["error"]="Blender executable not found"
 Path(a.out).write_text(json.dumps(r,indent=2),encoding="utf-8");print(json.dumps(r,indent=2))
 if not exe or r.get("probe_exit_code")!=0:raise SystemExit(1)
if __name__=="__main__":main()
