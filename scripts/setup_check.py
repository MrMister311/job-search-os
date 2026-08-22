"""Check that everything this system needs is installed, and say exactly how to fix what is not.

    python3 scripts/setup_check.py            report only
    python3 scripts/setup_check.py --install  also install what can be installed safely

Run this first, before intake. It replaces hunting through documentation: it tells you what is
missing, what the command is, and roughly how long it will take.

Nothing here installs anything without --install, and even then it will not run a command that
needs your password without telling you first.
"""
import argparse
import os
import platform
import shutil
import subprocess
import sys

MAC = platform.system() == "Darwin"
WIN = platform.system() == "Windows"


def run(cmd, capture=True):
    try:
        r = subprocess.run(cmd, shell=isinstance(cmd, str), capture_output=capture,
                           text=True, timeout=60)
        return r.returncode, (r.stdout or "").strip()
    except Exception:
        return 1, ""


def have(name):
    return shutil.which(name) is not None


def chrome_path():
    for p in [os.environ.get("CHROME_PATH"),
              "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
              "/Applications/Chromium.app/Contents/MacOS/Chromium",
              r"C:\Program Files\Google\Chrome\Application\chrome.exe",
              r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"]:
        if p and os.path.exists(p):
            return p
    for n in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        if have(n):
            return shutil.which(n)
    return None


def aptos_dir():
    d = os.environ.get("APTOS_DIR") or "/Applications/Microsoft Word.app/Contents/Resources/DFonts"
    return d if os.path.isdir(d) else None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--install", action="store_true",
                    help="install what can be installed without surprises")
    args = ap.parse_args()

    print("== setup check\n")
    problems, fixes, notes = [], [], []

    # Python
    v = sys.version_info
    if (v.major, v.minor) >= (3, 10):
        notes.append(f"Python {v.major}.{v.minor} OK")
    else:
        problems.append(f"Python {v.major}.{v.minor} is too old; 3.10 or newer is needed")
        fixes.append(("Install a current Python from https://www.python.org/downloads/", None, "5 minutes"))

    # Xcode command line tools (macOS): this is what actually provides git on a clean Mac
    if MAC:
        code, _ = run("xcode-select -p")
        if code != 0:
            problems.append("Xcode Command Line Tools are not installed (this is what provides git)")
            fixes.append((
                "xcode-select --install",
                None,
                "10 minutes to several hours depending on your connection, and it cannot be "
                "paused or resumed. If the dialog quotes hours, cancel it and download the "
                "resumable .dmg from https://developer.apple.com/download/all instead (search "
                "\"Command Line Tools\", free Apple ID). You do NOT need this to start intake: "
                "it only provides git, for commit history. If the Claude desktop app refuses a "
                "local session without git, use the terminal version of Claude Code, which "
                "does not require it."))
        else:
            notes.append("Xcode Command Line Tools OK")

    # git
    if have("git"):
        notes.append(f"git OK ({run('git --version')[1]})")
    else:
        problems.append("git is not installed")
        if MAC:
            fixes.append(("xcode-select --install", None, "see the note above"))
        elif WIN:
            fixes.append(("Install Git for Windows from https://git-scm.com/download/win", None, "5 minutes"))
        else:
            fixes.append(("sudo apt install git", None, "1 minute"))

    # Homebrew (macOS only, and only because poppler needs it)
    brew = have("brew")
    if MAC and not brew:
        notes.append("Homebrew is not installed. It is only needed to install poppler, below")

    # poppler
    if have("pdftotext") and have("pdfinfo"):
        notes.append("poppler OK (pdftotext, pdfinfo)")
    else:
        problems.append("poppler is missing (pdftotext and pdfinfo, used for page counts and the ATS check)")
        if MAC:
            if brew:
                fixes.append(("brew install poppler", "brew install poppler", "2 to 5 minutes"))
            else:
                fixes.append((
                    'Install Homebrew first:\n     /bin/bash -c "$(curl -fsSL '
                    'https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"\n'
                    "   then: brew install poppler",
                    None,
                    "Homebrew 5 to 15 minutes and it asks for your password. Then poppler, "
                    "2 to 5 minutes. You do not need MacPorts; pick one, and Homebrew is the "
                    "one these instructions assume."))
        elif WIN:
            fixes.append(("Install poppler for Windows, or run this system inside WSL where "
                          "`apt install poppler-utils` works", None, "10 minutes"))
        else:
            fixes.append(("sudo apt install poppler-utils", None, "1 minute"))

    # Chrome
    cp = chrome_path()
    if cp:
        notes.append(f"Chrome OK ({cp})")
    else:
        problems.append("Google Chrome or Chromium not found (the PDF renderer drives it headless)")
        fixes.append(("Install Chrome from https://www.google.com/chrome/, or set CHROME_PATH "
                      "to an existing Chromium binary", None, "5 minutes"))

    # Aptos font
    if aptos_dir():
        notes.append(f"Aptos font available ({aptos_dir()})")
    else:
        notes.append("Aptos font NOT found, so resumes will render in Calibri, then Helvetica "
                     "or Arial. That is a legitimate choice, but make it deliberately: Aptos "
                     "ships with Microsoft Word, or set APTOS_DIR to a folder holding Aptos*.ttf")

    # Claude Code itself: the single most common install failure is PATH, not a bad install
    local_claude = os.path.expanduser("~/.local/bin/claude")
    if have("claude"):
        notes.append(f"Claude Code OK ({run('claude --version')[1] or 'installed'})")
    elif os.path.exists(local_claude):
        problems.append("Claude Code is installed but not on your PATH, which is why "
                        "`claude` reports command not found. The install is fine")
        fixes.append(('echo \'export PATH="$HOME/.local/bin:$PATH"\' >> ~/.zshrc '
                      '&& source ~/.zshrc',
                      'echo \'export PATH="$HOME/.local/bin:$PATH"\' >> ~/.zshrc',
                      "seconds. Use ~/.bashrc instead of ~/.zshrc if your shell is bash"))
    else:
        notes.append("Claude Code not found on PATH. If you have not installed it yet, see "
                     "SETUP.md step 2. If you have, it may be the PATH problem: check with "
                     "ls -l ~/.local/bin/claude")

    for n in notes:
        print(f"   {n}")

    if not problems:
        print("\n   RESULT: ready. Next: render a test PDF with")
        print("   python3 scripts/render_resume.py templates/base_resume.md test.pdf \"Test\"")
        return 0

    print("\n   MISSING:")
    for p in problems:
        print(f"   x {p}")
    print("\n   HOW TO FIX, in order:")
    for i, (text, cmd, how_long) in enumerate(fixes, 1):
        print(f"   {i}. {text}")
        if how_long:
            print(f"      time: {how_long}")

    if args.install:
        runnable = [(t, c) for t, c, _ in fixes if c]
        if not runnable:
            print("\n   Nothing here can be installed automatically. Run the commands above yourself.")
        else:
            print("\n   Running the installable ones:")
            for text, cmd in runnable:
                print(f"   $ {cmd}")
                code, _ = run(cmd, capture=False)
                print(f"     {'done' if code == 0 else 'FAILED, run it yourself and read the error'}")
            print("\n   Re-run this script to confirm.")
    else:
        print("\n   Re-run with --install to attempt the ones that can be automated.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
