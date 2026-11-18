#!/usr/bin/env python3
"""Inspect audio files with ffprobe; does not modify or transcode source audio."""
import argparse, json, shutil, subprocess
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    args=ap.parse_args()
    if not shutil.which("ffprobe"):
        raise SystemExit("ffprobe not found. Install FFmpeg and ensure ffprobe is on PATH.")
    reports=[]
    for raw in args.files:
        p=Path(raw)
        if not p.is_file():
            reports.append({"file":raw,"error":"not found"})
            continue
        cmd=["ffprobe","-v","error","-show_entries","format=duration,format_name:stream=codec_type,codec_name,sample_rate,channels,channel_layout","-of","json",str(p)]
        r=subprocess.run(cmd,capture_output=True,text=True)
        if r.returncode:
            reports.append({"file":str(p),"error":r.stderr.strip()})
            continue
        data=json.loads(r.stdout)
        reports.append({"file":str(p),"format":data.get("format",{}),"streams":data.get("streams",[])})
    print(json.dumps(reports,indent=2,ensure_ascii=False))

if __name__=="__main__":
    main()
