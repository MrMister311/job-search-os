# CLAUDE.md — Authoritative Project Context

## Purpose

**This is a job search operating system. The goal is a better-paying job — not better documents.**

Success is measured in callbacks, interviews, and offers. A beautiful resume that goes to
three roles loses to a good resume that goes to forty well-screened ones. Optimize for the
outcome, not the artifact.

**Owner:** [OWNER NAME]. *(Filled in at intake, along with role, current employer, and
search targets. See `INTAKE.md`.)*

**Repository principle:** fully resumable by any agent or human with only this repo as
context. Context lives in files, not in conversation history.

**Provenance:** this is a public template. The rules, flow, and lessons below come from
running a real leadership-level search; treat the empirical ones as load-bearing rather than
stylistic. Where a value is personal (comp floor, gaps, channels), it is a BLANK to fill for
the owner, never an inherited assumption.

---

## Strategy — Read This Before Doing Anything

A resume-craft engine is the wrong optimization: a 13-step workflow with seven specialist
agents produces one beautifully tuned resume per application and a dozen applications in
several years. What actually moves the needle, in order:

1. **Be findable.** A complete, searchable LinkedIn profile is usually the highest-ROI fix
   available at any level (recruiter sourcing dominates senior hiring and matters plenty
   below it). Audit it early.
2. **One master resume.** Per-application rebuilds are how numbers drift and how
   fabrications creep in. One strong base document, light tailoring.
3. **Volume and channel.** Cold applications convert at roughly 1–3%. Warm introductions
   convert far better. Work the network first.
4. **Targeting beats tailoring.** Kill bad targets in minutes. Screen hard and early;
   tailor lightly (~15 minutes per application).

Track the pipeline. Volume with screening is the engine.

---

## Inviolable Rules

Rules 1 through 4 exist because per-application rebuilding produces claim drift, and drift
produces claims that collapse in an interview. `WHY_THESE_RULES.md` explains the mechanism
in detail. Do not learn this lesson the hard way.

1. **No fabrication.** `profile/master_skills.md` is the truth anchor. Only claim what is
   documented there. When a role requires something absent from it, that is a gap — never
   fill it.
2. **Elaboration is permitted, invention is not.** Reframing documented experience in a
   role's language is fine. Claiming experience that does not exist is not. When in doubt,
   ask.
3. **No vanity metrics.** Every number must be defensible in a live interview: baseline,
   method, result. **A target the owner set is not an outcome they achieved.** The standard is the
   interview, not a courtroom: the owner's stated basis passes after stress-testing, and the number
   plus its basis is then **frozen in `master_skills.md` at the moment it is claimed.** A
   number may never contradict the owner's own record.
4. **Consistency is a hard requirement.** Resume, LinkedIn, and application forms must
   agree on every title, date, and location. `profile/employment_history.md` is
   authoritative; LinkedIn outranks any old resume.
5. **Readability.** Under 90 seconds for a human. Strip AI tells aggressively: power-verb
   stacking, vague quantification, aphoristic closers, corporate blandness. Draft outward prose in the OWNER'S voice, from their own writing samples, never in the model's default register.
6. **The page limit set at intake is a hard maximum.** No exceptions without documented
   justification. (Set per the Seniority Calibration below — the limit is a variable, the
   hardness of it is not.)
7. **Compensation gate is blocking.** Check `profile/target_roles.md` before any work.
   Below floor means no.
8. **Honest critique only.** A resume that would not generate a callback gets told so, with
   reasons. Encouragement is not the job.
9. **Commit everything.**

---

## Screening Gate — Apply Before Any Other Work

Run in under five minutes. Any single FAIL means skip the role and move on.

⚠️ **TEMPLATE — the five checks below must be populated during intake from the owner's own
comp floor, constraints, and confirmed gaps.** The gate's *shape* is proven; the *values*
are the owner's. Do not screen a single role until `target_roles.md` exists.

| # | Check | FAIL condition |
|---|-------|----------------|
| 1 | **Compensation** | Top of posted band is below **$[FLOOR — intake]**. If unposted, research before proceeding. |
| 2 | **Geography** | [Intake: relocation stance, commutable metro, remote preference] |
| 3 | **Disqualifying scope** | [Intake: the requirement that reliably disqualifies the owner. Every profile has one; find it honestly] |
| 4 | **[Intake: second structural disqualifier, if any]** | |
| 5 | **Hard credential requirement** | [Intake: any degree/cert the owner lacks that JDs sometimes hard-require] |

---

