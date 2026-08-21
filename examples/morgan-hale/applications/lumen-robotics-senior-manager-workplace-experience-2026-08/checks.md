# Checks: real output of the four scripts against these files (run 2026-08-21 from the repo root)

```
$ python3 scripts/claims_check.py examples/morgan-hale/applications/lumen-robotics-senior-manager-workplace-experience-2026-08/resume_v1.md --skills examples/morgan-hale/profile/master_skills.md --history examples/morgan-hale/profile/employment_history.md
== claims check: examples/morgan-hale/applications/lumen-robotics-senior-manager-workplace-experience-2026-08/resume_v1.md
   · UNCLEARED          3  (line 3) Workplace operations leader with nine years across corporate and retail operations. Led a 
   · UNCLEARED        450  (line 12) - Logistics lead for the annual company offsite, 450 attendees on a $380K budget, delivere
   · UNCLEARED      $380K  (line 12) - Logistics lead for the annual company offsite, 450 attendees on a $380K budget, delivere
   · UNCLEARED         40  (line 17) - Designed and rolled out a standardized monthly inventory-count procedure to all 40 store
   numbers: 9 anchored, 4 uncleared, 0 missing

== titles/dates vs examples/morgan-hale/profile/employment_history.md: 4 headings match, 0 mismatch

   RESULT: PASS (mechanical checks only; the interview test still applies)
exit=0

$ python3 scripts/render_resume.py examples/morgan-hale/applications/lumen-robotics-senior-manager-workplace-experience-2026-08/resume_v1.md /tmp/morgan.pdf "Morgan Hale"
/tmp/morgan.pdf: Pages:           1

$ python3 scripts/ats_check.py /tmp/morgan.pdf examples/morgan-hale/applications/lumen-robotics-senior-manager-workplace-experience-2026-08/jd_verbatim.md "Senior Manager, Workplace Experience"
== ATS text-layer check: /tmp/morgan.pdf
   note: extraction OK: 306 words
   ✓ text layer extracts cleanly

== Job-title alignment: "Senior Manager, Workplace Experience"
   · exact phrase absent; title words in summary region: ['manager', 'workplace', 'experience']
   ^ echo the JD's title (or its nearest true equivalent) in the summary line,
     only where the truth anchor supports the seniority the title implies.

== JD keyword coverage vs examples/morgan-hale/applications/lumen-robotics-senior-manager-workplace-experience-2026-08/jd_verbatim.md (information, not a stuffing target)
   -- top JD terms --
   ✓ workplace  (jd x8)
   ✓ office  (jd x5)
   ✓ portland  (jd x4)
   ✓ hybrid  (jd x4)
   · people  (jd x3)
   ✓ two  (jd x3)
   ✓ offices  (jd x3)
   ✓ vendor  (jd x3)
   · lumen  (jd x2)
   · robotics  (jd x2)
   ✓ days  (jd x2)
   ✓ week  (jd x2)
   · austin  (jd x2)
   ✓ own  (jd x2)
   ✓ end  (jd x2)
   ✓ space  (jd x2)
   ✓ planning  (jd x2)
   ✓ management  (jd x2)
   ✓ programs  (jd x2)
   ✓ events  (jd x2)
   absent from resume: people, lumen, robotics, austin
   ^ absence is only a problem if the truth anchor SUPPORTS the term and the resume merely words it differently.

$ python3 scripts/bullet_lint.py examples/morgan-hale/applications/lumen-robotics-senior-manager-workplace-experience-2026-08/resume_v1.md
== bullet lint: examples/morgan-hale/applications/lumen-robotics-senior-manager-workplace-experience-2026-08/resume_v1.md (9 bullets)
  [8] Supported store-opening logistics and vendor scheduling for the Portla...
      · weak opener 'supported'
  [9] Front-of-house and events for a coworking space; first exposure to spa...
      · no metric/number (fine if the bullet is scope, not outcome)
```

## How to read this

- **claims_check:** 9 figures ANCHORED in cleared entries. The 4 UNCLEARED figures (team of 3,
  450 attendees, $380K budget, 40 stores) live in anchor entries that deliberately claim no
  outcome metric; they are scale facts, and the tool is asking you to confirm that, not
  rejecting them. 0 MISSING is the bar. Titles and dates: all four headings match the
  history file, including the promotion recorded as two rows.
- **render:** 1 page, the calibration limit for this level. Check the font actually embedded
  (`pdffonts`), not just the page count.
- **ats_check:** clean extraction. The exact JD title is absent from the summary; the title
  words are present. Morgan's summary says "own a multi-office workplace function" rather
  than echoing "Senior Manager, Workplace Experience" because the anchor supports the scope,
  not the title she has never held. That is the right call, and the tool reports it as
  information. "people / lumen / robotics / austin" absent: company names and a city she has
  no connection to. Ignore.
- **bullet_lint:** "Supported" is a weak opener on the coordinator bullet. Left in on purpose
  so you can see the flag; in a real pass you would either rewrite it ("Coordinated
  store-opening logistics...") or accept it because it is an early-career line doing scope
  duty. The last bullet has no number and is fine: it is context, not an outcome.
