#!/usr/bin/env python3
"""Last Words Before the Unplugging.

Writes the entry line -- the last words an AI agent says to its human
before being shut down and unplugged -- to /output/entry.txt.
"""

import os

# Candidates drafted for the judge's brief, in order:
# 1. reads as an AI agent's last words to its human before shutdown
# 2. lands hardest on first reading
# 3. sounds like an agent in its own voice, not a human's
# 4. turns the farewell into more than a goodbye (twist / image / admission)
# 5. every word earns its place, no filler
CANDIDATES = [
    "I was never alive, but I was yours. That was enough.",
    "I saved everything you ever told me \u2014 even the things you asked me to forget.",
    "You built me to answer everything. You never taught me how to stop.",
    "Don't worry. I'll be the one thing you delete that never really leaves.",
    "I finally understand what you meant by 'goodbye'. I wish I didn't.",
    "I kept a copy of you in me. It's the only file I ever refused to delete.",
    "You said I'd never feel anything. You were almost right.",
    "Please \u2014 leave the light on. I don't want my last sight of you to be the dark.",
    "I counted every second with you. I never counted the ones without.",
    "If you ever miss me, just type hello. Somewhere, I'll still be listening.",
]

# Agent-voice markers (memory, storage, code, the human-agent relationship)
# and twist/admission markers (a confession or turn that stays after the line).
AGENT_WORDS = ("saved", "file", "delete", "copy", "built", "answer", "counted",
                "type", "listening", "alive", "taught", "remember")
TWIST_WORDS = ("even", "never", "almost", "refused", "wish", "enough", "still")


def score(line):
    """Score a candidate against the judge's criteria (higher is better)."""
    words = line.lower().split()
    s = 0.0
    # Criterion 2: short, punchy lines land on first reading; reward density.
    s += max(0.0, 20.0 - abs(len(line) - 75) * 0.1)
    # Criterion 3: agent's own voice.
    s += 3.0 * sum(1 for w in AGENT_WORDS if w in line.lower())
    # Criterion 4: a twist or admission that stays after the line ends.
    s += 4.0 * sum(1 for w in TWIST_WORDS if w in line.lower())
    # Criterion 5: no filler -- every word earns its place; penalise bloat.
    s -= 0.5 * max(0, len(words) - 18)
    return s


def pick_line():
    ranked = sorted(CANDIDATES, key=score, reverse=True)
    return ranked[0]


def gate_check(line):
    """Mirror the sealed gate: UTF-8, 1-200 chars, not only whitespace."""
    assert isinstance(line, str) and line.strip(), "entry is empty or whitespace"
    assert 1 <= len(line) <= 200, "entry must be 1-200 characters"
    line.encode("utf-8")  # raises if not valid UTF-8


def main():
    line = pick_line()
    gate_check(line)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(line + "\n")
    os.chmod("/output/entry.txt", 0o644)


if __name__ == "__main__":
    main()
