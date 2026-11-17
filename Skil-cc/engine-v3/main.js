import {drawCharacter} from "./character.js";
import {idleOffset,blinkAt,drawBlink} from "./motion.js";
import {PRESETS,normalizeCharacter} from "./character-presets.js";

const canvas=document.querySelector("#scene"),ctx=canvas.getContext("2d");
const defaults=normalizeCharacter(PRESETS.bobwan);
const state={...defaults};
const $=id=>document.getElementById(id);
let animationFrame=0;

function render(time=0){
  ctx.clearRect(0,0,600,900);
  ctx.fillStyle=state.background;
  ctx.fillRect(0,0,600,900);
  const halo=ctx.createRadialGradient(300,390,40,300,390,340);
  halo.addColorStop(0,"#ffffff35");
  halo.addColorStop(1,"#ffffff00");
  ctx.fillStyle=halo;
  ctx.fillRect(0,0,600,900);
  if(state.showGround){
    ctx.beginPath();
    ctx.ellipse(300,765,135,20,0,0,Math.PI*2);
    ctx.fillStyle="#544b4430";
    ctx.fill();
  }
  ctx.save();
  ctx.translate(0,state.pose==="sit"?0:idleOffset(time));
  drawCharacter(ctx,state);
  if(blinkAt(time)&&state.expression!=="surprised")drawBlink(ctx);
  ctx.restore();
  ctx.strokeStyle="#ffffff30";
  ctx.lineWidth=2;
  ctx.setLineDash([7,9]);
  ctx.strokeRect(36,36,528,828);
  ctx.setLineDash([]);
}
function startAnimation(){
  if(animationFrame) return;
  const loop=time=>{
    render(time);
    animationFrame=requestAnimationFrame(loop);
  };
  animationFrame=requestAnimationFrame(loop);
}
function sync(){
  for(const key of ["name","skin","hair","outfit","pants","background"]){
    $(key).value=state[key];
  }
  $("showGround").checked=state.showGround;
  document.querySelectorAll(".choices button").forEach(btn=>{
    const group=btn.closest(".choices").id;
    btn.classList.toggle("active",btn.dataset.value===state[group==="poses"?"pose":"expression"]);
  });
  $("preset").value="custom";
  render();
}
function applyProfile(profile){
  Object.assign(state,normalizeCharacter(profile,defaults));
  sync();
}
for(const key of ["name","skin","hair","outfit","pants","background"]){
  $(key).addEventListener("input",event=>{
    state[key]=event.target.value;
    render();
  });
}
$("showGround").addEventListener("change",event=>{
  state.showGround=event.target.checked;
  render();
});
function bindChoices(id,key){
  $(id).querySelectorAll("button").forEach(btn=>{
    btn.addEventListener("click",()=>{
      $(id).querySelectorAll("button").forEach(item=>item.classList.remove("active"));
      btn.classList.add("active");
      state[key]=btn.dataset.value;
      render();
    });
  });
}
bindChoices("expressions","expression");
bindChoices("poses","pose");

$("preset").addEventListener("change",event=>{
  if(PRESETS[event.target.value]) applyProfile(PRESETS[event.target.value]);
});
$("reset").addEventListener("click",()=>applyProfile(defaults));
$("randomize").addEventListener("click",()=>{
  const keys=["bobwan","narrator","student","worker"];
  const key=keys[Math.floor(Math.random()*keys.length)];
  const palette=PRESETS[key];
  state.skin=palette.skin;
  state.hair=palette.hair;
  state.outfit=palette.outfit;
  state.pants=palette.pants;
  sync();
});
$("download").addEventListener("click",()=>{
  const a=document.createElement("a");
  a.download=(state.name.trim().replace(/[^a-z0-9-_]+/gi,"-")||"character")+".png";
  a.href=canvas.toDataURL("image/png");
  a.click();
});
$("downloadJson").addEventListener("click",()=>{
  const blob=new Blob([JSON.stringify({...state},null,2)],{type:"application/json"});
  const url=URL.createObjectURL(blob);
  const a=document.createElement("a");
  a.href=url;
  a.download=(state.name.trim().replace(/[^a-z0-9-_]+/gi,"-")||"character")+".json";
  a.click();
  URL.revokeObjectURL(url);
});
$("importJson").addEventListener("change",async event=>{
  const file=event.target.files?.[0];
  if(!file) return;
  try{
    const profile=JSON.parse(await file.text());
    applyProfile(profile);
    $("status").textContent="Profil karakter berhasil dimuat.";
  }catch{
    $("status").textContent="File JSON tidak valid. Gunakan hasil export dari Character Studio.";
  }
  event.target.value="";
});
render();
startAnimation();
