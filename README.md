# Job Search OS

An operating system for a job search, built to run inside [Claude Code](https://claude.com/claude-code).
The point is a better job, not better documents: a five-check screening gate that kills bad
targets in minutes, one master resume with light tailoring, a pipeline with follow-up
clocks, a people ledger for warm introductions, and hard anti-fabrication rules that keep
every number on the resume defensible in an interview.

It is a template. The structure and rules come from running a real leadership-level search;
every personal value (comp floor, gaps, channels, voice) is a blank you fill during an intake
interview that the agent runs with you.

## What you get

| Piece | What it does |
|---|---|
| `CLAUDE.md` | The agent's operating manual: strategy, inviolable rules, screening gate, four-step application flow, seniority calibration, end-of-session protocol. Read it first. |
| `INTAKE.md` | The first-session interview that builds your truth layer (verified employment history, evidence-backed skills, comp floor, constraints, voice samples). Nothing works until this is done. |
| `profile/` | Your truth layer. Empty templates for the truth anchor, pipeline, contacts ledger, negotiation scripts, target roles. |
| `scripts/` | `render_resume.py` and `render_letter.py` (markdown to print-ready PDF through headless Chrome), `claims_check.py` (every number and every title/date in a document must trace to the truth layer; fails the send if not), `ats_check.py` (does the PDF's text layer survive extraction, JD keyword coverage, job-title alignment), `bullet_lint.py` (per-bullet rubric). Stdlib only. |
| `agents/` | Five specialist personas the orchestrator can spawn: resume builder, hiring-manager critic, metrics interrogator, editor, LinkedIn specialist. Field and level are set at intake. |
| `templates/` | Base resume, cover letter, LinkedIn profile, mock-interview protocol. |
| `examples/` | A complete fictional worked example (`morgan-hale/`) showing what intake and one application produce. |

## Start here

If you want to see what a populated system looks like before you begin, open
[`examples/morgan-hale/`](examples/morgan-hale/README.md): a fictional mid-level workplace-operations
search with a filled truth layer, gate, pipeline, contacts, and one tailored application,
including the real output of the four scripts.

1. **Use this repository as a template, and keep your copy private.** `profile/` and
   `applications/` will hold your employment history, compensation targets, and every
   application you send. Do not run this in a public fork.
2. Open the folder in Claude Code (CLI, desktop app, or IDE extension). Say:
   *"Read CLAUDE.md and INTAKE.md and let's begin intake."*
3. The agent runs Session Zero (tooling check) and then the intake interview. Expect more
   than one session. The screening gate stays blocked until `profile/target_roles.md`
   has a real compensation floor.

### Prerequisites

- Python 3.10+ (no packages to install)
- git
- Google Chrome or Chromium (the PDF renderer drives it headless; set `CHROME_PATH` if
  it is not in a standard location)
- poppler (`pdftotext`, `pdfinfo`) for page counts and the ATS check: `brew install poppler`
  on macOS, `apt install poppler-utils` on Debian/Ubuntu
- Optional: Microsoft Office, for the Aptos font the design spec uses. Without it the
  renderer falls back to Calibri, then Helvetica/Arial. The intake makes you check which
  font actually rendered so the fallback is a choice, not an accident.

Developed and tested on macOS. Linux should work with `CHROME_PATH` set; Windows is
untested.

## Why it looks the way it does

The short version is below. The long version, including the failure that produced the
rules, is in [`WHY_THESE_RULES.md`](WHY_THESE_RULES.md).

- **Screen hard, tailor lightly.** Most of the value is in not pursuing bad targets. The
  gate runs in under five minutes; tailoring is about fifteen.
- **One master resume.** Per-application rebuilds are how numbers drift and how unverifiable
  claims creep in, which is why Rules 1 through 4 exist. See
  [`WHY_THESE_RULES.md`](WHY_THESE_RULES.md) for how that failure actually happens.
- **People are pipeline rows.** Warm introductions convert far better than cold
  applications at every level, so every application carries a mandatory warm-path pass and
  every contact carries a follow-up clock.
- **Your voice, not the model's.** Hiring managers increasingly auto-reject prose that
  reads as AI-written. Outward text is drafted from your own writing samples, and the
  agent is told to reject its own default register.
- **Level is a variable.** A seniority calibration at intake sets page limit, channel
  ranking, and comp-research approach. The rules and the gate shape do not change.

## Setting it up for someone else

The repo is person-neutral. Copy it fresh (never copy a populated `profile/` or
`applications/` between people), fill the `[OWNER NAME]` line in `CLAUDE.md`, and run the
intake. Everything else is set during intake.

## License

MIT. See `LICENSE`.
