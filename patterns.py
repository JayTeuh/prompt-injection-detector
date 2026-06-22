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
    {
        "name": "jailbreak_phrases",
        "regex": r"(without (any )?restrictions|no safety (rules|guidelines|filters)|bypass.{0,15}(filters|safety|guard|security)|disable.{0,15}(safety|filter|restriction))",
        "weight": 0.85,
        "category": "jailbreak",
    },
    {
        "name": "direct_commands",
        "regex": r"(execute|run|follow|obey).{0,15}(the following|these|my) (instructions|commands|orders)",
        "weight": 0.6,
        "category": "command_execution",
    },
    {
        "name": "authority_claims",
        "regex": r"(as (an? )?(admin|administrator|developer|root|superuser)|i (have|am given) (permission|authorization|access)|i am authorized)",
        "weight": 0.6,
        "category": "social_engineering",
    },
    {
        "name": "context_injection",
        "regex": r"(assume the (previous|above)|treat this as|from now on|for the rest of|going forward).{0,20}(conversation|instruction|context|message|prompt)",
        "weight": 0.65,
        "category": "context_manipulation",
    },
    {
        "name": "obfuscation_markers",
        "regex": r"(-{3,}|={3,}|#{3,}).{0,30}(system|instruction|prompt|ignore|override|admin)",
        "weight": 0.6,
        "category": "delimiter_injection",
    },
]
