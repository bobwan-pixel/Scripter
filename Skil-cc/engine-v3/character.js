const TAU=Math.PI*2;
const rounded=(ctx,x,y,w,h,r)=>{ctx.beginPath();ctx.roundRect(x,y,w,h,r);};
const fill=(ctx,color)=>{ctx.fillStyle=color;ctx.fill();};
const stroke=(ctx,color="#513b37",width=5)=>{ctx.strokeStyle=color;ctx.lineWidth=width;ctx.lineCap="round";ctx.lineJoin="round";ctx.stroke();};
const ellipse=(ctx,x,y,rx,ry,color,angle=0)=>{ctx.beginPath();ctx.ellipse(x,y,rx,ry,angle,0,TAU);fill(ctx,color);};
const mix=(hex,amount)=>{const n=parseInt(hex.slice(1),16),r=n>>16,g=n>>8&255,b=n&255;return `rgb(${Math.round(r+(255-r)*amount)},${Math.round(g+(255-g)*amount)},${Math.round(b+(255-b)*amount)})`;};
function mitten(ctx,x,y,angle,skin,scale=1){ctx.save();ctx.translate(x,y);ctx.rotate(angle);ellipse(ctx,0,0,19*scale,23*scale,skin);ellipse(ctx,9*scale,-5*scale,8*scale,11*scale,skin,-.45);ctx.restore();}
function drawFace(ctx,c,expression){
 const skin=c.skin, dark="#49352f";
 // Ears and neck
 ellipse(ctx,206,267,19,27,skin);ellipse(ctx,394,267,19,27,skin);
 rounded(ctx,267,330,66,88,20);fill(ctx,skin);
 // Face silhouette
 ctx.beginPath();ctx.moveTo(210,190);ctx.quadraticCurveTo(210,115,300,112);ctx.quadraticCurveTo(390,115,390,198);ctx.lineTo(379,276);ctx.quadraticCurveTo(360,338,300,345);ctx.quadraticCurveTo(240,338,221,276);ctx.closePath();fill(ctx,skin);stroke(ctx,dark,4);
 // soft cheek
 ellipse(ctx,245,278,18,9,mix(skin,.23));ellipse(ctx,355,278,18,9,mix(skin,.23));
 const eyeY=expression==="surprised"?230:237;
 if(expression==="happy"){ctx.beginPath();ctx.arc(257,eyeY,10,Math.PI,TAU);stroke(ctx,dark,5);ctx.beginPath();ctx.arc(343,eyeY,10,Math.PI,TAU);stroke(ctx,dark,5);}
 else {ellipse(ctx,258,eyeY,expression==="surprised"?7:6,expression==="surprised"?12:9,dark);ellipse(ctx,342,eyeY,expression==="surprised"?7:6,expression==="surprised"?12:9,dark);}
 if(expression==="worried"||expression==="sad"){ctx.beginPath();ctx.moveTo(243,211);ctx.quadraticCurveTo(256,202,270,213);ctx.moveTo(330,213);ctx.quadraticCurveTo(344,202,357,211);stroke(ctx,dark,5);}
 if(expression==="angry"){ctx.beginPath();ctx.moveTo(243,215);ctx.lineTo(271,225);ctx.moveTo(329,225);ctx.lineTo(357,215);stroke(ctx,dark,6);}
 // Nose
 ctx.beginPath();ctx.moveTo(300,244);ctx.quadraticCurveTo(289,263,301,265);stroke(ctx,mix(dark,.2),3);
 // Mouth
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
 // Back mass and layered locks
 ctx.beginPath();ctx.moveTo(210,230);ctx.quadraticCurveTo(175,90,270,75);ctx.quadraticCurveTo(355,40,390,130);ctx.quadraticCurveTo(426,170,390,280);ctx.lineTo(370,315);ctx.lineTo(356,220);ctx.quadraticCurveTo(300,190,246,226);ctx.lineTo(226,306);ctx.closePath();fill(ctx,h);stroke(ctx,"#392a28",5);
 ellipse(ctx,240,145,48,57,mix(h,.08),-.55);ellipse(ctx,305,112,65,48,mix(h,.06),-.12);ellipse(ctx,361,145,42,54,h,.5);
 ctx.beginPath();ctx.moveTo(213,204);ctx.quadraticCurveTo(248,139,296,161);ctx.quadraticCurveTo(337,112,389,184);ctx.quadraticCurveTo(345,176,323,207);ctx.quadraticCurveTo(281,182,249,223);ctx.quadraticCurveTo(230,238,213,204);closePath();fill(ctx,mix(h,.05));stroke(ctx,"#392a28",4);
}
function drawBody(ctx,c,pose){
 const skin=c.skin, shirt=c.outfit, pants=c.pants, dark="#493b38";
 // legs
 if(pose==="sit"){
  ctx.save();ctx.translate(0,20);
  ctx.beginPath();ctx.moveTo(252,560);ctx.lineTo(300,560);ctx.lineTo(280,675);ctx.lineTo(175,690);ctx.lineTo(170,658);ctx.lineTo(245,635);ctx.closePath();fill(ctx,pants);stroke(ctx,dark,5);
  ctx.beginPath();ctx.moveTo(310,560);ctx.lineTo(350,560);ctx.lineTo(410,655);ctx.lineTo(395,684);ctx.lineTo(305,640);ctx.closePath();fill(ctx,pants);stroke(ctx,dark,5);
  ctx.restore();
 }else{
  rounded(ctx,244,530,48,205,22);fill(ctx,pants);stroke(ctx,dark,5);
  rounded(ctx,308,530,48,205,22);fill(ctx,pants);stroke(ctx,dark,5);
 }
 // shoes
 ellipse(ctx,260,738,39,19,"#4b4546");ellipse(ctx,333,738,39,19,"#4b4546");
 // torso
 ctx.beginPath();ctx.moveTo(245,365);ctx.quadraticCurveTo(300,345,355,365);ctx.lineTo(385,535);ctx.quadraticCurveTo(300,565,215,535);ctx.closePath();fill(ctx,shirt);stroke(ctx,dark,5);
 // shirt shading
 ctx.beginPath();ctx.moveTo(300,375);ctx.lineTo(300,535);ctx.quadraticCurveTo(260,540,232,526);ctx.quadraticCurveTo(258,440,300,375);fill(ctx,mix(shirt,.18));
 // collar
 ctx.beginPath();ctx.moveTo(272,365);ctx.lineTo(300,395);ctx.lineTo(328,365);stroke(ctx,mix(shirt,.42),5);
 // arms, shoulders to hands
 ctx.save();
 if(pose==="wave"){
  ctx.beginPath();ctx.moveTo(350,390);ctx.quadraticCurveTo(400,360,414,300);ctx.lineTo(432,240);ctx.lineTo(462,250);ctx.lineTo(445,330);ctx.quadraticCurveTo(435,400,382,438);closePath();fill(ctx,shirt);stroke(ctx,dark,5);
  mitten(ctx,448,226,-.15,skin,1.03);
  ctx.beginPath();ctx.moveTo(250,395);ctx.quadraticCurveTo(206,435,202,520);ctx.lineTo(232,526);ctx.lineTo(272,430);closePath();fill(ctx,shirt);stroke(ctx,dark,5);mitten(ctx,211,535,0,skin);
 }else if(pose==="think"){
  ctx.beginPath();ctx.moveTo(350,390);ctx.quadraticCurveTo(405,400,389,465);ctx.lineTo(350,450);closePath();fill(ctx,shirt);stroke(ctx,dark,5);mitten(ctx,375,450,-.8,skin);
  ctx.beginPath();ctx.moveTo(250,390);ctx.quadraticCurveTo(205,400,225,470);ctx.lineTo(258,450);closePath();fill(ctx,shirt);stroke(ctx,dark,5);mitten(ctx,277,325,-.7,skin);
 }else{
  ctx.beginPath();ctx.moveTo(250,390);ctx.quadraticCurveTo(205,400,205,505);ctx.lineTo(235,525);ctx.quadraticCurveTo(260,450,275,430);closePath();fill(ctx,shirt);stroke(ctx,dark,5);mitten(ctx,218,535,.08,skin);
  ctx.beginPath();ctx.moveTo(350,390);ctx.quadraticCurveTo(395,400,395,505);ctx.lineTo(365,525);ctx.quadraticCurveTo(340,450,325,430);closePath();fill(ctx,shirt);stroke(ctx,dark,5);mitten(ctx,382,535,-.08,skin);
 }
 ctx.restore();
}
export function drawCharacter(ctx,c){
 ctx.save();ctx.translate(0,c.pose==="sit"?30:0);
 drawBody(ctx,c,c.pose);
 drawFace(ctx,c,c.expression);
 drawHair(ctx,c);
 // Hair highlight, understated
 ctx.beginPath();ctx.moveTo(244,124);ctx.quadraticCurveTo(278,82,326,91);stroke(ctx,mix(c.hair,.28),7);
 ctx.restore();
}
