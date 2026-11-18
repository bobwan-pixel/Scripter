#!/usr/bin/env python3
"""End-to-end Blender/FFmpeg smoke test for Skill3D's starter pipeline.

Run in CI or locally:
  python skill3d/tests/blender_smoke.py
Requires Blender and FFmpeg/FFprobe on PATH. Renders a tiny 1-second test clip.
"""
import json,shutil,subprocess,tempfile
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def run(cmd, label):
    print("\n==",label,"==",flush=True)
    r=subprocess.run(cmd,text=True)
    if r.returncode: raise SystemExit(f"{label} failed with exit code {r.returncode}")
def main():
    blender=shutil.which("blender")
    if not blender: raise SystemExit("Blender is required for this integration test")
    for tool in ("ffmpeg","ffprobe"):
        if not shutil.which(tool): raise SystemExit(tool+" is required")
    with tempfile.TemporaryDirectory(prefix="skill3d-smoke-") as raw:
        d=Path(raw); character=d/"character.blend"; env=d/"environment.blend"
        run([blender,"-b","--python",str(ROOT/"tools/blender/build_lowpoly_character.py"),"--","--name","QA_Character","--out",str(character)],"generate low-poly character")
        inspect="import bpy; rig=next((o for o in bpy.data.objects if o.type=='ARMATURE'),None); mouth=bpy.data.objects.get('SK3D_Mouth'); assert rig and len(rig.data.bones)>=15, 'armature/bones missing'; assert mouth and mouth.data.shape_keys and len(mouth.data.shape_keys.key_blocks)>=9, 'mouth shape keys missing'; print('CHARACTER_OK',len(rig.data.bones),len(mouth.data.shape_keys.key_blocks))"
        run([blender,"-b",str(character),"--python-expr",inspect],"inspect character rig and mouth")
        cues=d/"cues.json"; cues.write_text(json.dumps({"fps":24,"object":"SK3D_Mouth","events":[{"start":0.0,"end":0.25,"viseme":"MBP"},{"start":0.25,"end":0.5,"viseme":"A"},{"start":0.5,"end":0.75,"viseme":"REST"}]}),encoding="utf-8")
        run([blender,"-b",str(character),"--python",str(ROOT/"tools/blender/apply_visemes.py"),"--","--json",str(cues)],"apply lip-sync viseme keys")
        animcheck="import bpy; k=bpy.data.objects['SK3D_Mouth'].data.shape_keys; assert k.animation_data and k.animation_data.action, 'viseme action missing'; print('VISEME_ACTION_OK')"
        run([blender,"-b",str(character),"--python-expr",animcheck],"inspect lip-sync keyframes")
        run([blender,"-b","--python",str(ROOT/"tools/blender/build_modern_ruins_blockout.py"),"--","--out",str(env),"--seed","19"],"generate modern ruined-street blockout")
        setup="import bpy; s=bpy.context.scene; s.render.resolution_x=320; s.render.resolution_y=180; s.render.resolution_percentage=100; s.render.fps=24; s.frame_start=1; s.frame_end=24; s.eevee.taa_render_samples=8 if hasattr(s,'eevee') else 8; print('ENV_CAMERA',bool(s.camera))"
        run([blender,"-b",str(env),"--python-expr",setup],"configure tiny render")
        prefix=str(d/"frames"/"frame_")
        run(["python",str(ROOT/"tools/render_range.py"),str(env),"--blender",blender,"--start","1","--end","24","--chunk","12","--output",prefix],"render frames in chunks")
        wav=d/"dialogue-test.wav"
        run(["ffmpeg","-y","-f","lavfi","-i","sine=frequency=440:duration=1","-c:a","pcm_s16le",str(wav)],"create synthetic QA audio")
        video=d/"smoke.mp4"
        run(["python",str(ROOT/"tools/encode_mp4.py"),"--frames",prefix+"%04d.png","--audio",str(wav),"--output",str(video),"--fps","24","--frame-count","24"],"encode MP4 with audio")
        run(["python",str(ROOT/"tools/validate_mp4.py"),str(video),"--min-seconds","0.8","--max-seconds","1.2"],"validate MP4 streams and duration")
        run(["python",str(ROOT/"tools/video_qa.py"),str(video)],"run black/freeze QA")
        print("SKILL3D_BLENDER_FFMPEG_SMOKE_TEST_PASS",video.stat().st_size,"bytes")
if __name__=="__main__": main()
