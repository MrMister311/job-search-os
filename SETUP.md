# Setup

For someone comfortable with a computer who is not a developer. You do not need to know how to
code. You will copy and paste a few commands.

Verified against Anthropic's documentation on 2026-08-21. Links and menu labels change; if
something does not match, the official docs at https://code.claude.com/docs are the authority.

---

This project is not legal, financial, or career advice; see [`DISCLAIMER.md`](DISCLAIMER.md).

## Before you start: what this costs

**Claude Code is not free.** The free Claude.ai plan cannot run it. You need one of:

- A **Claude Pro** subscription (the usual choice)
- **Claude Max** (same Claude Code features as Pro, higher usage limits)
- Team or Enterprise, if your workplace provides it, though see the privacy note below
- A **Console account** with prepaid API credits, billed per use

Pro and Max are identical in what Claude Code can *do*. The difference is how much you can use
before hitting limits. Start with Pro.

**Use a personal account, not a work one.** This repository will hold your employment history,
compensation targets, and every application you send. Your employer should not be able to see
any of it.

You also need:

- **git** installed. On a Mac it usually already is. On Windows, install Git for Windows from
  https://git-scm.com, which is also required for local sessions in the Claude desktop app.
- A GitHub account is **optional**. It gives you offsite backup and sync between computers.
  Step 1 covers both paths.
- macOS 13 or later, or Windows 10 (1809) or later

---

## Step 1: Get the files

You do **not** need a GitHub account. Pick one of these two.

### Option A: Download the files (simplest, recommended)

1. Go to https://github.com/MrMister311/job-search-os
2. Click the green **Code** button (the one above the file list, not the "Code" tab at the
   top of the page), then **Download ZIP**
3. Unzip it and move the folder somewhere sensible, for example your home folder, renamed to
   something like `my-job-search`

That is it. Nothing you write is connected to GitHub or visible to anyone.

**Then turn it into a git repository**, which the system uses to track changes and let you
undo mistakes. This is local only. No account, nothing uploaded. Open Terminal (Mac: press
Cmd+Space, type "Terminal") or PowerShell (Windows: press Start, type "PowerShell") and run,
adjusting the folder name:

```
cd ~/my-job-search
git init
git add -A
git commit -m "Starting point"
```

If `git` is not installed, get it from https://git-scm.com. On most Macs it is already there.

**What you give up:** if your computer dies, your job search dies with it. If that bothers
you, do Option B instead, or just copy the folder to a backup drive now and then.

### Option B: Your own private repository on GitHub (adds backup and sync)

Worth it if you want your work backed up offsite or want to use it from more than one
computer. Requires a free account at https://github.com.

**Do not fork this repository.** A fork of a public repository is permanently public and
cannot be made private afterward. Your salary history would be visible to anyone, including
your employer. Use the template button instead, which lets you choose Private:

1. Sign in to GitHub, then go to https://github.com/MrMister311/job-search-os
2. Click **Use this template**, then **Create a new repository**. The button only appears
   when you are signed in to GitHub. If you do not see it, sign in and reload, or go straight
   to https://github.com/MrMister311/job-search-os/generate
3. Name it, for example `my-job-search`
4. **Select Private.** This is the step that matters
5. Click **Create repository**

Then get it onto your computer. Either install GitHub Desktop from https://desktop.github.com,
sign in, and use **File > Clone repository**; or run this in a terminal, replacing
`YOUR-USERNAME`:

```
cd ~
git clone https://github.com/YOUR-USERNAME/my-job-search.git
```

Verify it is actually private before you put anything real in it:

```
cd ~/my-job-search
python3 scripts/privacy_check.py
```

## Step 1b: Check your tooling (and what you can skip)

From your project folder, run:

```
python3 scripts/setup_check.py
```

It lists what is installed, what is missing, the exact command for each fix, and roughly how
long each takes.

**You do not need all of it to start.** The intake interview needs nothing installed. Tooling
matters at the end, when the first resume is rendered:

| To do this | You need |
|---|---|
| The whole intake interview | nothing |
| Render a resume or cover letter to PDF | Python 3.10+ and Google Chrome |
| Automatic page count after rendering | plus poppler |
| `ats_check.py` | plus poppler |
| Commit history and undo | plus git |

