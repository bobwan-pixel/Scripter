#!/usr/bin/env python3
"""Technical MP4 checks and heuristic black/frozen-span detection; visual review remains required."""
import argparse,json,shutil,subprocess
from pathlib import Path
def main():
 p=argparse.ArgumentParser();p.add_argument("video");p.add_argument("--black-min",default="0.25");p.add_argument("--freeze-min",default="0.5");a=p.parse_args();v=Path(a.video)
 for t in ["ffprobe","ffmpeg"]:
  if not shutil.which(t):raise SystemExit(t+" not found")
 if not v.is_file() or not v.stat().st_size:raise SystemExit("Video missing or empty")
 q=subprocess.run(["ffprobe","-v","error","-show_streams","-show_format","-of","json",str(v)],capture_output=True,text=True)
 if q.returncode:raise SystemExit(q.stderr)
 d=json.loads(q.stdout);streams=d.get("streams",[]);video=next((s for s in streams if s.get("codec_type")=="video"),None);audio=next((s for s in streams if s.get("codec_type")=="audio"),None)
 report={"file":str(v.resolve()),"bytes":v.stat().st_size,"duration":float(d.get("format",{}).get("duration",0)),"video":video,"audio":audio,"black_spans":[],"freeze_spans":[]}
 if video:
  for name,expr in [("black_spans",f"blackdetect=d={a.black_min}:pix_th=0.10"),("freeze_spans",f"freezedetect=n=-50dB:d={a.freeze_min}")]:
   r=subprocess.run(["ffmpeg","-hide_banner","-i",str(v),"-vf",expr,"-an","-f","null","-"],capture_output=True,text=True)
   report[name]=[line.strip() for line in (r.stderr or "").splitlines() if ("black_" in line or "freeze_" in line)]
 report["technical_pass"]=bool(video and audio and report["duration"]>0);print(json.dumps(report,indent=2))
 if not report["technical_pass"]:raise SystemExit(1)
 print("NOTE: detections are heuristic; watch the video and compare mouth motion with original audio.")
if __name__=="__main__":main()
