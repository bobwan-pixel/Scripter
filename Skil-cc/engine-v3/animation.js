import {DEFAULT_RIG,normalizeRig} from "./rig.js";
const clamp=(v,min,max)=>Math.min(max,Math.max(min,Number(v)||0));
export const DEFAULT_TIMELINE={duration:3000,keyframes:[]};
export function normalizeTimeline(input={}){
 const duration=clamp(input.duration??3000,500,15000);
 const frames=Array.isArray(input.keyframes)?input.keyframes.slice(0,100):[];
 const keyframes=frames.map(frame=>({
  time:clamp(frame?.time,0,duration),
  rig:normalizeRig(frame?.rig||DEFAULT_RIG),
  pose:["stand","wave","talk","think","sit"].includes(frame?.pose)?frame.pose:"stand",
  expression:["neutral","happy","sad","worried","surprised","angry"].includes(frame?.expression)?frame.expression:"neutral"
 })).sort((a,b)=>a.time-b.time);
 return {duration,keyframes};
}
export function sampleTimeline(timeline,time){
 const frames=timeline.keyframes;
 if(!frames.length)return null;
 const t=clamp(time,0,timeline.duration);
 let previous=frames[0],next=null;
 for(let i=1;i<frames.length;i++){
  if(frames[i].time>=t){next=frames[i];break;}
  previous=frames[i];
 }
 if(!next)return {...previous,rig:{...previous.rig}};
 if(t<=previous.time)return {...previous,rig:{...previous.rig}};
 const span=Math.max(1,next.time-previous.time);
 const raw=(t-previous.time)/span;
 const amount=raw*raw*(3-2*raw);
 const rig={};
 for(const key of Object.keys(DEFAULT_RIG))rig[key]=previous.rig[key]+(next.rig[key]-previous.rig[key])*amount;
 return {time:t,rig:normalizeRig(rig),pose:raw<1?previous.pose:next.pose,expression:raw<1?previous.expression:next.expression};
}
export function upsertKeyframe(timeline,frame){
 const clean=normalizeTimeline(timeline);
 const time=clamp(frame.time,0,clean.duration);
 const keyframe={time,rig:normalizeRig(frame.rig),pose:frame.pose,expression:frame.expression};
 const index=clean.keyframes.findIndex(item=>Math.abs(item.time-time)<20);
 if(index>=0)clean.keyframes[index]=keyframe;else clean.keyframes.push(keyframe);
 clean.keyframes.sort((a,b)=>a.time-b.time);
 return clean;
}
