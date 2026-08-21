# INTAKE: The First Session

**Purpose:** build the truth layer. Nothing else in this system works until this exists.
Expect this to take more than one session; that is normal. Run it as an interview plus
document reading, not as a form. "The owner" below is the person whose search this is.

Before starting, the owner and the agent should both skim `examples/morgan-hale/` once: it
shows what every file below looks like when finished, including how a cleared metric, a
soft metric, and a removed claim are written.

## Session Zero: Environment Check (run BEFORE any career content)

The tooling must be proven working on the owner's machine before intake begins, so the
first render isn't debugged under application-deadline pressure. Run each check and fix
failures as they appear:

1. **Python 3**: `python3 --version` (3.10+; the scripts are stdlib-only, no pip installs).
   On a fresh Mac this may prompt to install Command Line Tools; accept.
2. **git**: `git --version`, then confirm identity: `git config user.name` and
   `git config user.email`. Set them to the owner's name and personal email if empty.
   Commits should be theirs, from a personal account, never a work one.
3. **Private repository.** This folder will hold employment history, compensation targets,
   and every application sent. Run `python3 scripts/privacy_check.py`. It verifies the remote
   is private, catches the permanently-public fork case, and looks for tracked credentials.
   **Do not proceed past this step on a FAIL.** If the owner forked rather than using the
   template button, the copy cannot be made private and must be recreated; see `SETUP.md`.
4. **Google Chrome or Chromium**: the PDF renderer drives it headless. If the browser is
   not in a standard location, set `CHROME_PATH` to the binary.
5. **poppler** (`pdfinfo` + `pdftotext`, used for page counts and the ATS check):
   `pdftotext -v`. If missing: `brew install poppler` (macOS) or
   `apt install poppler-utils` (Debian/Ubuntu).
6. **Fonts**: the design spec is Aptos, which the renderer loads from Microsoft Word's
   app bundle on macOS (or from `APTOS_DIR` if set). If Word is not installed, the render
   silently falls back (Calibri → Helvetica Neue → Arial). **Check which font actually
   rendered** in the test PDF below; if it fell back, either install Office, source Aptos
   another way, or consciously re-approve the fallback as the owner's design choice.
   Never let the font change silently.
7. **End-to-end render test**: render `templates/base_resume.md` through
   `scripts/render_resume.py` from the repo root, confirm a PDF appears with a page count
   printed, open it, and check the font and layout. Then run `scripts/ats_check.py` on the
   test PDF to confirm extraction works (the placeholder template will report missing contact fields; that is expected). `scripts/claims_check.py templates/base_resume.md` should FAIL loudly on the placeholder numbers; that is the gate working.
8. **Claude Code setup**: a local session (CLI, desktop app, or IDE extension) opened on
   this folder, under the owner's own account and OS user.
9. **Optional**: the Claude in Chrome extension, only if the sourcing playbook ends up
   using browser-only job boards (some are invisible to plain fetching). Defer until
   channel research says it's needed.

Session Zero is done when a test PDF rendered in the intended font, the checks all pass,
and the repo has the owner's git identity on a first commit.

## What is in profile/ before you begin

Read `profile/README.md` once. It lists which files exist now and which get created during
intake, so neither the owner nor the agent goes looking for something that is not supposed
to be there yet.

## Before starting, the owner gathers

- Every old resume they can find (they go in `/archive/`, and they are *evidence, not truth*)
- Performance reviews, promotion letters, any manager-written assessment (these outrank
  resumes as evidence)
- Their LinkedIn profile as it stands today
- A rough sense of the target: role titles, minimum compensation, geography constraints

## The interview, in order

0. **Seniority calibration** (CLAUDE.md's calibration table): the owner's level sets the
   resume page limit, the channel ranking, and the comp-research approach. Record the
   choices in CLAUDE.md's "Owner calibration" line. This template began at Director level;
   do not let senior-role defaults leak into a search at a different level.
1. **Employment history first** (`profile/employment_history.md`): every employer, exact
   title of record, start/end months, location. Cross-check against LinkedIn and flag every
   disagreement now. This file becomes authoritative.
2. **Skills and accomplishments** (`profile/master_skills.md`, one entry per skill using the
   schema in CLAUDE.md): for every claim, ask for the evidence, the scale, and the outcome.
   **Interrogate every number**: what was the baseline, how was it measured, can the owner
   walk it in an interview? Numbers that pass get frozen with their basis. Numbers that
   don't get recorded as [SOFT METRIC] or excluded. Do not soften this step; it is the
   reason the system works.
3. **Gaps, honestly**: what do target JDs ask for that the owner does not have? Record them
   in master_skills under a GAPS section. Gaps are screened around, never written around.
4. **Target definition** (`profile/target_roles.md`): compensation floor (a number),
   geography constraints (absolute vs preference), role titles in scope, and anything the
   owner will not do. Then populate the five-check screening gate in CLAUDE.md from this
   file.
5. **LinkedIn audit**: completeness, headline, whether the Experience section supports
   recruiter title-search. Usually the highest-ROI early fix.
6. **Channel research**: where do the target roles actually get filled? **Start by asking
   the owner**: which job boards, niche sites, newsletters, communities, staffing agencies,
   or company careers pages do they already use, trust, or want included? Their field
   almost certainly has niche sources no generic sweep would find, and they are the best
   lead on them. Everything they name enters `profile/sourcing_playbook.md` as a candidate
   on equal footing with agent-discovered sources, and every source, theirs included,
   passes the same validation before it is trusted: test it, verify a sample hit against
   the company's own ATS, and demote or drop anything that produces nothing in two sweeps.
   Sources can be added the same way at any point after intake.
7. **Network mapping**: seed `profile/contacts.md` prospect pools (alumni networks, past
   employers, communities). The warm-path pass in Step 4 draws from this from day one.
8. **Negotiation prep**: personalize `profile/negotiation_scripts.md` from the owner's comp
   research and voice-pass it with them. It must exist before the first offer, and ideally
   before the first recruiter call asks the expectations question.
9. **Cover-letter voice exercise**: draft ONE sample cover letter with the owner during
   intake, against a real posting they like (no need to send it). Iterate until they say
   it sounds like them, then keep it as the voice reference for every future letter.
   Calibrating voice once, calmly, beats calibrating it against an application deadline,
   and first drafts almost always read as AI-written until real samples are in hand.

## Voice (matters more than it looks)

Collect samples of the owner's own writing early (self-assessments, emails they are proud
of, anything in their natural register) and keep them in `profile/analysis/voice_samples.md`.
Every outward document gets drafted against those samples, in their voice. The origin
system's rule is that AI-register prose (aphoristic closers, mirrored pivots, too-perfect
symmetry) reads as inauthentic to human readers, and the fix is drafting from the person's
real writing rather than polishing the model's. The loop that works best: the owner dictates
rough, the agent fact-checks against the truth anchor and tidies. Automated voice-cloning
tools were evaluated for this system and dropped; they rewrite facts while rewriting prose.

## Exit criteria

Intake is done when: employment_history is verified against LinkedIn, master_skills has
interview-ready entries covering the owner's main claims with numbers gated, target_roles
has a real comp floor, the screening gate in CLAUDE.md has values in every row, and a first
`master_resume.md` draft exists that contains nothing unanchored. Then delete this file's
checklist status below and start screening roles.

## STATUS: NOT STARTED