**A warning about the Xcode Command Line Tools on Mac.** That is where git comes from, and it
is a large download. Apple's documentation and Anthropic's both assume you already have it;
a Mac that has never had it does not really have git, only a stub that triggers this install.
Running `xcode-select --install` opens a system dialog whose time estimate is frequently wrong.
On a slow connection it can claim many hours, and it cannot be paused or resumed. If that
happens to you:

- Cancel it. You are not stuck; git is not needed for the interview
- Install later from https://developer.apple.com/download/all (search "Command Line Tools",
  free Apple ID). That is a normal .dmg download, which resumes if it drops
- If `python3 --version` also fails, do not wait on Xcode for it. Install Python directly from
  https://www.python.org/downloads/, a much smaller download
- **If the Claude desktop app refuses to start a local session without git, use the terminal
  instead.** Anthropic's setup documentation does not list git as a requirement for the CLI
  (only for the desktop app on Windows), so `claude` in a terminal is the way around a stalled
  Xcode download. Option B in Step 2 has the install command

Homebrew is only needed to install poppler, and poppler is only needed for page counts and the
ATS check. You do not need MacPorts. If you already have one of them, use that one.

## Step 2: Install Claude Code

Two ways to run it. Read both before choosing.

| | Desktop app | Terminal |
|---|---|---|
| Setup | Download and double-click | One command, then a PATH fix if it does not work |
| Terminal needed | No | Yes |
| git required | Yes on Windows, and in practice on a Mac that has never installed developer tools | Not listed as a requirement |
| Best for | Most people | Anyone stuck on a slow or failing developer-tools download |

Anthropic's own troubleshooting page puts it plainly: "If you'd rather skip the terminal
entirely, the Claude Code Desktop app lets you install and use Claude Code through a graphical
interface." That is the right default. Use the terminal if the desktop app blocks you on git.

### Option A: Desktop app

1. Download from https://claude.ai/download and install it
2. Open it and sign in. **A paid plan is required.** The free plan cannot run Claude Code
3. Click the **Code** tab at the top
4. Set **Environment** to **Local**
5. Click **Select folder** and pick the folder from Step 1
6. Choose a permission mode. **Accept edits** is a reasonable start, because this system writes
   a lot of files and approving each one gets tedious
7. Type your first instruction (Step 3) and press Enter

**If it refuses to start a local session because git is missing:** on Windows, install Git for
Windows from https://git-scm.com/download/win and restart the app. On a Mac, git comes from the
Xcode Command Line Tools, and if that download is slow or stalled, switch to Option B rather
than waiting.

### Option B: Terminal

**Install.** Open Terminal (Mac: press Cmd+Space, type "Terminal") or PowerShell (Windows:
press Start, type "PowerShell") and run:

**Mac or Linux**
```
curl -fsSL https://claude.ai/install.sh | bash
```

**Windows PowerShell**
```
irm https://claude.ai/install.ps1 | iex
```

**Verify.**
```
claude --version
```

A working install prints something like `2.1.211 (Claude Code)`.

**If you get `zsh: command not found: claude`, that is expected and normal.** It is the most
common install problem, and it is not a failed install. The installer puts the program at
`~/.local/bin/claude`, and your shell does not know to look there yet. Fix it:

```
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
claude --version
```

(On Linux, if your shell is bash, use `~/.bashrc` in both places instead of `~/.zshrc`.)

If it still fails, check whether the program is actually there:

```
ls -l ~/.local/bin/claude
```

- **File exists:** PATH is still wrong. Try closing the terminal completely and opening a new
  one, then run `claude --version` again.
- **No such file:** the install did not finish, usually a dropped download. Run the install
  command again and read the output instead of letting it scroll past.

**Start it.** Move into your project folder first, then launch:

```
cd ~/my-job-search
claude
```

**Always `cd` into the project folder before running `claude`.** Starting it from your home
folder means the trust prompt comes back every single time and is never remembered.

### What happens on first launch, in order

1. **Login.** A browser opens. Sign in with your Claude account. Credentials are stored, so
   this happens once
