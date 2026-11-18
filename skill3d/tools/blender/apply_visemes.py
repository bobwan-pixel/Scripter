"""Apply time-coded viseme events to Blender shape keys.

Input JSON:
{
  "fps": 24,
  "object": "SK3D_Mouth",
  "events": [
    {"start": 0.10, "end": 0.18, "viseme": "MBP"},
    {"start": 0.18, "end": 0.30, "viseme": "A"}
  ]
}

Times are seconds. The target mesh must have shape keys named REST, MBP, FV, A, E, I, O, U, L_TH.
This applies an approximate track; it does not perform speech recognition or prove lip-sync.
Run: blender -b project.blend --python apply_visemes.py -- --json visemes.json
"""
import bpy, json, argparse, sys

def main():
    av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument("--json",required=True);a=p.parse_args(av)
    data=json.load(open(a.json,encoding="utf-8"));fps=float(data.get("fps",bpy.context.scene.render.fps))
    obj=bpy.data.objects.get(data.get("object","SK3D_Mouth"))
    if not obj or not obj.data.shape_keys: raise SystemExit("Target object or shape keys not found")
    keys=obj.data.shape_keys.key_blocks
    required={"REST","MBP","FV","A","E","I","O","U","L_TH"}
    missing=required-set(keys.keys())
    if missing: raise SystemExit("Missing shape keys: "+", ".join(sorted(missing)))
    events=sorted(data.get("events",[]),key=lambda e:float(e["start"]))
    scene=bpy.context.scene
    for key in keys:
        if key.name!="Basis": key.value=0.0
    for ev in events:
        start=max(0,round(float(ev["start"])*fps));end=max(start+1,round(float(ev["end"])*fps))
        vis=str(ev["viseme"]).upper()
        if vis not in required: raise SystemExit("Unsupported viseme: "+vis)
        # Short neutral lead-in and blend-out avoid hard pops at event boundaries.
        for name in required:
            block=keys[name]
            block.value=0.0;block.keyframe_insert("value",frame=max(1,start-1))
        block=keys[vis];block.value=1.0;block.keyframe_insert("value",frame=start)
        block.value=1.0;block.keyframe_insert("value",frame=end)
        block.value=0.0;block.keyframe_insert("value",frame=end+2)
    scene.frame_end=max(scene.frame_end,round(max([float(e["end"]) for e in events],default=0)*fps)+3)
    print("SKILL3D_VISEMES_APPLIED",len(events),"events",fps,"fps")
if __name__=="__main__":main()
