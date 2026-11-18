"""Create a modern post-disaster street blockout. Run Blender with --python this_file -- --out //ruins.blend.
Starter layout only: adapt damage, props, architecture and composition to the user's script.
"""
import bpy,random,argparse,sys
from mathutils import Vector
def args():
 av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
 p=argparse.ArgumentParser();p.add_argument("--out",default="//modern_ruins.blend");p.add_argument("--seed",type=int,default=19);return p.parse_args(av)
def mat(n,c):
 m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;m.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value=(*c,1);return m
def box(n,l,d,m,bev=0):
 bpy.ops.mesh.primitive_cube_add(size=1,location=l);o=bpy.context.object;o.name=n;o.dimensions=d;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if m:o.data.materials.append(m)
 if bev:b=o.modifiers.new("Edge wear","BEVEL");b.width=bev;b.segments=1;o.modifiers.new("Weighted normals","WEIGHTED_NORMAL")
 return o
def main():
 a=args();random.seed(a.seed);bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
 asphalt=mat("Asphalt",(.07,.08,.085));concrete=mat("Weathered concrete",(.34,.34,.31));glass=mat("Dark glass",(.045,.085,.11));metal=mat("Painted metal",(.12,.15,.16));dirt=mat("Rust and dirt",(.19,.105,.065));green=mat("Overgrowth",(.12,.20,.11))
 box("Road",(0,0,-.12),(18,30,.2),asphalt);box("Sidewalk_L",(-5.4,0,-.01),(2.6,30,.28),concrete);box("Sidewalk_R",(5.4,0,-.01),(2.6,30,.28),concrete)
 for side in [-1,1]:
  for j in range(3):
   x=side*8.2;y=-8+j*9;box("Modern_Building",(x,y,3),(5,7.5,6),concrete,.06)
   for floor in range(3):
    for col in range(2):box("Window",(x+side*(-1.45+col*2),y-2.2,1.25+floor*1.8),(.85,.09,1.15),glass,.02)
   box("Roof_Parapet",(x,y,6.08),(5.15,7.65,.18),dirt)
 box("Abandoned_Car_Body",(-2.2,-2,.72),(2,4,.85),metal,.14);box("Car_Cabin",(-2.2,-2.05,1.35),(1.65,2.1,.65),glass,.1)
 for x in [-3.25,-1.15]:
  for y in [-3.25,-.75]:
   bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=.38,depth=.22,location=(x,y,.38),rotation=(0,1.5708,0));bpy.context.object.name="Car_Wheel";bpy.context.object.data.materials.append(dirt)
 for x in [-6.2,6.2]:
  box("Streetlight_Pole",(x,2.5,2.4),(.12,.12,4.8),metal);box("Streetlight_Arm",(x-.35,2.5,4.65),(.8,.12,.12),metal);box("Streetlight_Lamp",(x-.72,2.5,4.58),(.35,.28,.18),dirt)
 for i in range(22):
  bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=random.uniform(.12,.38),location=(random.uniform(-4.5,4.5),random.uniform(-13,13),.12));o=bpy.context.object;o.name="Road_Rubble";o.scale=(1.3,.8,.5);o.data.materials.append(random.choice([concrete,dirt,green]))
 bpy.ops.object.light_add(type="AREA",location=(1,-5,12));bpy.context.object.data.energy=1800;bpy.context.object.data.shape="DISK";bpy.context.object.data.size=10
 bpy.ops.object.camera_add(location=(10,-18,8));cam=bpy.context.object;cam.rotation_euler=(Vector((0,0,2))-cam.location).to_track_quat("-Z","Y").to_euler();s=bpy.context.scene;s.camera=cam;s.render.resolution_x=1280;s.render.resolution_y=720;s.render.resolution_percentage=50
 s.render.engine="BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys() else "BLENDER_EEVEE"
 bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(a.out));print("SKILL3D_ENV_CREATED",bpy.path.abspath(a.out))
if __name__=="__main__":main()
