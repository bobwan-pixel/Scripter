export const DEFAULT_RIG = {
  headTilt: 0, bodyLean: 0,
  leftArm: 0, rightArm: 0,
  leftElbow: 0, rightElbow: 0,
  leftLeg: 0, rightLeg: 0,
  leftKnee: 0, rightKnee: 0
};
const clamp=(value,min,max)=>Math.min(max,Math.max(min,Number(value)||0));
export function normalizeRig(input={}){
 return {
  headTilt:clamp(input.headTilt,-25,25),bodyLean:clamp(input.bodyLean,-12,12),
  leftArm:clamp(input.leftArm,-65,65),rightArm:clamp(input.rightArm,-65,65),
  leftElbow:clamp(input.leftElbow,-90,90),rightElbow:clamp(input.rightElbow,-90,90),
  leftLeg:clamp(input.leftLeg,-35,35),rightLeg:clamp(input.rightLeg,-35,35),
  leftKnee:clamp(input.leftKnee,-65,65),rightKnee:clamp(input.rightKnee,-65,65)
 };
}
