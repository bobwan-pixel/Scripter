"""Apply a time-coded viseme JSON track to Blender shape keys (approximate automation).
JSON: {"fps":24,"object":"SK3D_Mouth","events":[{"start":0.1,"end":0.18,"viseme":"MBP"}]}
Supported keys: REST, MBP, FV, A, E, I, O, U, L_TH.
Run: blender -b project.blend --python apply_visemes.py -- --json visemes.json
"""
import bpy,json,argparse,sys
def main():
 av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
 p=argparse.ArgumentParser();p.add_argument("--json",required=True);a=p.parse_args(av)
 with open(a.json,encoding="utf-8") as f:data=json.load(f)
 fps=float(data.get("fps",bpy.context.scene.render.fps));obj=bpy.data.objects.get(data.get("object","SK3D_Mouth"))
 if not obj or not obj.data.shape_keys:raise SystemExit("Target object or shape keys not found")
 keys=obj.data.shape_keys.key_blocks;valid={"REST","MBP","TEETH","FV","A","E","I","O","U","L_TH"};missing=valid-set(keys.keys())
 if missing:raise SystemExit("Missing shape keys: "+", ".join(sorted(missing)))
 events=sorted(data.get("events",[]),key=lambda e:float(e["start"]))
 for ev in events:
  st=max(1,round(float(ev["start"])*fps));en=max(st+1,round(float(ev["end"])*fps));v=str(ev["viseme"]).upper()
  if v not in valid:raise SystemExit("Unsupported viseme "+v)
  for k in valid:
   block=keys[k];block.value=0;block.keyframe_insert("value",frame=max(1,st-1))
  keys[v].value=1;keys[v].keyframe_insert("value",frame=st);keys[v].keyframe_insert("value",frame=en);keys[v].value=0;keys[v].keyframe_insert("value",frame=en+2)
 bpy.context.scene.frame_end=max(bpy.context.scene.frame_end,round(max([float(e["end"]) for e in events],default=0)*fps)+3)
 print("SKILL3D_VISEMES_APPLIED",len(events),"events at",fps,"fps")
if __name__=="__main__":main()
