export function idleOffset(time){return Math.sin(time/620)*2.2;}
export function blinkAt(time){const phase=time%4200;return phase>3950&&phase<4040;}
export function drawBlink(ctx){ctx.save();ctx.strokeStyle="#49352f";ctx.lineWidth=5;ctx.lineCap="round";ctx.beginPath();ctx.moveTo(248,237);ctx.lineTo(268,237);ctx.moveTo(332,237);ctx.lineTo(352,237);ctx.stroke();ctx.restore();}
