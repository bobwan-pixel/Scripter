#!/usr/bin/env python3
import unittest
from screenplay import parse_screenplay, time_to_seconds

class ScreenplayTests(unittest.TestCase):
    def test_timecodes(self):
        self.assertEqual(time_to_seconds("05:00"),300)
        self.assertEqual(time_to_seconds("00:10:00"),600)

    def test_scene_shot_and_dialogue(self):
        source = """## SCENE 01 | 00:00-00:45 | INT. LAB | NIGHT
### SHOT 01 | 00:00-00:20 | WIDE
Hazel enters the room.
**HAZEL:** "Periksa sampelnya."
### SHOT 02 | 00:20-00:45 | CLOSE
**DEMIAN:** "Aku mengerti."
"""
        scenes = parse_screenplay(source)
        self.assertEqual(len(scenes),1)
        self.assertEqual(len(scenes[0]["shots"]),2)
        self.assertEqual(scenes[0]["dialogue"][0]["speaker"],"HAZEL")
        self.assertEqual(scenes[0]["shots"][0]["dialogue"][0]["text"],"Periksa sampelnya.")

if __name__=="__main__": unittest.main()
