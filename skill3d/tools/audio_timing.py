#!/usr/bin/env python3
"""Align user-supplied dialogue text to audio for animation timing only.

Usage: python audio_timing.py dialogue.wav dialogue-script.txt --out production/audio-timing
Uses faster-whisper/openai-whisper word timestamps when installed. Otherwise detects speech
segments with FFmpeg silence detection and aligns the exact supplied phrases approximately.
It never edits or generates dialogue/audio.
"""
import argparse,json,re,subprocess
from pathlib import Path

def run(cmd):
 r=subprocess.run(cmd,capture_output=True,text=True)
 if r.returncode:raise RuntimeError(r.stderr[-1500:])
 return r.stdout,r.stderr

def duration(path):
 out,_=run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(path)])
 return float(out.strip())

def syllables(word):
 w=re.sub(r"[^a-zA-ZÀ-ÿ]","",word.lower())
 if not w:return 1
 # Lightweight English/Indonesian vowel-group estimate, not phoneme recognition.
 groups=re.findall(r"[aeiouyàáâäèéêëìíîïòóôöùúûü]+",w)
 n=len(groups)
 if w.endswith("e") and len(w)>3 and not w.endswith(("le","ye")):n-=1
 return max(1,n)

def segments(path,threshold="-36dB",minimum="0.12"):
 _,err=run(["ffmpeg","-hide_banner","-i",str(path),"-af",f"silencedetect=noise={threshold}:d={minimum}","-f","null","-"])
 starts=[float(x) for x in re.findall(r"silence_start: ([0-9.]+)",err)]
 ends=[float(x) for x in re.findall(r"silence_end: ([0-9.]+)",err)]
 total=duration(path);out=[];cur=0.0
 for i,s in enumerate(starts):
  e=ends[i] if i<len(ends) else total
  if s-cur>.06:out.append([cur,s])
  cur=max(cur,e)
 if total-cur>.06:out.append([cur,total])
 return out,total

def whisper(path):
 try:
  from faster_whisper import WhisperModel
  model=WhisperModel("base",compute_type="int8")
  segs,_=model.transcribe(str(path),word_timestamps=True)
  return [{"word":w.word.strip(),"start":round(w.start,3),"end":round(w.end,3)} for s in segs for w in (s.words or [])]
 except Exception:pass
 try:
  import whisper as ow
  result=ow.load_model("base").transcribe(str(path),word_timestamps=True)
  return [{"word":w["word"].strip(),"start":round(w["start"],3),"end":round(w["end"],3)} for s in result["segments"] for w in s.get("words",[])]
 except Exception:return None

def align(text,segs):
 phrases=[x.strip() for x in re.findall(r"[^,.;:!?]+[,.;:!?]*",text.replace("\n"," ")) if x.strip()]
 if not phrases or not segs:return [],[],{"warning":"No phrases or speech segments found"}
 import functools
 weights=[sum(syllables(w) for w in p.split()) for p in phrases]
 total_w=sum(weights);total_d=sum(b-a for a,b in segs);rate=total_w/max(total_d,.01);INF=1e12
 @functools.lru_cache(None)
 def dp(i,j):
  if i==len(phrases) and j==len(segs):return 0.0,()
  if i>=len(phrases) or j>=len(segs):return INF,()
  best=(INF,())
  for k in range(i+1,min(len(phrases),i+4)+1):
   for l in range(j+1,min(len(segs),j+3)+1):
    if k-i>1 and l-j>1:continue
    d=segs[l-1][1]-segs[j][0];expected=sum(weights[i:k])/rate
    cost=(d-expected)**2/max(d,.25)
    cost+=sum(.35 for p in phrases[i:k-1] if re.search(r"[.!?][\"']?$",p))
    sub,plan=dp(k,l)
    if cost+sub<best[0]:best=(cost+sub,((i,k,j,l),)+plan)
  return best
 cost,plan=dp(0,0);words=[];out=[]
 for i,k,j,l in plan:
  start,end=segs[j][0],segs[l-1][1];ws=" ".join(phrases[i:k]).split();ww=[syllables(w) for w in ws];den=max(1,sum(ww));t=start
  out.append({"text":" ".join(phrases[i:k]),"start":round(start,3),"end":round(end,3),"approximate":True})
  for w,n in zip(ws,ww):
   nxt=t+(end-start)*n/den;words.append({"word":w,"start":round(t,3),"end":round(nxt,3),"approximate":True});t=nxt
 return words,out,{"alignment_cost":round(cost,3),"method":"silence + syllable-weighted phrase alignment (approximate)"}

def main():
 p=argparse.ArgumentParser();p.add_argument("audio");p.add_argument("script");p.add_argument("--out",default="audio-timing");a=p.parse_args()
 audio=Path(a.audio);script=Path(a.script)
 if not audio.is_file() or not script.is_file():raise SystemExit("Audio or dialogue script not found")
 text=script.read_text(encoding="utf-8");segs,total=segments(audio);words=whisper(audio)
 if words:
  phrases=[];cur=[]
  for w in words:
   cur.append(w)
   if re.search(r"[,.;:!?]$",w["word"]):
    phrases.append({"text":" ".join(x["word"] for x in cur),"start":cur[0]["start"],"end":cur[-1]["end"],"approximate":False});cur=[]
  if cur:phrases.append({"text":" ".join(x["word"] for x in cur),"start":cur[0]["start"],"end":cur[-1]["end"],"approximate":False})
  method="speech recognition word timestamps; compare transcript to supplied text"
 else:words,phrases,meta=align(text,segs);method=meta.get("method","approximate")
 out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
 (out/"words.json").write_text(json.dumps(words,ensure_ascii=False,indent=2),encoding="utf-8")
 (out/"phrases.json").write_text(json.dumps({"audio_duration":total,"speech_segments":segs,"phrases":phrases,"method":method},ensure_ascii=False,indent=2),encoding="utf-8")
 print(json.dumps({"audio_duration":total,"word_count":len(words),"phrase_count":len(phrases),"method":method,"output":str(out.resolve())},ensure_ascii=False,indent=2))
 print("REVIEW TIMESTAMPS AGAINST THE ORIGINAL AUDIO BEFORE LIP-SYNC.")
if __name__=="__main__":main()
