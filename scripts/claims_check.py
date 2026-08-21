"""Claims consistency check: every number and every title/date in a document must trace
to the truth layer.

    python3 scripts/claims_check.py <document.md> [--skills profile/master_skills.md]
                                                  [--history profile/employment_history.md]

This is the mechanical half of Rules 1, 3, and 4. Other tools generate claims; this one
refuses them. It runs on any markdown document you are about to send (resume, cover
letter, form answer) and reports, per claim:

  NUMBERS (every figure in the body: counts, percentages, dollars, multiples, "N years")
    ANCHORED   the value appears in a master_skills.md entry marked "Metrics Cleared: Yes"
    UNCLEARED  the value appears in master_skills.md, but only in entries NOT marked cleared
               (a fact of scale may be fine; an outcome metric is not) -> confirm the basis
    MISSING    the value appears nowhere in master_skills.md -> hard fail
    + a warning when target language ("goal", "aimed", "on track", "projected" ...) sits on
      the same line as a number: a target is not an outcome.

  TITLES AND DATES (resume role headings "### Title, Employer | Location | Start - End")
    each heading that names an employer from employment_history.md must carry that row's
    exact title of record and its start/end months -> any mismatch is a hard fail.

Exit status is 1 on any hard fail so it can gate a send. Numbers are skipped inside the
header block (before the first "## " heading), inside URLs, in years (1900-2099), and when
glued to a product or standard name (SOC 2, ISO 27001, Type II, Windows 11 ...); extend
IGNORE_BEFORE if your field has more. Numbers written as words ("six months") are not
parsed; keep figures as digits on documents you send, which is also better for ATS reading.
"""
import argparse
import os
import re
import sys

YEAR = re.compile(r"^(19|20)\d\d$")
NUM = re.compile(r"(?<![\w.])(\$?\d[\d,]*(?:\.\d+)?)\s?(%|[KkMmBb]\b|x\b|\+)?")
IGNORE_BEFORE = re.compile(
    r"(?:\b(?:SOC|ISO|IEC|PCI|NIST|CIS|HIPAA|Type|Tier|Level|Layer|Series|Version|v|Windows|"
    r"Office|Microsoft|M|O|Phase|Step|Round|Q|FY|H|Gen|Web|Wi-?Fi|802\.11\w*|Top|Page|Chapter)"
    r"\s?$)", re.I)
TARGET_WORDS = re.compile(
    r"\b(goal|goals|target|targeted|targeting|aim|aimed|aiming|intend|intended|plan to|planned to|"
    r"on track|projected|projection|forecast|expected to|anticipate|anticipated|hope to|slated)\b", re.I)
MONTHS = "Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec|January|February|March|April|June|July|August|September|October|November|December"
DATE = re.compile(rf"\b(?:{MONTHS})\.?\s+(?:19|20)\d\d\b|\bPresent\b|\bCurrent\b", re.I)


def norm_dash(s):
    return re.sub(r"[‐-―−]", "-", s)


def to_value(raw, suffix):
    v = float(raw.replace("$", "").replace(",", ""))
    if suffix:
        s = suffix.lower()
        v *= {"k": 1e3, "m": 1e6, "b": 1e9}.get(s, 1)
    return v


def numbers_in(text):
    """Yield (value, raw_token, line_no, line) for every standalone figure in text."""
    text = re.sub(r"https?://\S+|www\.\S+|\S+@\S+", " ", text)
    for ln, line in enumerate(text.split("\n"), 1):
        for m in NUM.finditer(line):
            raw, suf = m.group(1), m.group(2) or ""
            digits = raw.replace("$", "").replace(",", "")
            if YEAR.match(digits) and not suf and not raw.startswith("$"):
                continue
            before = line[:m.start()]
            if IGNORE_BEFORE.search(before[-12:]):
                continue
            if DATE.search(line[max(0, m.start() - 10):m.end() + 6]) and len(digits) == 4:
                continue
            if re.match(r"^\d{1,2}$", digits) and re.search(rf"(?:{MONTHS})\.? ?{digits}\b", line, re.I):
                continue  # day-of-month inside a date
            window = line[max(0, m.start() - 70):m.end() + 70]
            yield to_value(raw, suf if suf in "KkMmBb" and suf else ""), (raw + suf).strip(), ln, line.strip(), window


def body_of(doc_text):
    """The part of the document that will actually be sent.

    Resume: everything from the first '## ' heading on (skips the contact header).
    Letter or form answer with no '## ' headings: everything after the first '---' rule,
    so working notes kept above the rule are not scanned. No headings and no rule: all of it.
    """
    i = doc_text.find("\n## ")
    if i >= 0:
        return doc_text[i + 1:]
    m = re.search(r"^---\s*$", doc_text, re.M)
    return doc_text[m.end():] if m else doc_text


def skills_values(skills_text):
    """Map numeric value -> {'cleared': bool}. Cleared if any entry containing it is marked Yes."""
    entries = re.split(r"\n(?=\*\*Skill/Experience:\*\*)", skills_text)
    cleared, present = set(), set()
    for e in entries:
        m = re.search(r"\*\*Metrics Cleared:\*\*\s*([A-Za-z]+)", e)
        is_cleared = bool(m and m.group(1).lower().startswith("y"))
        for v, _raw, _ln, _line, _w in numbers_in(e):
            present.add(v)
            if is_cleared:
                cleared.add(v)
    # anything in prose outside entries (section intros, GAPS, notes) counts as present only
    return present, cleared


