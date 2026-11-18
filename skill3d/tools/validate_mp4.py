#!/usr/bin/env python3
"""Check that a rendered MP4 exists, has video/audio streams, and matches expected runtime."""
import argparse, json, shutil, subprocess
from pathlib import Path

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--min-seconds",type=float,default=0)
    ap.add_argument("--max-seconds",type=float,default=0)
    args=ap.parse_args()
    p=Path(args.video)
    if not p.is_file() or p.stat().st_size==0:
        raise SystemExit("FAIL: output file is missing or empty.")
    if not shutil.which("ffprobe"):
        raise SystemExit("ffprobe not found. Install FFmpeg.")
    cmd=["ffprobe","-v","error","-show_entries","format=duration,format_name:stream=codec_type,codec_name,width,height,r_frame_rate,sample_rate,channels","-of","json",str(p)]
    r=subprocess.run(cmd,capture_output=True,text=True)
    if r.returncode:
        raise SystemExit("FAIL: ffprobe could not read the file: "+r.stderr.strip())
    data=json.loads(r.stdout)
    duration=float(data.get("format",{}).get("duration",0))
    streams=data.get("streams",[])
    video=next((s for s in streams if s.get("codec_type")=="video"),None)
    audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
    errors=[]
    if not video: errors.append("missing video stream")
    if not audio: errors.append("missing audio stream")
    if duration<=0: errors.append("invalid duration")
    if args.min_seconds and duration<args.min_seconds: errors.append(f"duration {duration:.2f}s below minimum {args.min_seconds:.2f}s")
    if args.max_seconds and duration>args.max_seconds: errors.append(f"duration {duration:.2f}s above maximum {args.max_seconds:.2f}s")
    print(json.dumps({"file":str(p.resolve()),"bytes":p.stat().st_size,"duration_seconds":duration,"format":data.get("format",{}).get("format_name"),"video":video,"audio":audio,"errors":errors},indent=2))
    if errors: raise SystemExit(1)
    print("PASS: MP4 structure and requested duration checks passed. Visual quality and lip-sync still require human review.")

if __name__=="__main__":
    main()