2. **Trust prompt.** It asks whether you trust the folder. Say yes
3. **Permission behavior.** In your first session it asks before every change. That is
   deliberate and only applies to the first session

### Other install errors worth knowing

| What you see | What it means |
|---|---|
| `command not found: claude` | PATH. See above. Not a failed install |
| `syntax error near unexpected token '<'` or a 403 | The download returned a web page instead of the installer. Usually a network or proxy problem. Try again on a different connection |
| `curl: (56) Failure writing output` | Connection dropped mid-download. Run it again |
| `irm is not recognized` | You are in CMD, not PowerShell. Your prompt shows `PS C:\` in PowerShell |
| `Claude Code requires a Pro, Max, Team, or Enterprise subscription` | The free plan does not include Claude Code |

Anthropic's full list is at https://code.claude.com/docs/en/troubleshoot-install

## Step 3: Your first session

Whichever way you started it, type this:

```
Read CLAUDE.md and INTAKE.md and let's begin intake.
```

That is the whole trigger. It will run an environment check first, confirming Python, git,
Chrome, and the PDF tools are present, then start interviewing you about your work history.

**Expect intake to take more than one sitting.** It is building a verified record of your
career, and it will push back on numbers you cannot explain. That is the point.

Before you start, gather:

- Every old resume you can find
- Performance reviews or any written assessment from a manager
- Your LinkedIn profile as it stands now
- A rough sense of your target: titles, minimum salary, where you will and will not work

If you want to see what a finished system looks like first, open
[`examples/morgan-hale/`](examples/morgan-hale/README.md). It is a complete fictional example.

---

## Step 4: Everyday use

Start a session the same way each time: open the folder in the desktop app's Code tab, or
`cd` into it and run `claude`.

A good opening line for any later session:

```
Read CLAUDE.md and the latest session log entry, then tell me what needs doing.
```

Commands worth knowing, typed inside a session:

| Command | What it does |
|---|---|
| `/help` | Lists everything available |
| `/` | Type just a slash to see all commands |
| `/clear` | Starts a fresh conversation, keeping the files |
| `/usage` | Shows how much of your plan you have used |
| `/exit` | Ends the session |

In the terminal only:

| Command | What it does |
|---|---|
| `claude -c` | Continues your most recent conversation in this folder |
| `claude -r` | Picks an older conversation to resume |
| `claude doctor` | Checks your installation if something seems broken |

---

## Keeping it private

Three rules.

1. **If you put it on GitHub, it stays private.** Run `python3 scripts/privacy_check.py` in
   your project folder any time you are unsure; it tells you what the remote is and whether
   anything is exposed. On GitHub, your repository page shows "Private" next to the name. If
   it says Public, go to Settings, scroll to the bottom, and change it. If you forked instead
   of using the template button, it cannot be changed and you need to redo Step 1. If you took
   Option A and never touched GitHub, there is nothing to expose.
2. **Work in local sessions.** The desktop app also offers Cloud sessions, and there is a
   web version at claude.ai/code. Those run on Anthropic's servers rather than your machine,
   and cloud sessions can be shared publicly by accident. Anthropic's own documentation warns
   to check for sensitive content before sharing a session. This repository holds your salary
   history and personal details, so keep it local.
3. **Personal account, personal machine.** Not a work laptop, not a work Claude account, not a
   work GitHub organization.

---

## If something goes wrong

**"claude: command not found"** after installing: close and reopen your terminal. If it still
fails, run the installer again and read what it prints about your PATH.

**It asks about trusting the folder every time:** you are running `claude` from your home
folder. `cd` into the project folder first.

**"Claude Code requires a Pro, Max, Team, or Enterprise subscription":** the free plan does not
include Claude Code. See the top of this page.

**The resume PDF renders in the wrong font:** the design uses Aptos, which comes with Microsoft
Word. Without Word it silently falls back to Calibri, then Helvetica or Arial. Intake walks you
through checking this so the fallback is a decision rather than an accident.

**A script fails with "command not found: pdftotext":** install poppler. On a Mac,
`brew install poppler`. On Ubuntu or Debian, `sudo apt install poppler-utils`.

**Anything else:** describe it to Claude in the session. It has this repository's full context
and can usually diagnose its own environment.
