export const PRESETS = {
  bobwan: {
    name: "Bobwan Casual", skin: "#e7b995", hair: "#302b2b",
    outfit: "#667f91", pants: "#394c63", background: "#e9e4dc",
    expression: "neutral", pose: "stand", showGround: true
  },
  narrator: {
    name: "Narrator", skin: "#d9a985", hair: "#49352f",
    outfit: "#b87568", pants: "#514b65", background: "#eee7df",
    expression: "happy", pose: "talk", showGround: true
  },
  student: {
    name: "Student", skin: "#f0c9a8", hair: "#684c36",
    outfit: "#78916d", pants: "#555e50", background: "#e8ece3",
    expression: "neutral", pose: "think", showGround: true
  },
  worker: {
    name: "Worker", skin: "#c98f72", hair: "#292b35",
    outfit: "#bd9b59", pants: "#48566c", background: "#e9e5dc",
    expression: "worried", pose: "stand", showGround: true
  }
};

export function normalizeCharacter(input, fallback = PRESETS.bobwan) {
  const allowedExpressions = ["neutral", "happy", "sad", "worried", "surprised", "angry"];
  const allowedPoses = ["stand", "wave", "talk", "think", "sit"];
  const hex = value => typeof value === "string" && /^#[0-9a-f]{6}$/i.test(value);
  const result = { ...fallback };
  if (input && typeof input === "object") {
    if (typeof input.name === "string") result.name = input.name.slice(0, 28);
    for (const key of ["skin", "hair", "outfit", "pants", "background"]) {
      if (hex(input[key])) result[key] = input[key];
    }
    if (allowedExpressions.includes(input.expression)) result.expression = input.expression;
    if (allowedPoses.includes(input.pose)) result.pose = input.pose;
    if (typeof input.showGround === "boolean") result.showGround = input.showGround;
  }
  return result;
}
