from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]

class Skill3DContractTests(unittest.TestCase):
    def read(self, path):
        return (ROOT / path).read_text(encoding="utf-8")

    def test_user_sources_are_locked(self):
        skill = self.read("SKILL.md").lower()
        self.assertIn("never", skill)
        self.assertIn("dialogue audio", skill)
        self.assertIn("do not", skill)
        self.assertIn("rewrite", skill)

    def test_duration_choices_are_present(self):
        skill = self.read("SKILL.md")
        for choice in ("30–60 seconds", "1–5 minutes", "5–10 minutes"):
            self.assertIn(choice, skill)

    def test_visual_standard(self):
        visual = self.read("references/VISUAL-STANDARD.md").lower()
        self.assertIn("low-poly 3d", visual)
        self.assertIn("medium detail", visual)
        self.assertIn("modern", visual)
        self.assertIn("post-apocalyptic", visual)

    def test_blender_pipeline_exists(self):
        for path in (
            "tools/blender_preflight.py",
            "tools/blender/build_lowpoly_character.py",
            "tools/blender/build_modern_ruins_blockout.py",
            "tools/blender/apply_visemes.py",
            "tools/render_range.py",
            "tools/encode_mp4.py",
            "tools/video_qa.py",
            "tools/audio_timing.py",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

if __name__ == "__main__":
    unittest.main()
