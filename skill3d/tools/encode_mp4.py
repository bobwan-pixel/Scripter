#!/usr/bin/env python3
"""Encode numbered frames and mux supplied dialogue audio without time-stretching/truncation."""
import argparse,json,shutil,subprocess
from pathlib import Path
def probe(path):
 r=subprocess.run(["ffprobe","-v","error","-show_entries","format=duration:stream=codec_type","-of","json",str(path)],capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr.strip())
 d=json.loads(r.stdout);return float(d.get("format",{}).get("duration",0)),[s.get("codec_type") for s in d.get("streams",[])]
def main():
 p=argparse.ArgumentParser();p.add_argument("--frames",required=True,help="frame filename pattern, e.g. renders/frames/frame_%%04d.png");p.add_argument("--audio",required=True);p.add_argument("--output",default="output/final.mp4");p.add_argument("--fps",type=int,default=24);p.add_argument("--start-number",type=int,default=1);p.add_argument("--frame-count",type=int,required=True);p.add_argument("--crf",type=int,default=18);a=p.parse_args()
 for t in ["ffmpeg","ffprobe"]:
  if not shutil.which(t):raise SystemExit(t+" not found")
 audio=Path(a.audio);out=Path(a.output);out.parent.mkdir(parents=True,exist_ok=True)
 if not audio.is_file():raise SystemExit("Dialogue audio not found: "+str(audio))
 picture=a.frame_count/a.fps;duration,_=probe(audio)
 if duration>picture+.25:raise SystemExit(f"Refusing to truncate dialogue: audio {duration:.3f}s > picture {picture:.3f}s. Extend picture or resolve source timing.")
 cmd=["ffmpeg","-y","-framerate",str(a.fps),"-start_number",str(a.start_number),"-i",a.frames,"-i",str(audio),"-map","0:v:0","-map","1:a:0","-frames:v",str(a.frame_count),"-c:v","libx264","-preset","medium","-crf",str(a.crf),"-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",str(out)]
 r=subprocess.run(cmd)
 if r.returncode:raise SystemExit(r.returncode)
 print("ENCODED",out.resolve(),"picture_seconds",round(picture,3),"dialogue_seconds",round(duration,3))
if __name__=="__main__":main()
