import * as THREE from "three";
import { OrbitControls } from "three/addons/controls/OrbitControls.js";
import { GLTFLoader } from "three/addons/loaders/GLTFLoader.js";

const $ = id => document.getElementById(id);
const stage = $("stage");
const scene = new THREE.Scene();
scene.background = new THREE.Color("#a9c7df");
scene.fog = new THREE.Fog("#a9c7df", 28, 90);
const camera = new THREE.PerspectiveCamera(42, 1, 0.1, 250);
camera.position.set(8, 6, 11);
const renderer = new THREE.WebGLRenderer({antialias:true, preserveDrawingBuffer:true});
renderer.setPixelRatio(Math.min(devicePixelRatio, 1.75));
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
renderer.outputColorSpace = THREE.SRGBColorSpace;
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.15;
stage.appendChild(renderer.domElement);
const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0,1.3,0); controls.enableDamping = true;
scene.add(new THREE.HemisphereLight(0xe7f3ff,0x6e5b4d,2.0));
const sun = new THREE.DirectionalLight(0xffe2c1,3.1);
sun.position.set(-7,12,8); sun.castShadow=true; sun.shadow.mapSize.set(2048,2048);
sun.shadow.camera.left=-22;sun.shadow.camera.right=22;sun.shadow.camera.top=22;sun.shadow.camera.bottom=-22;scene.add(sun);
const fill = new THREE.DirectionalLight(0x9ecbff,1.0);fill.position.set(7,6,-8);scene.add(fill);
const mat=(color,roughness=.82)=>new THREE.MeshStandardMaterial({color,roughness});
const mats={ground:mat("#8c9b79"),wall:mat("#e6d9c5"),roof:mat("#875d50"),trunk:mat("#71503b"),leaf:mat("#63865d"),glass:mat("#83b6c8",.28)};
const world=new THREE.Group();scene.add(world);
const ground=new THREE.Mesh(new THREE.PlaneGeometry(200,200),mats.ground);ground.rotation.x=-Math.PI/2;ground.receiveShadow=true;world.add(ground);
const grid=new THREE.GridHelper(80,80,"#72818b","#9ca8ae");grid.position.y=.012;world.add(grid);
let characters=[],active=null,props=[],keyframes=[],timeMs=0,playing=false,lastTick=0,environment="studio";
const loader=new GLTFLoader();
function addMesh(parent,geometry,material,pos=[0,0,0],scale=[1,1,1]){const m=new THREE.Mesh(geometry,material);m.position.set(...pos);m.scale.set(...scale);m.castShadow=true;m.receiveShadow=true;parent.add(m);return m;}
function capsule(parent,r,len,material,pos){return addMesh(parent,new THREE.CapsuleGeometry(r,len,5,10),material,pos);}
function createCharacter(data={}){
 const colors={skin:data.skin||"#e7b995",hair:data.hair||"#302b2b",shirt:data.shirt||"#667f91",pants:data.pants||"#394c63"};
 const root=new THREE.Group();root.position.set(data.x||0,0,data.z||0);root.rotation.y=data.rotation||0;root.scale.setScalar(data.scale||1);world.add(root);
 const torso=new THREE.Group();torso.position.y=1.38;root.add(torso);
 const bodyMat=mat(colors.shirt),skinMat=mat(colors.skin),hairMat=mat(colors.hair),pantsMat=mat(colors.pants),shoeMat=mat("#343a40");
 addMesh(torso,new THREE.CapsuleGeometry(.43,.66,6,16),bodyMat,[0,0,0],[1,1,0.72]);
 const neck=capsule(torso,.13,.12,skinMat,[0,.56,0]);
 const head=new THREE.Group();head.position.set(0,.94,0);torso.add(head);
 addMesh(head,new THREE.SphereGeometry(.53,32,24),skinMat,[0,0,0],[.92,1.05,.82]);
 addMesh(head,new THREE.SphereGeometry(.54,24,16),hairMat,[0,.32,-.05],[.95,.58,.87]);
 addMesh(head,new THREE.SphereGeometry(.22,16,12),hairMat,[-.31,.2,.18],[1,.8,.7]);
 const eyeMat=mat("#22242a",.3),white=mat("#fffaf0",.3);
 for(const x of [-.19,.19]){addMesh(head,new THREE.SphereGeometry(.075,12,10),white,[x,.04,.43],[1,1,.45]);addMesh(head,new THREE.SphereGeometry(.043,12,10),eyeMat,[x,.035,.466],[1,1,.4]);}
 const mouth=addMesh(head,new THREE.TorusGeometry(.09,.018,6,18,Math.PI),mat("#743e3a"),[0,-.19,.435]);mouth.rotation.z=Math.PI;
 const armPivots=[];
 for(const side of [-1,1]){
  const shoulder=new THREE.Group();shoulder.position.set(side*.48,.42,0);torso.add(shoulder);
  capsule(shoulder,.13,.55,bodyMat,[0,-.36,0]);
  const elbow=new THREE.Group();elbow.position.set(0,-.69,0);shoulder.add(elbow);
  capsule(elbow,.105,.48,skinMat,[0,-.29,0]);
  addMesh(elbow,new THREE.SphereGeometry(.15,16,12),skinMat,[0,-.62,.02],[.95,.8,.85]);
  armPivots.push({shoulder,elbow});
  const leg=new THREE.Group();leg.position.set(side*.23,-.3,0);root.add(leg);
  capsule(leg,.17,.64,pantsMat,[0,-.43,0]);
  const foot=addMesh(leg,new THREE.BoxGeometry(.3,.17,.53),shoeMat,[0,-.84,.13]);foot.rotation.x=-.04;
 }
 root.userData={name:data.name||"Character "+(characters.length+1),colors,torso,head,armPivots};
 const item={root,data:{...colors,name:root.userData.name},armPivots};characters.push(item);selectCharacter(item);return item;
}
function selectCharacter(item){active=item;const d=item.data; $("charName").value=d.name;$("skin").value=d.skin;$("hair").value=d.hair;$("shirt").value=d.shirt;$("pants").value=d.pants;syncTransform();}
function syncTransform(){if(!active)return;const o=active.root;$("posX").value=o.position.x;$("posZ").value=o.position.z;$("rotY").value=THREE.MathUtils.radToDeg(o.rotation.y);$("scale").value=o.scale.x;updateLabels();}
function updateLabels(){$("xVal").textContent=Number($("posX").value).toFixed(1);$("zVal").textContent=Number($("posZ").value).toFixed(1);$("rotVal").textContent=Math.round($("rotY").value)+"°";$("scaleVal").textContent=Number($("scale").value).toFixed(2);}
function updateCharacterColors(){if(!active)return;const d=active.data;d.name=$("charName").value;d.skin=$("skin").value;d.hair=$("hair").value;d.shirt=$("shirt").value;d.pants=$("pants").value;const root=active.root;root.traverse(o=>{if(!o.isMesh)return;const c=o.material?.color;if(!c)return;const nm=o.material; if(nm===undefined)return;});rebuildActive();}
function rebuildActive(){if(!active)return;const old=active;const idx=characters.indexOf(old);const transform={x:old.root.position.x,z:old.root.position.z,rotation:old.root.rotation.y,scale:old.root.scale.x};world.remove(old.root);characters.splice(idx,1);const fresh=createCharacter({...old.data,...transform});characters.splice(characters.indexOf(fresh),1);characters.splice(idx,0,fresh);active=fresh;selectCharacter(fresh);}
function clearEnvironment(){for(const o of [...world.children])if(o!==ground&&o!==grid)world.remove(o);props=[];characters.forEach(c=>world.remove(c.root));characters=[];active=null;world.add(ground,grid);}
function building(x,z,w,h,d){const g=new THREE.Group();g.position.set(x,0,z);world.add(g);addMesh(g,new THREE.BoxGeometry(w,h,d),mats.wall,[0,h/2,0]);const roof=addMesh(g,new THREE.ConeGeometry(Math.max(w,d)*.78,Math.max(1.2,h*.35),4),mats.roof,[0,h+.55,0]);roof.rotation.y=Math.PI/4;addMesh(g,new THREE.BoxGeometry(.85,1.55,.09),mat("#594a40"),[0,.78,d/2+.05]);return g;}
function tree(x,z){const g=new THREE.Group();g.position.set(x,0,z);world.add(g);addMesh(g,new THREE.CylinderGeometry(.13,.2,1.6,8),mats.trunk,[0,.8,0]);addMesh(g,new THREE.SphereGeometry(1,16,12),mats.leaf,[0,2.2,0],[.9,1.15,.9]);props.push({type:"tree",x,z});}
function setEnvironment(kind){
 environment=kind;clearEnvironment();
 if(kind==="village"){for(let i=0;i<8;i++)building((i%4-1.5)*7,Math.floor(i/4)*-8-5,3.6,2.8+(i%3)*.5,3.5);for(let i=0;i<14;i++)tree((i%7-3)*4,Math.floor(i/7)*8-3);}
 if(kind==="city"){for(let i=0;i<10;i++){const h=5+(i%4)*3;building((i%5-2)*6,Math.floor(i/5)*-8-7,4,h,4);}}
 if(kind==="room"){addMesh(world,new THREE.BoxGeometry(12,.2,12),mat("#9e8d7c"),[0,.1,0]);for(const x of [-6,6])addMesh(world,new THREE.BoxGeometry(.2,5,12),mat("#e3d8c9"),[x,2.5,0]);addMesh(world,new THREE.BoxGeometry(12,5,.2),mat("#e3d8c9"),[0,2.5,-6]);}
 $("status").textContent="Environment: "+kind;
}
function addBox(){const mesh=addMesh(world,new THREE.BoxGeometry(1.5,1.5,1.5),mat("#b77d57"),[Math.random()*5-2.5,.75,Math.random()*5-2.5]);props.push({type:"box",x:mesh.position.x,z:mesh.position.z});}
function addTree(){tree(Math.random()*12-6,Math.random()*12-6);}
function applyTransform(){if(!active)return;active.root.position.x=Number($("posX").value);active.root.position.z=Number($("posZ").value);active.root.rotation.y=THREE.MathUtils.degToRad(Number($("rotY").value));active.root.scale.setScalar(Number($("scale").value));updateLabels();}
function snapshot(){if(!active)return null;return {time:timeMs,x:active.root.position.x,z:active.root.position.z,rotation:active.root.rotation.y,scale:active.root.scale.x};}
function sample(t){if(!keyframes.length||!active)return;const frames=[...keyframes].sort((a,b)=>a.time-b.time);let a=frames[0],b=frames[frames.length-1];for(let i=0;i<frames.length-1;i++){if(t>=frames[i].time&&t<=frames[i+1].time){a=frames[i];b=frames[i+1];break;}}if(t<=a.time)b=a;if(t>=b.time)a=b;const p=a===b?0:THREE.MathUtils.clamp((t-a.time)/(b.time-a.time),0,1);const e=p*p*(3-2*p);active.root.position.x=THREE.MathUtils.lerp(a.x,b.x,e);active.root.position.z=THREE.MathUtils.lerp(a.z,b.z,e);active.root.rotation.y=THREE.MathUtils.lerp(a.rotation,b.rotation,e);active.root.scale.setScalar(THREE.MathUtils.lerp(a.scale,b.scale,e));syncTransform();}
function fmt(ms){const s=ms/1000,m=Math.floor(s/60),sec=s%60;return String(m).padStart(2,"0")+":"+sec.toFixed(2).padStart(5,"0");}
function renderKeys(){const host=$("keys");host.replaceChildren();if(!keyframes.length){host.textContent="Belum ada keyframe.";return;}keyframes.sort((a,b)=>a.time-b.time).forEach((k,i)=>{const b=document.createElement("button");b.textContent=fmt(k.time);b.className=Math.abs(k.time-timeMs)<80?"active":"";b.onclick=()=>{timeMs=k.time;$("scrubber").value=timeMs;sample(timeMs);updateTimeUI();};host.append(b);});}
function updateTimeUI(){$("timeLabel").textContent=fmt(timeMs);$("frameReadout").textContent=fmt(timeMs)+" / 10:00.00";}
function exportProject(){const data={version:4,duration:600000,fps:30,environment,sky:$("sky").value,characters:characters.map(c=>({name:c.data.name,...c.data,x:c.root.position.x,z:c.root.position.z,rotation:c.root.rotation.y,scale:c.root.scale.x})),props,keyframes};const blob=new Blob([JSON.stringify(data,null,2)],{type:"application/json"});download(blob,"skil-cc-v4-project.json");$("projectStatus").textContent="Project JSON berhasil diexport.";}
function download(blob,name){const url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=name;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);}
function loadProject(data){if(data.version!==4)throw new Error("Versi project tidak didukung.");setEnvironment(data.environment||"studio");$("sky").value=data.sky||"#a9c7df";scene.background.set($("sky").value);(data.characters||[]).forEach(c=>createCharacter(c));(data.props||[]).forEach(p=>{if(p.type==="tree")tree(p.x,p.z);else addBox();});keyframes=Array.isArray(data.keyframes)?data.keyframes:[];timeMs=0;$("scrubber").value=0;renderKeys();updateTimeUI();$("projectStatus").textContent="Project berhasil dimuat.";}
$("addCharacter").onclick=()=>createCharacter({name:"Character "+(characters.length+1),skin:$("skin").value,hair:$("hair").value,shirt:$("shirt").value,pants:$("pants").value});
$("resetPose").onclick=()=>{if(active){active.root.position.set(0,0,0);active.root.rotation.set(0,0,0);active.root.scale.setScalar(1);syncTransform();}};
["posX","posZ","rotY","scale"].forEach(id=>$(id).addEventListener("input",applyTransform));
["charName","skin","hair","shirt","pants"].forEach(id=>$(id).addEventListener("change",()=>{if(!active)return;const d=active.data;d.name=$("charName").value;d.skin=$("skin").value;d.hair=$("hair").value;d.shirt=$("shirt").value;d.pants=$("pants").value;rebuildActive();}));
$("environment").onchange=e=>setEnvironment(e.target.value);
$("sky").oninput=e=>{scene.background.set(e.target.value);scene.fog.color.set(e.target.value);};
$("addBox").onclick=addBox;$("addTree").onclick=addTree;
$("addKey").onclick=()=>{const k=snapshot();if(!k)return;const i=keyframes.findIndex(x=>Math.abs(x.time-timeMs)<100);if(i>=0)keyframes[i]=k;else keyframes.push(k);renderKeys();};
$("scrubber").oninput=e=>{playing=false;$("play").textContent="Play";timeMs=Number(e.target.value);sample(timeMs);updateTimeUI();renderKeys();};
$("play").onclick=()=>{playing=!playing;$("play").textContent=playing?"Pause":"Play";lastTick=performance.now();};
$("stop").onclick=()=>{playing=false;$("play").textContent="Play";timeMs=0;$("scrubber").value=0;sample(0);updateTimeUI();};
$("export").onclick=exportProject;
$("capture").onclick=()=>renderer.domElement.toBlob(blob=>download(blob,"skil-cc-v4-preview.png"));
$("projectFile").onchange=async e=>{const f=e.target.files[0];if(!f)return;try{loadProject(JSON.parse(await f.text()));}catch(err){$("projectStatus").textContent="Gagal import: "+err.message;}e.target.value="";};
$("modelFile").onchange=async e=>{const f=e.target.files[0];if(!f)return;const url=URL.createObjectURL(f);loader.load(url,gltf=>{const model=gltf.scene;model.position.set(2,0,0);model.traverse(o=>{if(o.isMesh){o.castShadow=true;o.receiveShadow=true;}});world.add(model);props.push({type:"external-model",name:f.name});$("status").textContent="Model diimport: "+f.name;URL.revokeObjectURL(url);},undefined,err=>{$("status").textContent="Gagal memuat model GLB/GLTF.";console.error(err);URL.revokeObjectURL(url);});e.target.value="";};
function resize(){const w=stage.clientWidth,h=stage.clientHeight;camera.aspect=w/h;camera.updateProjectionMatrix();renderer.setSize(w,h,false);}
new ResizeObserver(resize).observe(stage);resize();
setEnvironment("studio");createCharacter({name:"Character 01"});
function animate(now){requestAnimationFrame(animate);const dt=Math.min((now-lastTick)/1000,.05);lastTick=now;if(playing){timeMs=Math.min(600000,timeMs+dt*1000);$("scrubber").value=timeMs;sample(timeMs);updateTimeUI();if(timeMs>=600000){playing=false;$("play").textContent="Play";}}controls.update();renderer.render(scene,camera);}
requestAnimationFrame(animate);
$("status").textContent="3D Studio siap.";
