"""Create a reusable low-poly medium-detail humanoid starter asset in Blender.
Run: blender -b --python build_lowpoly_character.py -- --name Character_A --out //character_a.blend
This is a base asset. Refine its design, topology, rig, and materials against the supplied references.
"""
import bpy, argparse, sys
def getargs():
 av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
 p=argparse.ArgumentParser();p.add_argument("--name",default="SK3D_Character");p.add_argument("--out",default="//character.blend");return p.parse_args(av)
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;m.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value=(*c,1);m.node_tree.nodes.get("Principled BSDF").inputs["Roughness"].default_value=.72;return m
def uv(n,loc,scale,m,seg=12,rings=8):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=seg,ring_count=rings,location=loc);o=bpy.context.object;o.name=n;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if m:o.data.materials.append(m)
 return o
def cube(n,loc,dim,m,bev=.025):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if m:o.data.materials.append(m)
 if bev:b=o.modifiers.new("Low-poly edge bevel","BEVEL");b.width=bev;b.segments=1;o.modifiers.new("Weighted normals","WEIGHTED_NORMAL")
 return o
def main():
 a=getargs();bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
 coll=bpy.data.collections.new(a.name);bpy.context.scene.collection.children.link(coll)
 skin=mat("Skin",(.55,.32,.22));hair=mat("Hair",(.045,.03,.025));shirt=mat("Top",(.12,.22,.28));pants=mat("Trousers",(.10,.12,.16));shoe=mat("Shoes",(.035,.035,.04));eye=mat("Eyes",(.9,.86,.78));iris=mat("Iris",(.07,.12,.15));mouthmat=mat("Mouth",(.12,.025,.03))
 parts=[]
 def add(o,b):parts.append((o,b));return o
 add(uv("Head",(0,0,1.68),(.34,.30,.39),skin,16,10),"head")
 add(uv("Hair_Cap",(0,.025,1.91),(.355,.31,.20),hair),"head")
 for i,x in enumerate([-.22,-.08,.08,.22]):
  bpy.ops.mesh.primitive_cone_add(vertices=6,radius1=.10,radius2=.015,depth=.25,location=(x,-.22,1.82));o=bpy.context.object;o.name="Hair_Clump_%02d"%i;o.data.materials.append(hair);add(o,"head")
 for x in [-.13,.13]:
  add(uv("Eye_White",(x,-.282,1.73),(.075,.035,.09),eye,10,6),"head");add(uv("Iris",(x,-.315,1.73),(.035,.02,.045),iris,8,5),"head")
 add(uv("Nose",(0,-.32,1.65),(.045,.055,.065),skin,8,5),"head")
 mouth=uv("SK3D_Mouth",(0,-.304,1.555),(.105,.025,.027),mouthmat)
 mouth.shape_key_add(name="Basis")
 for key,zs,xs in [("REST",.18,1),("MBP",.12,1),("FV",.32,.8),("A",2.2,1),("E",.8,1.25),("I",.55,1),("O",1.7,.72),("U",1.1,.62),("L_TH",1.25,.9)]:
  kb=mouth.shape_key_add(name=key)
  for v in kb.data:v.co.x*=xs;v.co.z*=zs
 add(mouth,"head")
 add(uv("Neck",(0,0,1.27),(.12,.12,.16),skin),"neck");add(cube("Torso",(0,0,1.02),(.55,.30,.58),shirt,.05),"spine");add(cube("Pelvis",(0,0,.68),(.43,.29,.24),pants),"pelvis")
 for side,x in [("L",-.38),("R",.38)]:
  add(uv("UpperArm_"+side,(x,0,1.08),(.14,.15,.28),shirt),"upper_arm."+side);add(uv("Forearm_"+side,(x*1.12,0,.78),(.12,.13,.25),shirt),"forearm."+side);add(uv("Hand_"+side,(x*1.12,-.015,.57),(.13,.10,.11),skin),"hand."+side)
  add(uv("Thigh_"+side,(x*.52,0,.43),(.16,.17,.27),pants),"thigh."+side);add(uv("Shin_"+side,(x*.52,0,.16),(.12,.14,.22),pants),"shin."+side);add(cube("Shoe_"+side,(x*.52,-.075,.045),(.25,.38,.12),shoe),"foot."+side)
 arm=bpy.data.armatures.new(a.name+"_Armature");rig=bpy.data.objects.new(a.name+"_Rig",arm);coll.objects.link(rig);bpy.context.view_layer.objects.active=rig;rig.select_set(True);bpy.ops.object.mode_set(mode="EDIT")
 bones={"root":((0,0,0),(0,0,.2),None),"pelvis":((0,0,.58),(0,0,.82),"root"),"spine":((0,0,.78),(0,0,1.25),"pelvis"),"neck":((0,0,1.22),(0,0,1.43),"spine"),"head":((0,0,1.40),(0,0,1.88),"neck")}
 for s,x in [("L",-.38),("R",.38)]:
  bones.update({"upper_arm."+s:((0,0,1.16),(x,0,.94),"spine"),"forearm."+s:((x,0,.94),(x*1.12,0,.66),"upper_arm."+s),"hand."+s:((x*1.12,0,.66),(x*1.12,0,.52),"forearm."+s),"thigh."+s:((0,0,.66),(x*.52,0,.39),"pelvis"),"shin."+s:((x*.52,0,.39),(x*.52,0,.12),"thigh."+s),"foot."+s:((x*.52,0,.12),(x*.52,-.18,.06),"shin."+s)})
 for n,(h,t,parent) in bones.items():
  b=arm.edit_bones.new(n);b.head=h;b.tail=t
  if parent:b.parent=arm.edit_bones[parent]
 bpy.ops.object.mode_set(mode="OBJECT");rig.show_in_front=True
 for o,bn in parts:
  for old in list(o.users_collection):old.objects.unlink(o)
  coll.objects.link(o);o.parent=rig;o.parent_type="BONE";o.parent_bone=bn
 bpy.context.scene.render.engine="BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys() else "BLENDER_EEVEE"
 bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(a.out));print("SKILL3D_CHARACTER_CREATED",a.name,bpy.path.abspath(a.out))
if __name__=="__main__":main()
