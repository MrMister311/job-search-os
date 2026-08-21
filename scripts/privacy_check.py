"""Verify this repository cannot leak the owner's personal data.

    python3 scripts/privacy_check.py

This repository holds employment history, compensation targets, contact names, and every
application sent. One wrong click makes that public and there is no taking it back. Run this
at Session Zero, after any change to remotes, and any time the owner is unsure.

Checks, in order of severity:

  1. Remote visibility. If a git remote points at GitHub, ask GitHub whether the repository is
     public. Requires the `gh` CLI, authenticated. Without gh, the check reports UNKNOWN and
     tells you how to verify by hand, because a silent pass here would be worse than no check.
  2. Fork status. A fork of a public repository is permanently public and cannot be made
     private. If this is one, the only fix is to recreate the repository.
  3. Truth-layer files staged or committed to a public remote (only meaningful if 1 says
     public).
  4. Loose credentials: files that look like keys, tokens, or .env files anywhere in the tree.

Exit status is 1 if anything is a hard failure, so it can gate a push.
"""
import json
import os
import re
import shutil
import subprocess
import sys

SECRET_NAMES = re.compile(r"(^|/)(\.env|\.env\..+|id_rsa|id_ed25519|.*\.pem|.*\.p12|.*\.pfx|"
                          r"credentials(\.json)?|token(\.txt|\.json)?|.*secret.*)$", re.I)
SECRET_CONTENT = re.compile(r"(sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|"
                            r"AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----)")
TRUTH_FILES = ["profile/employment_history.md", "profile/master_skills.md",
               "profile/target_roles.md", "profile/contacts.md", "profile/pipeline.md",
               "profile/compensation_research.md", "profile/negotiation_scripts.md"]
TEMPLATE_MARKERS = ("STATUS: INCOMPLETE", "STATUS: TEMPLATE", "[FILL", "populated during intake")


def is_unpopulated_template():
    """True when the truth layer is still blank, i.e. this is the shared template itself
    rather than somebody's real search. A public template is fine; a public search is not."""
    for f in ("profile/master_skills.md", "profile/employment_history.md",
              "profile/target_roles.md"):
        if not os.path.exists(f):
            return False
        text = open(f, encoding="utf-8", errors="ignore").read()
        if not any(m in text for m in TEMPLATE_MARKERS):
            return False
    return True


def sh(*args):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=25)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return 1, "", "not available"


def main():
    fails, warns, notes = [], [], []

    code, remotes, _ = sh("git", "remote", "-v")
    if code != 0:
        print("Not a git repository, or git is unavailable. Nothing to check.")
        return 0

    if not remotes:
        notes.append("no git remote configured: nothing is pushed anywhere, which is safe")
        slug = None
    else:
        url = remotes.split("\n")[0].split()[1]
        m = re.search(r"github\.com[:/]+([^/]+/[^/\s]+?)(?:\.git)?$", url)
        slug = m.group(1) if m else None
        notes.append(f"remote: {url}")
        if not slug:
            warns.append(f"remote is not GitHub ({url}); verify its visibility manually")

    if slug:
        if not shutil.which("gh"):
            warns.append(f"gh CLI not installed, so visibility is UNKNOWN. Verify by hand: "
                         f"open https://github.com/{slug} and confirm it is labeled Private")
        else:
            code, out, err = sh("gh", "api", f"repos/{slug}",
                                "--jq", "{v:.visibility,f:.fork,p:.parent.full_name}")
            if code != 0:
                warns.append(f"could not query GitHub for {slug} ({err[:90]}). "
                             f"Verify by hand that it is Private")
            else:
                d = json.loads(out)
                if d.get("v") != "private":
                    if is_unpopulated_template():
                        notes.append(f"{slug} is {d.get('v')}, but the truth layer is still "
                                     f"blank, so this is the shared template rather than a "
                                     f"real search. Make your own copy private before intake")
                    else:
                        fails.append(f"REPOSITORY IS {str(d.get('v')).upper()} and the truth "
                                     f"layer is populated. Employment history and compensation "
                                     f"targets are visible to anyone. Fix now: "
                                     f"https://github.com/{slug}/settings, scroll to the Danger "
                                     f"Zone, change visibility to Private")
                else:
                    notes.append(f"{slug} is private")
                if d.get("f"):
                    fails.append(f"this is a FORK of {d.get('p')}. Forks of public repositories "
                                 f"are permanently public and cannot be made private. Recreate "
                                 f"the repository from the template instead (see SETUP.md)")

    tracked = sh("git", "ls-files")[1].split("\n")
    if any("REPOSITORY IS" in x for x in fails):
        exposed = [f for f in TRUTH_FILES if f in tracked]
        if exposed:
            fails.append("populated truth-layer files are committed to that public repository: "
                         + ", ".join(exposed))

    for path in tracked:
        if not path:
            continue
        if SECRET_NAMES.search(path):
            warns.append(f"file name looks sensitive and is tracked by git: {path}")
        if os.path.isfile(path) and os.path.getsize(path) < 2_000_000:
            try:
                if SECRET_CONTENT.search(open(path, encoding="utf-8", errors="ignore").read()):
                    fails.append(f"what looks like a live credential is tracked in {path}")
            except OSError:
                pass

    print("== privacy check")
    for n in notes:
        print(f"   note: {n}")
    for w in warns:
        print(f"   ! {w}")
    for f in fails:
        print(f"   ✗ {f}")
    print("\n   RESULT:", "FAIL, fix before doing anything else" if fails
          else ("PASS with warnings, read them" if warns else "PASS"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