def history_rows(hist_text):
    rows = []
    for line in hist_text.split("\n"):
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 5 or not re.match(r"^\d+$", cells[0]):
            continue
        employer = re.sub(r"\*", "", cells[1])
        employer_key = norm_dash(employer).split(" - ")[0].split(" (")[0].strip()
        rows.append({"employer": employer_key, "title": re.sub(r"\*", "", cells[2]),
                     "start": cells[3], "end": cells[4], "raw": employer})
    return rows


def check_headings(doc_text, rows):
    fails, ok = [], []
    headings = [norm_dash(l[4:]).strip() for l in doc_text.split("\n") if l.startswith("### ")]
    matched = {}
    for h in headings:
        for r in rows:
            key = r["employer"].lower()
            short = key.replace(" inc.", "").replace(" inc", "").replace(",", "")
            if key in h.lower() or short in h.lower():
                matched.setdefault(h, []).append(r)
    for h, rs in matched.items():
        titles_ok = any(r["title"].lower() in h.lower() for r in rs)
        starts = [r["start"] for r in rs]
        ends = [r["end"] for r in rs]
        span_ok = any(s.lower() in h.lower() for s in starts) and any(e.lower() in h.lower() for e in ends)
        if len(rs) > 1:  # combined heading (e.g., two stints at one employer): accept the outer span
            span_ok = any(s.lower() in h.lower() for s in starts) and any(e.lower() in h.lower() for e in ends)
        problems, notes = [], []
        if not titles_ok:
            starts_with_employer = any(h.lower().startswith(r["employer"].lower()[:8]) for r in rs)
            if starts_with_employer:
                notes.append(f"no title in this heading (titles of record: {' / '.join(r['title'] for r in rs)}); make sure the body states them exactly")
            else:
                problems.append(f"title of record is '{' / '.join(r['title'] for r in rs)}'")
        if not span_ok:
            problems.append(f"dates of record are {', '.join(f'{r['start']} - {r['end']}' for r in rs)}")
        (fails if problems else ok).append((h, problems or notes))
    return fails, ok, headings


def fmt(v):
    return f"{v:,.0f}" if v == int(v) else f"{v:,}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("document")
    ap.add_argument("--skills", default="profile/master_skills.md")
    ap.add_argument("--history", default="profile/employment_history.md")
    a = ap.parse_args()

    doc = open(a.document, encoding="utf-8").read()
    hard = 0

    # ---- numbers
    print(f"== claims check: {a.document}")
    if not os.path.exists(a.skills):
        sys.exit(f"   ✗ truth anchor not found: {a.skills} (run from the repo root, or pass --skills)")
    present, cleared = skills_values(open(a.skills, encoding="utf-8").read())
    if not present:
        print(f"   ! {a.skills} contains no figures yet; every number below is MISSING until intake fills it")
    seen = set()
    missing = uncleared = anchored = 0
    for v, raw, ln, line, window in numbers_in(body_of(doc)):
        key = (v, raw)
        tag = "ANCHORED" if v in cleared else ("UNCLEARED" if v in present else "MISSING")
        if key not in seen:
            seen.add(key)
            if tag == "MISSING":
                missing += 1; hard += 1
                print(f"   ✗ MISSING   {raw:>10}  (line {ln}) {line[:90]}")
            elif tag == "UNCLEARED":
                uncleared += 1
                print(f"   · UNCLEARED {raw:>10}  (line {ln}) {line[:90]}")
            else:
                anchored += 1
        tw = TARGET_WORDS.search(window)
        if tw:
            print(f"   ! target language near {raw} (line {ln}): \"{tw.group(0)}\" -- a target is not an outcome")
    print(f"   numbers: {anchored} anchored, {uncleared} uncleared, {missing} missing")

    # ---- titles and dates
    if os.path.exists(a.history):
        rows = history_rows(open(a.history, encoding="utf-8").read())
        if rows:
            fails, ok, headings = check_headings(doc, rows)
            role_headings = [h for h in headings if DATE.search(h)]
            print(f"\n== titles/dates vs {a.history}: {len(ok)} headings match, {len(fails)} mismatch")
            for h, probs in fails:
                hard += 1
                print(f"   ✗ {h[:80]}\n       {'; '.join(probs)}")
            for h, notes in ok:
                if notes:
                    print(f"   ! {h[:80]}\n       {'; '.join(notes)}")
            unmatched = [h for h in role_headings if h not in dict(ok) and h not in dict(fails)]
            for h in unmatched:
                print(f"   ! heading names no employer in the history file: {h[:80]}")
        else:
            print(f"\n   ! {a.history} has no rows yet; title/date check skipped")
    else:
        print(f"\n   ! {a.history} not found; title/date check skipped")

    print("\n   RESULT:", "FAIL (do not send)" if hard else "PASS (mechanical checks only; the interview test still applies)")
    sys.exit(1 if hard else 0)


if __name__ == "__main__":
    main()
