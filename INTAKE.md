# INTAKE: The First Session

**Purpose:** build the truth layer. Nothing else in this system works until this exists.
Expect this to take more than one session; that is normal. Run it as an interview plus
document reading, not as a form. "The owner" below is the person whose search this is.

Before starting, the owner and the agent should both skim `examples/morgan-hale/` once: it
shows what every file below looks like when finished, including how a cleared metric, a
soft metric, and a removed claim are written.

## Session Zero: Environment Check

**Do not let this block intake.** The interview below needs nothing installed. Tooling is only
needed at the end, when the first resume gets rendered. If a download is slow or a connection
is bad, note what is missing, start the interview, and come back to this.

Run `python3 scripts/setup_check.py`. It reports what is present, what is missing, the exact
command to fix each one, and how long each takes. Then use this table to decide what actually
blocks you today:

| To do this | You need |
|---|---|
| The whole intake interview | nothing |
| Render a resume or cover letter to PDF | Python 3.10+ and Google Chrome |
| Automatic page count after rendering | plus poppler |
| `ats_check.py` | plus poppler |
| Commit history and undo | plus git |

**On a Mac, git comes from the Xcode Command Line Tools**, and that download is large. A Mac
that has never installed them does not really have git, only a stub that triggers the install,
which is why guidance saying "most Macs include git" can mislead. The installer dialog is not
resumable and its time estimate is often wrong; on a weak connection it can claim hours. If
that happens: cancel it, carry on with intake, and install later from
https://developer.apple.com/download/all (search "Command Line Tools", free Apple ID), which
gives a resumable .dmg.

**If the Claude desktop app refuses to open a local session without git**, use the terminal
version instead: `curl -fsSL https://claude.ai/install.sh | bash`, then `cd` into this folder
and run `claude`. Anthropic's setup documentation lists no git requirement for the CLI; the
documented requirement is for the desktop app on Windows. If `python3` is missing too, install
Python from https://www.python.org/downloads/ rather than waiting on Xcode.

Homebrew is only needed to install poppler. You do not need MacPorts. Pick one, and these
instructions assume Homebrew.

Two things `setup_check.py` cannot decide for you:

1. **Private repository, if you used one.** Run `python3 scripts/privacy_check.py`. It verifies
   the remote is private, catches the permanently-public fork case, and looks for tracked
   credentials. **Do not put real career data in a repository that fails this.** If you
   downloaded the ZIP and never touched GitHub, there is nothing to expose.
2. **Fonts.** The design spec is Aptos, which ships with Microsoft Word. Without it the render
   silently falls back to Calibri, then Helvetica or Arial. Check which font actually rendered
   in the test PDF below. A fallback is a fine choice; a silent one is not.

**End-to-end test, once the tooling is in place:** render `templates/base_resume.md` through
`scripts/render_resume.py`, open the PDF, check the font and layout. Then run
`scripts/ats_check.py` on it. The placeholder template will report missing contact fields;
that is expected. `scripts/claims_check.py templates/base_resume.md` should FAIL loudly on the
placeholder numbers; that is the gate working.

**Claude Code setup:** a local session (CLI, desktop app, or IDE extension) opened on this
folder, under the owner's own account and OS user. See `SETUP.md`.

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
