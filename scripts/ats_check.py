"""ATS text-layer verification for rendered resume PDFs.

    python3 scripts/ats_check.py <resume.pdf> [jd.md] ["Exact Job Title"]

Pattern credit: MadsLorentzen/ai-job-search. After rendering,
verify the PDF's text layer survives extraction the way an ATS would read it, and
(optionally) measure keyword coverage against the JD. This script REPORTS; the
orchestrator and the owner decide. It must never be used to justify stuffing a
keyword the truth anchor does not support.

Checks:
  1. pdftotext extraction succeeds and yields a sane amount of text
  2. Contact fields (email, phone) survive extraction
  3. No extraction artifacts: '(cid:', U+FFFD replacement chars, ligature loss
  4. Section headers present (Summary/Experience/Skills-shaped)
  5. With a JD file: top JD terms (unigrams + bigrams, stopword-filtered) and
     whether each appears in the resume text — coverage is INFORMATION, not a target
"""
import re
import subprocess
import sys
from collections import Counter

STOP = set("""a an and are as at be been but by can for from has have i in is it of on or our
that the their they this to was we were will with you your not no if than then so such via
who what when where which while our out over under more most other others across within
""".split())

JD_NOISE = set("""job role work team company employees experience years ability strong
excellent skills responsibilities requirements preferred plus benefits salary range
including etc apply candidates position location remote applicants application looking
""".split())


def extract(pdf):
    r = subprocess.run(["pdftotext", "-layout", pdf, "-"], capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"FAIL: pdftotext could not extract text ({r.stderr.strip()[:200]})")
    return r.stdout


def tokens(text):
    return re.findall(r"[a-z0-9][a-z0-9+#./-]*", text.lower())


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    pdf = sys.argv[1]
    jd_path = sys.argv[2] if len(sys.argv) > 2 else None

    text = extract(pdf)
    problems, notes = [], []

    # 1. Volume sanity
    words = tokens(text)
    if len(words) < 200:
        problems.append(f"only {len(words)} words extracted — text layer may be broken")
    else:
        notes.append(f"extraction OK: {len(words)} words")

    # 2. Contact fields
    if not re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text):
        problems.append("no email address survives extraction")
    if not re.search(r"\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}", text):
        problems.append("no phone number survives extraction")

    # 3. Artifacts
    if "(cid:" in text:
        problems.append("'(cid:' artifacts — font lacks a proper ToUnicode map")
    if "�" in text:
        problems.append("U+FFFD replacement characters in extracted text")
    for lig, plain in [("ﬁ", "fi"), ("ﬂ", "fl")]:
        if lig in text:
            notes.append(f"ligature {lig} present (most ATS handle it; verify '{plain}' words search correctly)")
    # missing-ligature heuristic: words that lost their fi/fl entirely
    for broken in ["certi cation", "con guration", "work ow", "identi ed", "bene ts"]:
        if broken in text.lower():
            problems.append(f"broken ligature: '{broken}' — fi/fl dropped during extraction")

    # 4. Section headers
    for header in ["summary", "experience", "skills"]:
        if not re.search(rf"^\s*(\w+\s+)?{header}", text, re.I | re.M):
            notes.append(f"section header '{header}' not found at line start (check parsing order)")

    print(f"== ATS text-layer check: {pdf}")
    for n in notes:
        print(f"   note: {n}")
    if problems:
        print("   PROBLEMS:")
        for p in problems:
            print(f"   ✗ {p}")
    else:
        print("   ✓ text layer extracts cleanly")

    # 5. Job-title alignment (title match is a heavy ATS ranking + recruiter-search signal)
    title = sys.argv[3] if len(sys.argv) > 3 else None
    if title:
        t_words = [w for w in tokens(title) if w not in STOP]
        head = " ".join(words[:150])  # summary/headline region
        full = " ".join(words)
        print(f"\n== Job-title alignment: \"{title}\"")
        if title.lower() in full:
            where = "in the summary region" if title.lower() in head else "later in the document"
            print(f"   ✓ exact title phrase present {where}")
        else:
            hits = [w for w in t_words if w in head]
            print(f"   · exact phrase absent; title words in summary region: {hits or 'NONE'}")
            print("   ^ echo the JD's title (or its nearest true equivalent) in the summary line —")
            print("     only where the truth anchor supports the seniority the title implies.")

    # 6. JD keyword coverage
    if jd_path:
        jd_text = open(jd_path, encoding="utf-8").read().lower()
        jd_toks = [t for t in tokens(jd_text) if t not in STOP and t not in JD_NOISE and len(t) > 2 and not t.isdigit()]
        uni = Counter(jd_toks)
        bi = Counter(f"{a} {b}" for a, b in zip(jd_toks, jd_toks[1:]))
        resume_lower = " ".join(words)
        print(f"\n== JD keyword coverage vs {jd_path} (information, not a stuffing target)")
        print("   -- top JD terms --")
        missing = []
        for term, count in (uni.most_common(20) + [x for x in bi.most_common(12) if x[1] >= 3]):
            present = term in resume_lower
            print(f"   {'✓' if present else '·'} {term}  (jd x{count})")
            if not present:
                missing.append(term)
        if missing:
            print(f"   absent from resume: {', '.join(missing)}")
            print("   ^ absence is only a problem if the truth anchor SUPPORTS the term and the resume merely words it differently.")


if __name__ == "__main__":
    main()