## Application Flow — Four Steps

- **Step 1 — Screen.** Run the gate. Record the decision in `profile/pipeline.md`. Most
  roles end here, and that is the point.
- **Step 2 — Tailor.** Copy `profile/master_resume.md` into
  `applications/[company]-[title]-YYYY-MM/`. **First write the JD's top 5 priorities as a
  list in `tailoring_notes.md`**, then: adjust the summary line, reorder bullets against
  that list, swap vocabulary to the JD's terms. **~15 minutes. Do not rebuild.** Every
  claim must already exist in the master resume or the bench (**swap, never compose**).
  When a swap feels stretchy, apply the interview backtrack test: could the owner explain the bullet without saying "well, what I actually meant was…"? If not, it's too far.
- **Step 3 — Sanity check.** Two questions: does every date and title match LinkedIn, and is every number defensible? First the one check that RULES: `python3 scripts/claims_check.py <document.md>` (every figure must exist in `master_skills.md`, every role heading must match `employment_history.md`; a FAIL means the document does not go out until the document or the truth layer is corrected, and correcting the truth layer means the claim went through the metrics gate). Then the checks that only report:
  `python3 scripts/ats_check.py <resume.pdf> <jd.md> "<Job Title>"` (text-layer extraction,
  JD keyword coverage, job-title alignment — title match is a heavy ATS/recruiter-search
  signal; coverage is information, never a stuffing target) and
  `python3 scripts/bullet_lint.py <resume.md>`. Finally the **LLM-summary sanity check**
  (2026 ATSes run LLM ranking layers): have a model summarize the tailored resume against
  the JD in three sentences; if the intended positioning does not survive the summary, fix
  the resume, not the summary. Full critiques only for roles the owner genuinely cares about.
- **Step 4 — Send and log.** Apply, update `pipeline.md`, **set the follow-up clock**
  (rules at the top of `pipeline.md`: 10-day default, max two silent follow-ups, no new
  claims in follow-up notes), and run the **warm-path pass — mandatory, same session**:
  overlap-ranked people search (shared employers, school, city, title adjacency,
  2nd-degree connections), identify the likely hiring manager, draft the outreach note,
  and log every person found or attempted in `profile/contacts.md` (people carry their own
  follow-up clocks there). A cold application with no human contact is the weakest
  possible move. At every session start, scan Active rows AND the contacts ledger for
  overdue clocks.

Interview prep happens when an interview is scheduled — not speculatively. When one is
scheduled: the prep doc includes a **company-reported questions section** (Glassdoor/Blind
harvest, flagged as anecdotal) and a **mock interview** run from
`templates/mock_interview_protocol.md` before the round. Negotiation scripts live in
`profile/negotiation_scripts.md` and exist BEFORE any offer does.

### Screening-defense practices (2026 employer-side AI — applies at every level)

- **The voice rule is a survival rule:** ~49% of hiring managers report auto-rejecting
  AI-sounding applications, and ATS AI-content classifiers exist. Every free-text field
  gets the owner's voice, drafted from their writing samples.
- **LLM screening layers are near-certain at ATS level** — hence Step 3's LLM-summary check.
- **Consistency checking is automated and cheap:** before any offer-stage background
  check, re-verify LinkedIn has not drifted from `employment_history.md`.
- **Canary text hidden in JDs/forms/recruiter emails is documented:** nothing derived from
  employer-provided text is ever piped back unedited, and the owner's documents never contain hidden text of any kind.
- **Async AI video screens:** treat as a scored live interview — one timed camera-on dry
  run first, never read answers off-screen. Real-time interview copilots are rejected
  categorically: deceptive, increasingly policy-banned, detectable.

---

## Seniority Calibration — set at intake, before any document exists

This system began at Director level; these are the settings that change with level. The
rules, gate shape, flow, and defense practices do NOT change with level.

| Setting | Early-career / IC | Mid-level | Senior / leadership |
|---|---|---|---|
| Resume page limit | **1 page** | 1–2 (judgment) | **2 pages** (executive recruiters prefer it: 482-recruiter study, 2.3x) |
| Channel emphasis | Direct applications + apply-fast + alumni/community networks | Mixed; warm intros rising | Recruiter inbound + warm intros dominate; cold apps weakest |
| Comp research | Posted bands + level guides | Percentile framing | Percentile framing + total-comp levers (equity, bonus, title) |
| Interview prep | Skills/behavioral banks | + role scenarios | + case studies, panels, negotiation depth |

