# Worked example: Morgan Hale (fictional)

**Everything in this folder is invented.** Morgan Hale, the employers, the job postings, the
people in the contacts ledger, the numbers: all fictional, written to show what a populated
system looks like after intake and one application. No real person or company is depicted.

Why it exists: the template's rules are easy to read and hard to picture. This folder is the
picture. It is deliberately **mid-level and non-technical** (workplace operations, nine years
in, targeting a senior manager seat) so you can see the seniority calibration land somewhere
other than a Director-level search.

## What to look at, in order

1. `CALIBRATION_AND_GATE.md`: the seniority calibration choices and the five-check gate with
   real values in every row. This is what the end of intake produces in `CLAUDE.md`.
2. `profile/employment_history.md`: the authoritative titles and dates. Note the promotion
   recorded as two rows.
3. `profile/master_skills.md`: the truth anchor. Six entries. Look at how a **cleared** metric
   carries its basis, how a **[SOFT METRIC]** is kept but fenced, and how a **removed claim**
   is struck through and kept rather than deleted.
4. `profile/master_resume.md`: one page, every figure traceable to the anchor.
5. `profile/target_roles.md`, `profile/pipeline.md`, `profile/contacts.md`: one role that
   passed the gate and was applied to, one screened out with the reason, one closed, and the
   people attached to them, each with a clock.
6. `applications/lumen-robotics-.../`: the 15-minute tailor. `tailoring_notes.md` starts with
   the JD's top-5 priorities and lists exactly three swaps. `checks.md` is the real output of
   the four scripts run against these files.
7. `profile/session_log.md`: what an end-of-session entry looks like.

## Run the checks yourself

From the repository root:

```
python3 scripts/claims_check.py examples/morgan-hale/profile/master_resume.md \
    --skills examples/morgan-hale/profile/master_skills.md \
    --history examples/morgan-hale/profile/employment_history.md
python3 scripts/render_resume.py examples/morgan-hale/profile/master_resume.md /tmp/morgan.pdf "Morgan Hale"
python3 scripts/ats_check.py /tmp/morgan.pdf examples/morgan-hale/applications/lumen-robotics-senior-manager-workplace-experience-2026-08/jd_verbatim.md "Senior Manager, Workplace Experience"
python3 scripts/bullet_lint.py examples/morgan-hale/profile/master_resume.md
```
