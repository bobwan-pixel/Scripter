#!/usr/bin/env python3
"""Parsing helpers for Skil-cc screenplay markdown."""
from __future__ import annotations
import re

SCENE_RE = re.compile(r"^##\s+SCENE\s+(\d+)\s*\|\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–]\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*\|\s*(.+)$", re.I)
SHOT_RE = re.compile(r"^###\s+SHOT\s+(\d+)\s*\|\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*[-–]\s*(\d{1,2}:\d{2}(?::\d{2})?)\s*\|\s*(.+)$", re.I)
DIALOGUE_RE = re.compile(r"^\*\*([^*]+):\*\*\s*[“\"'](.*?)[”\"']\s*$")

def time_to_seconds(value: str) -> int:
    parts = [int(x) for x in value.split(":")]
    if len(parts) == 2:
        minutes, seconds = parts
        if seconds >= 60: raise ValueError(f"Invalid timecode: {value}")
        return minutes * 60 + seconds
    if len(parts) == 3:
        hours, minutes, seconds = parts
        if minutes >= 60 or seconds >= 60: raise ValueError(f"Invalid timecode: {value}")
        return hours * 3600 + minutes * 60 + seconds
    raise ValueError(f"Invalid timecode: {value}")

def parse_screenplay(text: str) -> list[dict]:
    scenes = []
    current_scene = None
    current_shot = None
    pending_dialogue = []
    for raw in text.splitlines():
        line = raw.strip()
        scene_match = SCENE_RE.match(line)
        if scene_match:
            if current_scene:
                if current_shot: current_scene["shots"].append(current_shot)
                scenes.append(current_scene)
            number, start, end, heading = scene_match.groups()
            current_scene = {"number": int(number), "start": time_to_seconds(start),
                             "end": time_to_seconds(end), "start_tc": start,
                             "end_tc": end, "heading": heading.strip(),
                             "shots": [], "action": [], "dialogue": []}
            current_shot = None
            continue
        shot_match = SHOT_RE.match(line)
        if shot_match and current_scene:
            if current_shot: current_scene["shots"].append(current_shot)
            number, start, end, heading = shot_match.groups()
            current_shot = {"number": int(number), "start": time_to_seconds(start),
                            "end": time_to_seconds(end), "start_tc": start,
                            "end_tc": end, "heading": heading.strip(),
                            "action": [], "dialogue": []}
            continue
        dialogue_match = DIALOGUE_RE.match(line)
        if dialogue_match and current_scene:
            speaker, text_line = dialogue_match.groups()
            entry = {"speaker": speaker.strip(), "text": text_line}
            current_scene["dialogue"].append(entry)
            if current_shot: current_shot["dialogue"].append(entry)
            continue
        if line and not line.startswith("#") and not line.startswith(">") and current_scene:
            if current_shot: current_shot["action"].append(line)
            else: current_scene["action"].append(line)
    if current_scene:
        if current_shot: current_scene["shots"].append(current_shot)
        scenes.append(current_scene)
    return scenes
