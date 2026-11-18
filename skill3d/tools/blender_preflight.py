#!/usr/bin/env python3
"""Check Blender/FFmpeg availability and ask Blender to report its build/device context."""
import argparse, json, os, shutil, subprocess, sys
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--blender",default="blender")
    ap.add_argument("--out",default="blender-preflight.json")
    a=ap.parse_args()
    exe=shutil.which(a.blender) or (a.blender if Path(a.blender).is_file() else None)
    report={"blender_executable":exe,"ffmpeg":shutil.which("ffmpeg"),"ffprobe":shutil.which("ffprobe"),"python":sys.version,"platform":sys.platform}
    if exe:
        v=subprocess.run([exe,"--version"],capture_output=True,text=True,timeout=30)
        report["blender_version"]=v.stdout.splitlines()[0] if v.stdout else v.stderr.strip()
        expr="import bpy,json; print('SKILL3D_PREFLIGHT='+json.dumps({'version':bpy.app.version_string,'background':bpy.app.background,'engines':sorted({e.identifier for e in bpy.types.RenderSettings.bl_rna.properties['engine'].enum_items})}))"
        p=subprocess.run([exe,"-b","--factory-startup","--python-expr",expr],capture_output=True,text=True,timeout=90)
        report["blender_probe_exit_code"]=p.returncode
        report["blender_probe_output"]=p.stdout[-4000:]
        report["blender_probe_error"]=p.stderr[-4000:]
    else:
        report["error"]="Blender executable not found"
    Path(a.out).write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2))
    if not exe or report.get("blender_probe_exit_code") != 0: raise SystemExit(1)
if __name__=="__main__": main()
