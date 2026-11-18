const TAU=Math.PI*2;
const rounded=(ctx,x,y,w,h,r)=>{ctx.beginPath();ctx.roundRect(x,y,w,h,r);};
const fill=(ctx,color)=>{ctx.fillStyle=color;ctx.fill();};
const stroke=(ctx,color="#513b37",width=5)=>{ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap="round";ctx.lineJoin="round";ctx.stroke();};
const ellipse=(ctx,x,y,rx,ry,color,angle=0)=>{ctx.beginPath();ctx.ellipse(x,y,rx,ry,angle,0,TAU);fill(ctx,color);};
const mix=(hex,amount)=>{const n=parseInt(hex.slice(1),16),r=n>>16,g=n>>8&255,b=n&255;return `rgb(${Math.round(r+(255-r)*amount)},${Math.round(g+(255-g)*amount)},${Math.round(b+(255-b)*amount)})`;};
const point=(x,y,length,degrees)=>{const a=degrees*Math.PI/180;return{x:x+Math.sin(a)*length,y:y+Math.cos(a)*length};};
function segment(ctx,a,b,width,color,dark="#493b38"){
 ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.lineWidth=width;ctx.lineCap="round";ctx.strokeStyle=dark;ctx.stroke();
 ctx.beginPath();ctx.moveTo(a.x,a.y);ctx.lineTo(b.x,b.y);ctx.lineWidth=width-7;ctx.lineCap="round";ctx.strokeStyle=color;ctx.stroke();
}
function joint(ctx,p,r,color,dark="#493b38"){
 ellipse(ctx,p.x,p.y,r+3,r+3,dark);ellipse(ctx,p.x,p.y,r,r,color);
}
function mitten(ctx,x,y,angle,skin,scale=1){ctx.save();ctx.translate(x,y);ctx.rotate(angle);ellipse(ctx,0,0,19*scale,23*scale,skin);ellipse(ctx,9*scale,-5*scale,8*scale,11*scale,skin,-.45);ctx.restore();}
function drawFace(ctx,c,expression){
 const skin=c.skin,dark="#49352f";
 ellipse(ctx,206,267,19,27,skin);ellipse(ctx,394,267,19,27,skin);
 rounded(ctx,267,330,66,88,20);fill(ctx,skin);
 ctx.beginPath();ctx.moveTo(210,190);ctx.quadraticCurveTo(210,115,300,112);ctx.quadraticCurveTo(390,115,390,198);ctx.lineTo(379,276);ctx.quadraticCurveTo(360,338,300,345);ctx.quadraticCurveTo(240,338,221,276);ctx.closePath();fill(ctx,skin);stroke(ctx,dark,4);
 ellipse(ctx,245,278,18,9,mix(skin,.23));ellipse(ctx,355,278,18,9,mix(skin,.23));
 const eyeY=expression==="surprised"?230:237;
 if(expression==="happy"){ctx.beginPath();ctx.arc(257,eyeY,10,Math.PI,TAU);stroke(ctx,dark,5);ctx.beginPath();ctx.arc(343,eyeY,10,Math.PI,TAU);stroke(ctx,dark,5);}
 else {ellipse(ctx,258,eyeY,expression==="surprised"?7:6,expression==="surprised"?12:9,dark);ellipse(ctx,342,eyeY,expression==="surprised"?7:6,expression==="surprised"?12:9,dark);}
 if(expression==="worried"||expression==="sad"){ctx.beginPath();ctx.moveTo(243,211);ctx.quadraticCurveTo(256,202,270,213);ctx.moveTo(330,213);ctx.quadraticCurveTo(344,202,357,211);stroke(ctx,dark,5);}
 if(expression==="angry"){ctx.beginPath();ctx.moveTo(243,215);ctx.lineTo(271,225);ctx.moveTo(329,225);ctx.lineTo(357,215);stroke(ctx,dark,6);}
 ctx.beginPath();ctx.moveTo(300,244);ctx.quadraticCurveTo(289,263,301,265);stroke(ctx,mix(dark,.2),3);
 ctx.beginPath();
 if(expression==="happy"){ctx.moveTo(278,286);ctx.quadraticCurveTo(300,310,322,286);}
 else if(expression==="sad"||expression==="worried"){ctx.moveTo(280,302);ctx.quadraticCurveTo(300,282,320,302);}
 else if(expression==="surprised"){ctx.ellipse(300,294,9,14,0,0,TAU);}
 else if(expression==="angry"){ctx.moveTo(282,298);ctx.lineTo(318,298);}
 else {ctx.moveTo(285,294);ctx.quadraticCurveTo(300,300,315,294);}
 stroke(ctx,dark,5);
}
function drawHair(ctx,c){
 const h=c.hair;
 ctx.beginPath();ctx.moveTo(210,230);ctx.quadraticCurveTo(175,90,270,75);ctx.quadraticCurveTo(355,40,390,130);ctx.quadraticCurveTo(426,170,390,280);ctx.lineTo(370,315);ctx.lineTo(356,220);ctx.quadraticCurveTo(300,190,246,226);ctx.lineTo(226,306);ctx.closePath();fill(ctx,h);stroke(ctx,"#392a28",5);
 ellipse(ctx,240,145,48,57,mix(h,.08),-.55);ellipse(ctx,305,112,65,48,mix(h,.06),-.12);ellipse(ctx,361,145,42,54,h,.5);
 ctx.beginPath();ctx.moveTo(213,204);ctx.quadraticCurveTo(248,139,296,161);ctx.quadraticCurveTo(337,112,389,184);ctx.quadraticCurveTo(345,176,323,207);ctx.quadraticCurveTo(281,182,249,223);ctx.quadraticCurveTo(230,238,213,204);ctx.closePath();fill(ctx,mix(h,.05));stroke(ctx,"#392a28",4);
}
function drawArm(ctx,side,c,rig,pose,swing=0){
 const left=side==="left",shoulder={x:left?250:350,y:392};
 let shoulderAngle=(left?-7:7)+(left?rig.leftArm:rig.rightArm)+swing;
 let elbowBend=left?rig.leftElbow:rig.rightElbow;
 if(pose==="wave"&&!left){shoulderAngle=shoulderAngle-72;elbowBend+=-28;}
 if(pose==="think"){shoulderAngle+=left?12:-35;elbowBend+=left?-35:55;}
 const elbow=point(shoulder.x,shoulder.y,76,shoulderAngle);
 const forearmAngle=shoulderAngle+elbowBend;
 const wrist=point(elbow.x,elbow.y,70,forearmAngle);
 segment(ctx,shoulder,elbow,35,c.outfit);
 joint(ctx,elbow,15,c.outfit);
 segment(ctx,elbow,wrist,25,c.skin);
 mitten(ctx,wrist.x,wrist.y+8,forearmAngle*Math.PI/180,c.skin,.95);
}
function drawLeg(ctx,side,c,rig,swing=0,pose="stand"){
 const left=side==="left",hip={x:left?272:328,y:548};
 const thighAngle=(pose==="sit"?(left?-45:45):(left?-5:5))+(left?rig.leftLeg:rig.rightLeg)+swing;
 const knee=point(hip.x,hip.y,pose==="sit"?88:94,thighAngle);
 const bend=left?rig.leftKnee:rig.rightKnee;
 const shinAngle=pose==="sit"?(left?45:-45)+(left?bend:-bend):thighAngle+(left?-bend:bend);
 const ankle=point(knee.x,knee.y,pose==="sit"?88:96,shinAngle);
 segment(ctx,hip,knee,43,c.pants);
 joint(ctx,knee,19,c.pants);
 segment(ctx,knee,ankle,35,c.pants);
 ellipse(ctx,ankle.x+(left?-15:15),ankle.y+8,37,18,"#4b4546",left?-.08:.08);
}
function drawBody(ctx,c,pose,rig,motion){
 const swing=pose==="sit"?0:(motion?.walk?Math.sin((motion.time||0)/155)*24:0);
 drawLeg(ctx,"left",c,rig,swing,pose);
 drawLeg(ctx,"right",c,rig,-swing,pose);
 ctx.save();ctx.translate(300,430);ctx.rotate((rig.bodyLean||0)*Math.PI/180);ctx.translate(-300,-430);
 ctx.beginPath();ctx.moveTo(245,365);ctx.quadraticCurveTo(300,345,355,365);ctx.lineTo(385,535);ctx.quadraticCurveTo(300,565,215,535);ctx.closePath();fill(ctx,c.outfit);stroke(ctx,"#493b38",5);
 ctx.beginPath();ctx.moveTo(300,375);ctx.lineTo(300,535);ctx.quadraticCurveTo(260,540,232,526);ctx.quadraticCurveTo(258,440,300,375);fill(ctx,mix(c.outfit,.18));
 ctx.beginPath();ctx.moveTo(272,365);ctx.lineTo(300,395);ctx.lineTo(328,365);stroke(ctx,mix(c.outfit,.42),5);
 drawArm(ctx,"left",c,rig,pose,swing*.45);
 drawArm(ctx,"right",c,rig,pose,-swing*.45);
 ctx.restore();
}
export function drawCharacter(ctx,c,rig={},motion={}){
 ctx.save();ctx.translate(0,c.pose==="sit"?30:0);
 drawBody(ctx,c,c.pose,rig,motion);
 ctx.save();ctx.translate(300,330);ctx.rotate((rig.headTilt||0)*Math.PI/180);ctx.translate(-300,-330);
 drawFace(ctx,c,c.expression);drawHair(ctx,c);
 ctx.beginPath();ctx.moveTo(244,124);ctx.quadraticCurveTo(278,82,326,91);stroke(ctx,mix(c.hair,.28),7);
 ctx.restore();ctx.restore();
}
