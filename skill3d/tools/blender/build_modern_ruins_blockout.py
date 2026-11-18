"""Create a modern post-disaster street blockout in Blender.

Run:
  blender -b --python build_modern_ruins_blockout.py -- --out //modern_ruins.blend

Creates a reusable low-poly 3D blockout (road, sidewalks, contemporary buildings,
abandoned car mass, streetlights, rubble). It is a starter layout, not a finished set.
Claude must adapt architecture, damage, props, and layout to the supplied script.
"""
import bpy, argparse, sys, random
from mathutils import Vector

def getargs():
    av=sys.argv[sys.argv.index("--")+1:] if "--" in sys.argv else []
    p=argparse.ArgumentParser();p.add_argument("--out",default="//modern_ruins.blend");p.add_argument("--seed",type=int,default=19)
    return p.parse_args(av)
def material(n,c):
    m=bpy.data.materials.new(n);m.diffuse_color=(*c,1);m.use_nodes=True;m.node_tree.nodes.get("Principled BSDF").inputs["Base Color"].default_value=(*c,1);return m
def box(n,loc,dim,ma,bev=0):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.name=n;o.dimensions=dim;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if ma:o.data.materials.append(ma)
    if bev:
        b=o.modifiers.new("Small edge bevel","BEVEL");b.width=bev;b.segments=1;o.modifiers.new("Weighted normals","WEIGHTED_NORMAL")
    return o
def main():
    a=getargs();random.seed(a.seed);bpy.ops.object.select_all(action="SELECT");bpy.ops.object.delete(use_global=False)
    road=material("Asphalt",(.075,.085,.09));concrete=material("Weathered concrete",(.34,.34,.31));glass=material("Dark window glass",(.055,.10,.13));metal=material("Painted metal",(.12,.15,.16));rust=material("Rust/dirt",(.19,.105,.065));leaf=material("Overgrowth",(.12,.20,.11))
    box("Road",(0,0,-.12),(18,30,.2),road)
    box("Sidewalk_Left",(-5.4,0,-.015),(2.6,30,.28),concrete);box("Sidewalk_Right",(5.4,0,-.015),(2.6,30,.28),concrete)
    # Modern low-rise blocks with repeated window bays.
    for side in [-1,1]:
        for j in range(3):
            x=side*8.2;y=-8+j*9
            box("Modern_Building_%s_%s"%(side,j),(x,y,3.0),(5.0,7.5,6.0),concrete,.08)
            for floor in range(3):
                for col in range(2):
                    wx=x+side*(-1.45+col*2.0);wy=y-2.2+floor*0.0
                    box("Window",(wx,wy,1.25+floor*1.8),(.85,.09,1.15),glass,.025)
            box("Roof_Parapet",(x,y,6.08),(5.15,7.65,.18),rust,.02)
    # Car body and wheels: intentionally generic abandoned-vehicle blockout.
    box("Abandoned_Car_Body",(-2.2,-2.0,.72),(2.0,4.0,.85),metal,.16)
    box("Car_Cabin",(-2.2,-2.05,1.35),(1.65,2.1,.65),glass,.12)
    for x in [-3.25,-1.15]:
        for y in [-3.25,-.75]:
            bpy.ops.mesh.primitive_cylinder_add(vertices=10,radius=.38,depth=.22,location=(x,y,.38),rotation=(0,1.5708,0))
            bpy.context.object.name="Car_Wheel";bpy.context.object.data.materials.append(rust)
    # Streetlights and a few debris chunks.
    for x in [-6.2,6.2]:
        box("Streetlight_Pole",(x,2.5,2.4),(.12,.12,4.8),metal)
        box("Streetlight_Arm",(x-.35,2.5,4.65),(.8,.12,.12),metal)
        box("Streetlight_Lamp",(x-.72,2.5,4.58),(.35,.28,.18),rust)
    for i in range(22):
        x=random.uniform(-4.5,4.5);y=random.uniform(-13,13)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1,radius=random.uniform(.12,.38),location=(x,y,.12))
        o=bpy.context.object;o.name="Road_Rubble";o.scale=(1.3,.8,.5);o.data.materials.append(random.choice([concrete,rust,leaf]))
    # Lighting and camera for a useful first preview.
    bpy.ops.object.light_add(type="AREA",location=(1,-5,12));bpy.context.object.name="Overcast_Key";bpy.context.object.data.energy=1800;bpy.context.object.data.shape="DISK";bpy.context.object.data.size=10
    bpy.ops.object.camera_add(location=(10,-18,8));cam=bpy.context.object;cam.name="Blockout_Camera";cam.rotation_euler=(Vector((0,0,2))-cam.location).to_track_quat("-Z","Y").to_euler()
    scene=bpy.context.scene;scene.camera=cam;scene.render.engine="BLENDER_EEVEE_NEXT" if "BLENDER_EEVEE_NEXT" in bpy.types.RenderSettings.bl_rna.properties["engine"].enum_items.keys() else "BLENDER_EEVEE"
    scene.render.resolution_x=1280;scene.render.resolution_y=720;scene.render.resolution_percentage=50
    bpy.ops.wm.save_as_mainfile(filepath=bpy.path.abspath(a.out));print("SKILL3D_ENV_CREATED",bpy.path.abspath(a.out))
if __name__=="__main__":main()
