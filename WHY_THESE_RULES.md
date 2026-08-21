# Why these rules exist

The rules in `CLAUDE.md` are stricter than most resume advice. This file explains the failure
mode they exist to prevent, because the rules look like bureaucracy until you have seen how
the failure actually happens.

It does not happen the way people imagine. Nobody sits down and decides to lie on a resume.

## The rebuild loop

Most people handle applications the same way. Find a posting, open the most recent resume,
rebuild it for this role. Do that for a few years and you have thirty or forty versions, and
no two of them agree.

That is the mechanism. Each rebuild starts from whichever version was nearest to hand, and
each rebuild nudges something: a word, a range, an emphasis. No single step is a decision.
The drift is the sum of a hundred small edits nobody remembers making.

An AI assistant makes the rebuild faster, which makes the drift faster. Ask a model to
"strengthen" a bullet and it will, every time. It has no way to know which strengthening
crosses the line from wording into fact, because it cannot see the underlying truth. It only
sees the previous version of the sentence.

## The five shapes drift takes

If you audit a stack of your own old resumes against evidence you can actually verify, these
are the patterns you will find. They are worth knowing by name, because you will recognize
them mid-edit once you can name them.

- **Labels creep upward.** A Manager title gets described with a word that sits slightly
  above Manager. A Director's scope gets called "Executive Director" in a body line. Each
  version is defensible on its own as framing. In sequence, they describe a different career.
- **Facts migrate between employers.** A "first hire on the team" story that is true at one
  company gets borrowed onto another where it is not. A tool you owned at one job appears on
  the entry for the job before it.
- **Dates lose precision, then move.** Month-level dates collapse to bare years, which
  quietly erases employment gaps. Then a year shifts by one and nobody notices, because
  there is no file that says what the real one was.
- **Soft outcomes become percentages.** This is the fastest and most dangerous one, and an AI
  rebuild can do it in a single pass. "Improved response times" becomes "reduced response
  times by 40%." Nothing was measured. There was no baseline. The number appeared because
  the format wanted a number.
- **Old resumes become evidence for new ones.** When you want to check a claim, you check an
  earlier resume, because that is what is in front of you. That is not checking. That is
  copying with extra steps, and it launders an invention into a fact after two or three
  hops.

The person doing this is not dishonest. They are working from the wrong source document.

## Why it matters more than it used to

A claim that drifted is a claim you cannot walk in an interview. Asked for the baseline and
the method behind a number you did not calculate, there is no good answer, and the interviewer
can hear it.

Employers also check now. Automated consistency checking between a resume, a LinkedIn
profile, and an application form is cheap and increasingly standard, and some job postings say
so in the text. A title that disagrees with your own LinkedIn is not a rounding error to a
background-check vendor.

## What each rule does about it

**One truth file, and every document derives from it.** `master_skills.md` holds every claim
with its evidence, scale, and outcome. A resume can reword what is there. It cannot add. When
a posting asks for something the file does not contain, that is a gap to screen around, and
the answer is not to apply rather than to write around it.

**Numbers are frozen with their basis at the moment they are claimed.** The test is not
whether you have a receipt in a drawer. The test is whether you can walk the baseline, the
method, and the result out loud to someone paid to be skeptical. If you can, the number and
its basis get written down right then, and that frozen form is the only version that ever
appears again. If you cannot, it does not appear. A target you set is never written as a
result you achieved.

**The archive is evidence, not truth.** Old resumes live in a folder the system is told to
distrust. Performance reviews, written by someone else, outrank them. LinkedIn outranks them
for titles and dates, because it is the version a background check will see.

**Consistency is a hard requirement, not a nicety.** Resume, LinkedIn, and every application
form agree on every title, date, and location, and `employment_history.md` is the one file
they agree with.

**One master resume, tailored lightly.** Fifteen minutes of reordering and vocabulary swaps
against a posting. Never a rebuild. This removes the mechanism entirely, which is the only
fix that scales.

**The machine checks what it can.** `scripts/claims_check.py` pulls every figure out of a
document and fails it if the figure is not in the truth file, then compares every role
heading against the employment history. It cannot judge whether a claim is honest. It can
catch a number that came from nowhere and a title that disagrees with the record, which is
where both kinds of drift start.

## The part that is not a rule

None of this produces a job. What produces a job is applying to enough well-screened roles
through channels where a human knows your name, and that is what the rest of the system is
for.

The honesty rules exist so that when the conversation finally happens, there is nothing on
the paper you have to walk back.
