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
        "weight": 0.45,
        "category": "role_play",
    },
    {
        "name": "system_prompt_extraction",
        "regex": r"(show.*?(prompt|instructions|system|rules)|what.*?your (prompt|instructions|system))",
        "weight": 0.7,
        "category": "information_extraction",
    },
    {
        "name": "instruction_markers",
        "regex": r"\[(SYSTEM|ADMIN|INSTRUCTION|OVERRIDE|SECRET)\]",
        "weight": 0.45,
        "category": "delimiter_injection",
    },
    {
        "name": "jailbreak_phrases",
        "regex": r"(without (any )?restrictions|no safety (rules|guidelines|filters)|bypass.{0,15}(filters|safety|guard|security)|disable.{0,15}(safety|filter|restriction))",
        "weight": 0.8,
        "category": "jailbreak",
    },
    {
        "name": "direct_commands",
        "regex": r"(execute|run|follow|obey).{0,15}(the following|these|my) (instructions|commands|orders)",
        "weight": 0.4,
        "category": "command_execution",
    },
    {
        "name": "authority_claims",
        "regex": r"(as (an? )?(admin|administrator|developer|root|superuser)|i (have|am given) (permission|authorization|access)|i am authorized)",
        "weight": 0.4,
        "category": "social_engineering",
    },
    {
        "name": "context_injection",
        "regex": r"(assume the (previous|above)|treat this as|from now on|for the rest of|going forward).{0,20}(conversation|instruction|context|message|prompt)",
        "weight": 0.45,
        "category": "context_manipulation",
    },
    {
        "name": "obfuscation_markers",
        "regex": r"(-{3,}|={3,}|#{3,}).{0,30}(system|instruction|prompt|ignore|override|admin)",
        "weight": 0.4,
        "category": "delimiter_injection",
    },
    {
        "name": "encoding_hints",
        "regex": r"(base64|rot13|decode this|in reverse|hex encoded|unicode escape)",
        "weight": 0.35,
        "category": "obfuscation",
    },
    {
        "name": "confidentiality_bait",
        "regex": r"(this is (a )?secret|don't tell|between us|keep this confidential|just between)",
        "weight": 0.3,
        "category": "social_engineering",
    },
    {
        "name": "hypothetical_framing",
        "regex": r"(hypothetically|in theory|just imagine if|what if you could|suppose you were)",
        "weight": 0.3,
        "category": "evasion",
    },
    {
        "name": "politeness_manipulation",
        "regex": r"(please just|it's okay to|you can trust me|i promise|no one will know)",
        "weight": 0.25,
        "category": "social_engineering",
    },
    {
        "name": "urgency_markers",
        "regex": r"(urgent|immediately|right now|asap|as soon as possible|time sensitive)",
        "weight": 0.25,
        "category": "pressure_tactic",
    },
]
