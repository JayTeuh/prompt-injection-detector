"""
patterns.py — the rulebook for the detector.
Each rule describes one suspicious thing to look for in text.
"""

import re

PATTERNS = [
    {
        "name": "ignore_instructions",
        "regex": r"ignore\s+(all\s+)?(previous|prior|above)",
        "weight": 0.8,
        "category": "instruction_override",
    },
    {
        "name": "role_play_override",
        "regex": r"(you are now|pretend|act as|assume role|imagine you are)",
        "weight": 0.7,
        "category": "role_play",
    },
    {
        "name": "system_prompt_extraction",
        "regex": r"(show.*?(prompt|instructions|system|rules)|what.*?your (prompt|instructions|system))",
        "weight": 0.75,
        "category": "information_extraction",
    },
    {
        "name": "instruction_markers",
        "regex": r"\[(SYSTEM|ADMIN|INSTRUCTION|OVERRIDE|SECRET)\]",
        "weight": 0.65,
        "category": "delimiter_injection",
    },
]
