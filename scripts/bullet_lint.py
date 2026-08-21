"""Deterministic per-bullet lint for resume markdown.

    python3 scripts/bullet_lint.py <resume.md>

Rubric pattern in the Resume Worded / Rezi family, reimplemented deterministically.
Seconds-fast, deterministic, runs at Step 3 on every application. It REPORTS; the
full Hiring Manager critique remains reserved for roles the owner cares about.

Per bullet: word count vs the 15-25 design-spec band, weak-verb openers, filler
phrases (AI tells and corporate blandness, Rule 5), metric presence, and repeated
leading verbs across the document.
"""
import re
import sys
from collections import Counter

WEAK_OPENERS = [
    "responsible for", "helped", "assisted", "worked on", "participated",
    "supported", "involved in", "tasked with", "duties included", "aided",
]
FILLER = [
    "results-driven", "proven track record", "dynamic", "synerg", "leverag",
    "best-in-class", "passionate", "cutting-edge", "seasoned", "detail-oriented",
    "team player", "go-getter", "utilize", "utilized", "spearheaded", "impactful",
    "world-class", "state-of-the-art", "hit the ground running",
]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    text = open(sys.argv[1], encoding="utf-8").read()
    bullets = [l.strip()[2:].strip() for l in text.splitlines() if l.strip().startswith("- ")]
    if not bullets:
        sys.exit("no bullets found (lines starting with '- ')")

    first_words = Counter()
    flags_total = 0
    print(f"== bullet lint: {sys.argv[1]} ({len(bullets)} bullets)")
    for i, b in enumerate(bullets, 1):
        plain = re.sub(r"\*\*|\[|\]|\(.*?\)", "", b)
        words = plain.split()
        flags = []
        if len(words) < 12:
            flags.append(f"short ({len(words)}w; spec band 15-25)")
        elif len(words) > 28:
            flags.append(f"long ({len(words)}w; spec band 15-25)")
        low = plain.lower()
        for w in WEAK_OPENERS:
            if low.startswith(w):
                flags.append(f"weak opener '{w}'")
        for f in FILLER:
            if f in low:
                flags.append(f"filler '{f}'")
        if not re.search(r"\d|%|\$", plain):
            flags.append("no metric/number (fine if the bullet is scope, not outcome)")
        fw = words[0].lower().rstrip(",.") if words else ""
        first_words[fw] += 1
        if flags:
            flags_total += len(flags)
            print(f"  [{i}] {plain[:70]}...")
            for f in flags:
                print(f"      · {f}")
    repeats = [(w, c) for w, c in first_words.items() if c > 2]
    for w, c in repeats:
        print(f"  · leading verb '{w}' opens {c} bullets, vary the structure")
    if not flags_total and not repeats:
        print("  ✓ clean")


if __name__ == "__main__":
    main()
