#!/usr/bin/env python3
"""Create a contact sheet from rendered stills. Requires Pillow."""
import argparse, math
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("input_dir")
    ap.add_argument("output")
    ap.add_argument("--columns",type=int,default=4)
    ap.add_argument("--width",type=int,default=360)
    args=ap.parse_args()
    files=sorted(p for p in Path(args.input_dir).iterdir() if p.suffix.lower() in {".png",".jpg",".jpeg",".webp"})
    if not files:
        raise SystemExit("No still images found.")
    if args.columns<1 or args.width<1:
        raise SystemExit("columns and width must be positive.")
    thumbs=[]
    for p in files:
        im=Image.open(p).convert("RGB")
        h=max(1,round(im.height*args.width/im.width))
        im=im.resize((args.width,h),Image.Resampling.LANCZOS)
        canvas=Image.new("RGB",(args.width,h+28),"white")
        canvas.paste(im,(0,0))
        ImageDraw.Draw(canvas).text((8,h+6),p.name,fill="black")
        thumbs.append(canvas)
    cell_h=max(im.height for im in thumbs)
    rows=math.ceil(len(thumbs)/args.columns)
    sheet=Image.new("RGB",(args.columns*args.width,rows*cell_h),(36,36,36))
    for i,im in enumerate(thumbs):
        x=(i%args.columns)*args.width
        y=(i//args.columns)*cell_h
        sheet.paste(im,(x,y))
    out=Path(args.output)
    out.parent.mkdir(parents=True,exist_ok=True)
    sheet.save(out)
    print(f"{out} ({len(files)} images)")

if __name__=="__main__":
    main()
