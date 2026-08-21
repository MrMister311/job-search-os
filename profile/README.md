# profile/ : your truth layer

Everything a resume, letter, or application form may claim originates in this directory.
Nothing here is filled in yet. Intake fills it.

## What exists now (empty templates, ready to populate)

| File | What goes in it | When |
|---|---|---|
| `master_skills.md` | The truth anchor. One entry per capability: evidence, scale, outcome, whether the number is cleared. Every claim anywhere traces back here | Intake step 2 |
| `employment_history.md` | Authoritative titles, dates, employers, locations. The file everything else must agree with | Intake step 1 |
| `target_roles.md` | Compensation floor, geography constraints, titles in scope. **The screening gate is blocked until this has a real number** | Intake step 4 |
| `pipeline.md` | Every role screened, applied to, and its outcome. The scoreboard | First screen |
| `contacts.md` | People, with their own follow-up clocks. The warm-introduction channel's record | Intake step 7 |
| `negotiation_scripts.md` | What to say about money. Personalize before the first recruiter call | Intake step 8 |
| `open_questions.md` | Anything unresolved that blocks or degrades work | Ongoing |
| `session_log.md` | One entry per session: done, in progress, blocked, what is next | Every session |
| `claims_ignore.txt` | Tuning for `claims_check.py`. Read the warning at the top before using it | As needed |
| `analysis/` | Research outputs. Reference material, never the truth layer | As needed |

## What gets created later (do not go looking for these)

CLAUDE.md and INTAKE.md mention these by name. They do not exist yet, and that is correct.

| File | Created when |
|---|---|
| `master_resume.md` | End of intake, once the truth anchor can support it |
| `master_resume_BENCH.md` | After the master resume, as pre-vetted alternate bullets. Swap from it, never compose fresh |
| `sourcing_playbook.md` | Intake step 6, after channel research |
| `compensation_research.md` | Intake step 4 or 8, when comp research happens |
| `analysis/voice_samples.md` | Intake, as writing samples are collected |
| `tailoring_notes.md` | Per application, inside `applications/[company]-[title]-YYYY-MM/` |

## The one rule that matters here

If a claim is not in `master_skills.md`, it does not go in a document. When a posting asks for
something this directory cannot support, that is a gap to screen around, not a gap to write
around.