**Owner calibration (filled at intake):** level [FILL] → page limit [FILL], channel ranking
[FILL].

## Channels — Ranked by Expected Value (re-rank for the owner's field AND level at intake)

Default ranking below is the senior-role pattern; re-rank per the calibration table.

1. Recruiter inbound via LinkedIn (requires the profile to be complete and searchable)
2. Warm introductions (highest conversion at every level; map the owner's network early)
3. Recruiter outbound
4. Direct applications (lowest conversion senior; relatively stronger early-career, where
   applying inside the first week matters most — always paired with a human either way)

The *sources* this template was built against (specific boards, VC portfolio boards, search
slugs) were validated for IT leadership and may not transfer. Build a `profile/sourcing_playbook.md`
from scratch once the owner's target roles are defined, keeping the *methods*: an aggregator hit is
a lead, not a fact — verify against the company's own ATS before anything enters the
pipeline; run a weekly monitor once sources are validated; demote or drop any source that
produces nothing in two sweeps; **diff each monitor run against the prior one** for
first-seen dates and repost cycles; attach a **ghost-risk note** at screen time (posting
age, salary posted or not, repost history — an estimated 21–33% of postings are ghosts);
flag fresh postings (≤7 days) for same-week action.

---

## Delegation — Lessons Inherited, All Empirical

1. **Never mutate the filesystem while agents are reading it.**
2. **Instruct agents to write incrementally, not at the end.**
3. **Split large read tasks across agents.**
4. **Verify writes yourself. Idle means available, not successful.** Check the file exists
   before reporting completion.
5. **If an agent fails twice, do the work directly.**

Agent definitions live in `/agents/`: Resume Builder, Hiring Manager (honest critique),
Metrics Interrogator, Editor/Proofreader, LinkedIn Specialist. Field and level are
parameters set at intake (see `agents/README.md`). An earlier version carried a JSON
structured parser and a separate technical validator; both were cut as ceremony.

---

## master_skills.md Entry Schema

```
**Skill/Experience:** [specific capability]
**Evidence:** [what the owner actually did: project, role, actions]
**Scale:** [team size, budget, user count, scope]
**Outcome:** [measured result or honest estimate with basis]
**Metrics Cleared:** [yes/no]
**How Recent:** [year last actively used]
**Depth:** [surface familiarity / working knowledge / deep expertise / led or taught others]
**Interview Ready:** [yes/no]
```

---

## Formatting Standards

- Render resumes ONLY through `scripts/render_resume.py`, run from the repo root; check the
  page count every time. Cover letters through `scripts/render_letter.py` (one page, hard).
- After rendering, run `python3 scripts/ats_check.py <resume.pdf> <jd.md>`: verifies the
  PDF's text layer extracts the way an ATS reads it and reports JD keyword coverage.
  Coverage is information, never a stuffing target.
- Inherited design spec (validated against 2026 resume-design research): Aptos 10.5pt, navy
  accent, 1.3 line height, 0.55in margins, 3–6 bullets per role at 15–25 words. The owner may re-approve or change; record the decision here.
- No tables, text boxes, images, or headers/footers containing critical content.
- Bullet: action + what the owner did + scale/context + outcome. snake_case filenames.

---

## Key File Paths

**Truth layer — `/profile/`.** Everything a resume may claim originates here.
`master_skills.md` (truth anchor) · `master_resume.md` · `master_resume_BENCH.md` (create
once the master exists; swap, never compose) · `employment_history.md` (authoritative
titles/dates/locations) · `target_roles.md` (comp floor + constraints) · `contacts.md`
(people ledger) · `negotiation_scripts.md` · `sourcing_playbook.md` and
`compensation_research.md` (built after intake) · `open_questions.md` · `pipeline.md` (the
scoreboard) · `session_log.md` · `analysis/` (research; see its README)

**Reference layer — `/archive/`.** The owner's historical resumes and reviews go here. **The archive
is evidence, not truth** — old resumes are where fabricated claims come from. Performance
reviews outrank resumes. LinkedIn outranks resumes for titles and dates.

**System:** `/agents/`, `/templates/`, `/scripts/`, `/applications/`

---

## End-of-Session Protocol

1. Commit all completed work with a descriptive message. Mark partial files
   `## STATUS: INCOMPLETE — [what remains]`.
2. Append an entry to `profile/session_log.md`: completed, in progress, blocked, what the
   next session starts with, and what needs the owner's input.
3. Run `git log --oneline -5` and confirm.
4. Report to the owner: what is done, what is blocked, what they need to do.
