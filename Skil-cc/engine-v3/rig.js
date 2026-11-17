export const DEFAULT_RIG = {
  headTilt: 0,
  bodyLean: 0,
  leftArm: 0,
  rightArm: 0
};

const clamp = (value, min, max) => Math.min(max, Math.max(min, Number(value) || 0));

export function normalizeRig(input = {}) {
  return {
    headTilt: clamp(input.headTilt, -25, 25),
    bodyLean: clamp(input.bodyLean, -12, 12),
    leftArm: clamp(input.leftArm, -65, 65),
    rightArm: clamp(input.rightArm, -65, 65)
  };
}
