"""Generate a reusable low-poly medium-detail humanoid starter asset in Blender.

Run:
  blender -b --python build_lowpoly_character.py -- --name "Character_A" --out //assets/characters/character_a.blend

This is a procedural base asset, not a substitute for character-specific art direction.
Claude must refine silhouette, face, hair, clothing, materials, and rig to match supplied references.
"""
import bpy, math, argparse, sys
from mathutils import Vector

def args():
    av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p=argparse.ArgumentParser()
    p.add_argument("--name",default="SK3D_Character")
    p.add_argument("--out",default="//character.blend")
    return p.parse_args(av)

def mat(name,color,rough=.72):
    m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
    bs=m.node_tree.nodes.get("Principled BSDF"); bs.inputs["Base Color"].default_value=(*color,1); bs.inputs["Roughness"].default_value=rough
    return m

def uv(name,loc,scale,material,segments=12,rings=8):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=segments, ring_count=rings, location=loc)
    o=bpy.context.object; o.name=name; o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if material:o.data.materials.append(material)
    for f in o.data.polygons:f.use_smooth=False
    return o

def cube(name,loc,scale,material,bevel=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc); o=bpy.context.object; o.name=name; o.dimensions=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if material:o.data.materials.append(material)
    if bevel:
        mod=o.modifiers.new("Controlled low-poly bevel","BEVEL"); mod.width=bevel; mod.segments=1
        o.modifiers.new("Weighted corner normals","WEIGHTED_NORMAL")
    return o

def cone(name,loc,radius,depth,material,verts=8):
    bpy.ops.mesh.primitive_cone_add(vertices=verts,radius1=radius,radius2=0,depth=depth,location=loc)
    o=bpy.context.object;o.name=name
    if material:o.data.materials.append(material)
    return o

def main():
    a=args(); bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete(use_global=False)
    c=bpy.data.collections.new(a.name); bpy.context.scene.collection.children.link(c)
    skin=mat("Skin | warm neutral",(0.55,.32,.22)); hair=mat("Hair | dark",(0.055,.035,.03)); shirt=mat("Clothing | top",(.12,.22,.28)); pants=mat("Clothing | trousers",(.10,.12,.16)); shoes=mat("Shoes",(.035,.035,.04)); white=mat("Eyes",(.88,.86,.78)); iris=mat("Iris",(.08,.13,.16)); mouthmat=mat("Mouth",(.12,.025,.03))
    parts=[]
    def add(o,bone): parts.append((o,bone)); return o
    add(uv("Head",(0,0,1.68),(.34,.30,.39),skin,16,10),"head")
    add(uv("Hair_Cap",(0,.025,1.91),(.355,.31,.20),hair,12,6),"head")
    # Hair fringe blocks, deliberately grouped into readable clumps.
    for i,x in enumerate([-.22,-.08,.08,.22]):
        add(cone("Hair_Clump_%02d"%i,(x,-.245,1.82),.105,.25,hair,6),"head")
    for x in [-.13,.13]:
        add(uv("Eye_White",(x,-.282,1.73),(.075,.035,.09),white,10,6),"head")
        add(uv("Iris",(x,-.315,1.73),(.035,.02,.045),iris,8,5),"head")
    add(uv("Nose",(0,-.32,1.65),(.045,.055,.065),skin,8,5),"head")
    mouth=uv("SK3D_Mouth",(0,-.304,1.555),(.105,.025,.027),mouthmat,12,6)
    # Shape keys used by apply_visemes.py. Mouth object remains a separate facial control mesh.
    mouth.shape_key_add(name="Basis")
    for key,zs,xs in [("REST",.18,1.0),("MBP",.12,1.0),("FV",.32,.8),("A",2.2,1.0),("E",.8,1.25),("I",.55,1.0),("O",1.7,.72),("U",1.1,.62),("L_TH",1.25,.9)]:
        kb=mouth.shape_key_add(name=key)
        for v in kb.data:
            v.co.x*=xs; v.co.z*=zs
    add(mouth,"head")
    add(uv("Neck",(0,0,1.27),(.12,.12,.16),skin),"neck")
    add(cube("Torso",(0,0,1.02),(.55,.30,.58),shirt,.055),"spine")
    add(cube("Pelvis",(0,0,.68),(.43,.29,.24),pants,.035),"pelvis")
    for side,x in [("L",-.38),("R",.38)]:
        add(uv("UpperArm_"+side,(x,0,1.08),(.14,.15,.28),shirt),"upper_arm."+side)
        add(uv("Forearm_"+side,(x*1.12,-.005,.78),(.12,.13,.25),shirt),"forearm."+side)
        add(uv("Hand_"+side,(x*1.12,-.015,.57),(.13,.10,.11),skin),"hand."+side)
        add(uv("Thigh_"+side,(x*.52,0,.43),(.16,.17,.27),pants),"thigh."+side)
        add(uv("Shin_"+side,(x*.52,-.005,.16),(.12,.14,.22),pants),"shin."+side)
        add(cube("Shoe_"+side,(x*.52,-.075,.045),(.25,.38,.12),shoes,.025),"foot."+side)
    # Basic articulated armature; rigid bone-parented pieces make a usable block rig.
    arm=bpy.data.armatures.new(a.name+"_Rig"); rig=bpy.data.objects.new(a.name+"_Rig",arm); c.objects.link(rig)
    bpy.context.view_layer.objects.active=rig; rig.select_set(True); bpy.ops.object.mode_set(mode="EDIT")
    bones={"root":((0,0,0),(0,0,.2),None),"pelvis":((0,0,.58),(0,0,.82),"root"),"spine":((0,0,.78),(0,0,1.25),"pelvis"),"neck":((0,0,1.22),(0,0,1.43),"spine"),"head":((0,0,1.40),(0,0,1.88),"neck")}
    for side,x in [("L",-.38),("R",.38)]:
        bones["upper_arm."+side]=((0,0,1.16),(x,0,.94),"spine"); bones["forearm."+side]=((x,0,.94),(x*1.12,0,.66),"upper_arm."+side); bones["hand."+side]=((x*1.12,0,.66),(x*1.12,0,.52),"forearm."+side)
        bones["thigh."+side]=((0,0,.66),(x*.52,0,.39),"pelvis"); bones["shin."+side]=((x*.52,0,.39),(x*.52,0,.12),"thigh."+side); bones["foot."+side]=((x*.52,0,.12),(x*.52,-.18,.06),"shin."+side)
    for n,(h,t,parent) in bones.items():
        b=arm.edit_bones.new(n); b.head=h; b.tail=t
        if parent:b.parent=arm.edit_bones[parent]
    bpy.ops.object.mode_set(mode="OBJECT"); rig.show_in_front=True
    for o,bn in parts:
        o.parent=rig; o.parent_type="BONE"; o.parent_bone=bn
    # Move objects into this asset collection.
    for o in [rig]+[p[0] for p in parts]:
        for col in list(o.users_collection): col.objects.unlink(o)
        c.objects.link(o)
    rig.select_set(True); bpy.context.view_layer.objects.active=rig
    bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(a.out))
    print("SKILL3D_CHARACTER_CREATED",a.name,bpy.path.abspath(a.out))
if __name__=="__main__": main()
