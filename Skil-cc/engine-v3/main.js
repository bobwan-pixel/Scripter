import {drawCharacter} from "./character.js";
import {idleOffset,blinkAt,drawBlink} from "./motion.js";
import {PRESETS,normalizeCharacter} from "./character-presets.js";
import {DEFAULT_RIG,normalizeRig} from "./rig.js";
import {DEFAULT_TIMELINE,normalizeTimeline,sampleTimeline,upsertKeyframe} from "./animation.js";
const canvas=document.querySelector("#scene"),ctx=canvas.getContext("2d");
const defaults=normalizeCharacter(PRESETS.bobwan);
const state={...defaults,rig:normalizeRig(defaults.rig||DEFAULT_RIG),walkMode:false,timeline:normalizeTimeline(DEFAULT_TIMELINE)};
const $=id=>document.getElementById(id);
let animationFrame=0,playing=false,playStartedAt=0,playStartTime=0,playhead=0,selectedTime=null;
const formatTime=ms=>(ms/1000).toFixed(2)+"s";
function setPlayhead(value,apply=true){
 playhead=Math.max(0,Math.min(state.timeline.duration,Number(value)||0));
 $("timelineScrubber").value=playhead;
 $("playheadLabel").textContent=formatTime(playhead)+" / "+formatTime(state.timeline.duration);
 if(apply){
  const frame=sampleTimeline(state.timeline,playhead);
  if(frame){state.rig=normalizeRig(frame.rig);state.pose=frame.pose;state.expression=frame.expression;syncRigControls();syncChoices();}
 }
 render();
}
function syncRigControls(){
 for(const key of Object.keys(DEFAULT_RIG)){$(key).value=state.rig[key];$(key+"Value").textContent=Math.round(state.rig[key])+"°";}
}
function syncChoices(){
 document.querySelectorAll(".choices button").forEach(btn=>{const group=btn.closest(".choices").id;btn.classList.toggle("active",btn.dataset.value===state[group==="poses"?"pose":"expression"]);});
}
function render(time=0){
 ctx.clearRect(0,0,600,900);ctx.fillStyle=state.background;ctx.fillRect(0,0,600,900);
 const halo=ctx.createRadialGradient(300,390,40,300,390,340);halo.addColorStop(0,"#ffffff35");halo.addColorStop(1,"#ffffff00");ctx.fillStyle=halo;ctx.fillRect(0,0,600,900);
 if(state.showGround){ctx.beginPath();ctx.ellipse(300,765,135,20,0,0,Math.PI*2);ctx.fillStyle="#544b4430";ctx.fill();}
 ctx.save();ctx.translate(0,state.pose==="sit"?0:idleOffset(time));
 drawCharacter(ctx,state,state.rig,{walk:state.walkMode&&state.pose!=="sit",time});
 if(blinkAt(time)&&state.expression!=="surprised")drawBlink(ctx);
 ctx.restore();ctx.strokeStyle="#ffffff30";ctx.lineWidth=2;ctx.setLineDash([7,9]);ctx.strokeRect(36,36,528,828);ctx.setLineDash([]);
}
function renderKeyframes(){
 const host=$("keyframeList");host.replaceChildren();
 if(!state.timeline.keyframes.length){const empty=document.createElement("small");empty.textContent="Belum ada keyframe. Atur pose lalu tekan Tambah keyframe.";host.append(empty);return;}
 state.timeline.keyframes.forEach(frame=>{
  const button=document.createElement("button");button.type="button";button.className="keyframe-chip"+(selectedTime===frame.time?" active":"");
  button.textContent=formatTime(frame.time)+" · "+frame.pose;
  button.addEventListener("click",()=>{selectedTime=frame.time;setPlayhead(frame.time);renderKeyframes();});
  host.append(button);
 });
}
function refreshTimeline(){
 $("duration").value=state.timeline.duration;
 $("timelineScrubber").max=state.timeline.duration;
 setPlayhead(playhead,false);renderKeyframes();
}
function sync(){
 for(const key of ["name","skin","hair","outfit","pants","background"])$(key).value=state[key];
 $("showGround").checked=state.showGround;$("walkMode").checked=state.walkMode;
 syncRigControls();syncChoices();$("preset").value="custom";refreshTimeline();render();
}
function applyProfile(profile){
 Object.assign(state,normalizeCharacter(profile,defaults));
 state.walkMode=Boolean(profile.walkMode);
 state.timeline=normalizeTimeline(profile.timeline||DEFAULT_TIMELINE);
 playing=false;selectedTime=null;playhead=0;$("playButton").textContent="Play";
 sync();
}
function pausePlayback(){playing=false;$("playButton").textContent="Play";}
for(const key of ["name","skin","hair","outfit","pants","background"]){$(key).addEventListener("input",event=>{state[key]=event.target.value;render();});}
$("showGround").addEventListener("change",event=>{state.showGround=event.target.checked;render();});
$("walkMode").addEventListener("change",event=>{state.walkMode=event.target.checked;render();});
function bindChoices(id,key){$(id).querySelectorAll("button").forEach(btn=>btn.addEventListener("click",()=>{$(id).querySelectorAll("button").forEach(item=>item.classList.remove("active"));btn.classList.add("active");state[key]=btn.dataset.value;render();}));}
bindChoices("expressions","expression");bindChoices("poses","pose");
for(const key of Object.keys(DEFAULT_RIG)){$(key).addEventListener("input",event=>{state.rig=normalizeRig({...state.rig,[key]:Number(event.target.value)});$(key+"Value").textContent=Math.round(state.rig[key])+"°";$("preset").value="custom";render();});}
$("resetRig").addEventListener("click",()=>{state.rig={...DEFAULT_RIG};syncRigControls();render();});
$("preset").addEventListener("change",event=>{if(PRESETS[event.target.value])applyProfile(PRESETS[event.target.value]);});
$("reset").addEventListener("click",()=>applyProfile(defaults));
$("randomize").addEventListener("click",()=>{const keys=["bobwan","narrator","student","worker"],palette=PRESETS[keys[Math.floor(Math.random()*keys.length)]];state.skin=palette.skin;state.hair=palette.hair;state.outfit=palette.outfit;state.pants=palette.pants;sync();});
$("duration").addEventListener("change",event=>{
 pausePlayback();state.timeline=normalizeTimeline({...state.timeline,duration:Number(event.target.value)});
 state.timeline.keyframes=state.timeline.keyframes.map(frame=>({...frame,time:Math.min(frame.time,state.timeline.duration)})).sort((a,b)=>a.time-b.time);
 playhead=Math.min(playhead,state.timeline.duration);selectedTime=null;refreshTimeline();
});
$("timelineScrubber").addEventListener("input",event=>{pausePlayback();selectedTime=null;setPlayhead(event.target.value);renderKeyframes();});
$("addKeyframe").addEventListener("click",()=>{
 state.timeline=upsertKeyframe(state.timeline,{time:playhead,rig:state.rig,pose:state.pose,expression:state.expression});
 selectedTime=playhead;renderKeyframes();$("timelineStatus").textContent="Keyframe disimpan pada "+formatTime(playhead)+".";
});
$("deleteKeyframe").addEventListener("click",()=>{
 const index=state.timeline.keyframes.findIndex(frame=>Math.abs(frame.time-(selectedTime??playhead))<20);
 if(index<0){$("timelineStatus").textContent="Pilih keyframe yang mau dihapus.";return;}
 state.timeline.keyframes.splice(index,1);selectedTime=null;renderKeyframes();$("timelineStatus").textContent="Keyframe dihapus.";
});
$("playButton").addEventListener("click",()=>{
 if(playing){pausePlayback();return;}
 if(!state.timeline.keyframes.length){$("timelineStatus").textContent="Tambahkan minimal satu keyframe dulu.";return;}
 if(playhead>=state.timeline.duration)setPlayhead(0);
 playing=true;playStartedAt=performance.now();playStartTime=playhead;$("playButton").textContent="Pause";
});
$("stopButton").addEventListener("click",()=>{pausePlayback();selectedTime=null;setPlayhead(0);renderKeyframes();});
$("download").addEventListener("click",()=>{const a=document.createElement("a");a.download=(state.name.trim().replace(/[^a-z0-9-_]+/gi,"-")||"character")+".png";a.href=canvas.toDataURL("image/png");a.click();});
$("downloadJson").addEventListener("click",()=>{const blob=new Blob([JSON.stringify({...state,timeline:state.timeline},null,2)],{type:"application/json"}),url=URL.createObjectURL(blob),a=document.createElement("a");a.href=url;a.download=(state.name.trim().replace(/[^a-z0-9-_]+/gi,"-")||"character")+".json";a.click();URL.revokeObjectURL(url);});
$("importJson").addEventListener("change",async event=>{const file=event.target.files?.[0];if(!file)return;try{applyProfile(JSON.parse(await file.text()));$("status").textContent="Profil karakter dan timeline berhasil dimuat.";}catch{$("status").textContent="File JSON tidak valid. Gunakan hasil export Character Studio.";}event.target.value="";});
renderKeyframes();refreshTimeline();
function loop(time){
 if(playing){
  const next=playStartTime+(time-playStartedAt);
  if(next>=state.timeline.duration){setPlayhead(state.timeline.duration);pausePlayback();}
  else setPlayhead(next);
 }
 render(time);animationFrame=requestAnimationFrame(loop);
}
animationFrame=requestAnimationFrame(loop);
