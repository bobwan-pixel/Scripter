import {drawCharacter} from "./character.js";
import {idleOffset,blinkAt,drawBlink} from "./motion.js";
const canvas=document.querySelector("#scene"),ctx=canvas.getContext("2d");
const defaults={name:"Character 01",skin:"#e7b995",hair:"#593b32",outfit:"#648b9c",pants:"#394c63",background:"#e9e4dc",expression:"neutral",pose:"stand",showGround:true};
const state={...defaults};let last=0,animate=true;
const $=id=>document.getElementById(id);
function roundedRect(x,y,w,h,r,color){ctx.beginPath();ctx.roundRect(x,y,w,h,r);ctx.fillStyle=color;ctx.fill();}
function render(time=0){
 ctx.clearRect(0,0,600,900);ctx.fillStyle=state.background;ctx.fillRect(0,0,600,900);
 // soft background halo
 const halo=ctx.createRadialGradient(300,390,40,300,390,340);halo.addColorStop(0,"#ffffff35");halo.addColorStop(1,"#ffffff00");ctx.fillStyle=halo;ctx.fillRect(0,0,600,900);
 if(state.showGround){ctx.beginPath();ctx.ellipse(300,765,135,20,0,0,Math.PI*2);ctx.fillStyle="#544b4430";ctx.fill();}
 ctx.save();ctx.translate(0,state.pose==="sit"?0:idleOffset(time));
 drawCharacter(ctx,state);
 if(blinkAt(time)&&state.expression!=="surprised")drawBlink(ctx);
 ctx.restore();
 // studio framing guides
 ctx.strokeStyle="#ffffff30";ctx.lineWidth=2;ctx.setLineDash([7,9]);ctx.strokeRect(36,36,528,828);ctx.setLineDash([]);
 if(animate)requestAnimationFrame(render);
}
function setValue(key,value){state[key]=value; if(key==="name")return; }
["name","skin","hair","outfit","pants","background"].forEach(key=>$(key).addEventListener("input",e=>{setValue(key,e.target.value);if(key==="background")render();}));
$("showGround").addEventListener("change",e=>{state.showGround=e.target.checked;render();});
function bindChoices(id,key){$(id).querySelectorAll("button").forEach(btn=>btn.addEventListener("click",()=>{$(id).querySelectorAll("button").forEach(b=>b.classList.remove("active"));btn.classList.add("active");state[key]=btn.dataset.value;render();}));}
bindChoices("expressions","expression");bindChoices("poses","pose");
function sync(){for(const key of ["name","skin","hair","outfit","pants","background"])$(key).value=state[key];$("showGround").checked=state.showGround;document.querySelectorAll(".choices button").forEach(b=>b.classList.toggle("active",b.dataset.value===state[b.parentElement.id==="poses"?"pose":"expression"]));render();}
$("reset").addEventListener("click",()=>{Object.assign(state,defaults);sync();});
$("randomize").addEventListener("click",()=>{const palettes=[["#e7b995","#593b32","#648b9c","#394c63"],["#d9a985","#302d3b","#b87568","#514b65"],["#f0c9a8","#684c36","#78916d","#555e50"],["#c98f72","#292b35","#bd9b59","#48566c"]];const p=palettes[Math.floor(Math.random()*palettes.length)];[state.skin,state.hair,state.outfit,state.pants]=p;sync();});
$("download").addEventListener("click",()=>{const a=document.createElement("a");a.download=(state.name.trim().replace(/[^a-z0-9-_]+/gi,"-")||"character")+".png";a.href=canvas.toDataURL("image/png");a.click();});
$("downloadJson").addEventListener("click",()=>{const blob=new Blob([JSON.stringify({...state,name:$("name").value},null,2)],{type:"application/json"});const a=document.createElement("a");a.href=URL.createObjectURL(blob);a.download="character-profile.json";a.click();URL.revokeObjectURL(a.href);});
render();
