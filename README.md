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
| `scripts/` | `render_resume.py` and `render_letter.py` (markdown to print-ready PDF through headless Chrome), `claims_check.py` (every number and every title/date in a document must trace to the truth layer; fails the send if not), `privacy_check.py` (is your copy actually private, is it a permanently-public fork, are credentials tracked), `ats_check.py` (does the PDF's text layer survive extraction, JD keyword coverage, job-title alignment), `bullet_lint.py` (per-bullet rubric). Stdlib only. |
| `agents/` | Five specialist personas the orchestrator can spawn: resume builder, hiring-manager critic, metrics interrogator, editor, LinkedIn specialist. Field and level are set at intake. |
| `templates/` | Base resume, cover letter, LinkedIn profile, mock-interview protocol. |
| `examples/` | A complete fictional worked example (`morgan-hale/`) showing what intake and one application produce. |

## Start here

**New to this, or to Claude Code? Read [SETUP.md](SETUP.md).** It covers what it costs, how to
make your own private copy, installing Claude Code in the terminal or the desktop app, and your
first session, written for someone who is not a developer.

The short version:

1. Click **Use this template** at the top of this page, then **Create a new repository**, and
   **select Private**. Do not fork: forks of public repositories are permanently public, and
   this one will hold your salary history and every application you send.
2. Get the folder onto your computer, then open it in Claude Code (terminal or the desktop
   app's Code tab, Environment set to Local).
3. Say: *"Read CLAUDE.md and INTAKE.md and let's begin intake."*

The agent runs an environment check, then the intake interview. Expect more than one session.
The screening gate stays blocked until `profile/target_roles.md` has a real compensation floor.

If you want to see what a populated system looks like first, open
[`examples/morgan-hale/`](examples/morgan-hale/README.md): a fictional mid-level
workplace-operations search with a filled truth layer, gate, pipeline, contacts, and one
tailored application, including the real output of the four scripts.

Claude Code requires a paid plan (Pro, Max, Team, Enterprise, or Console credits). The free
Claude.ai plan cannot run it.

### Prerequisites

A paid Claude plan, plus:

- Python 3.10+ (no packages to install)
- git
- Google Chrome or Chromium (the PDF renderer drives it headless; set `CHROME_PATH` if
  it is not in a standard location)
- poppler (`pdftotext`, `pdfinfo`) for page counts and the ATS check: `brew install poppler`
  on macOS, `apt install poppler-utils` on Debian/Ubuntu
- Optional: Microsoft Office, for the Aptos font the design spec uses. Without it the
  renderer falls back to Calibri, then Helvetica/Arial. The intake makes you check which
  font actually rendered so the fallback is a choice, not an accident.

Developed and tested on macOS. Linux should work with `CHROME_PATH` set. Windows is untested,
though Claude Code itself runs there; [SETUP.md](SETUP.md) covers the Windows install path.

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
