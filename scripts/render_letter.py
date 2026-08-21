"""Render a cover letter markdown file to a one-page PDF matching the resume design family.

    python3 scripts/render_letter.py <input.md> <output.pdf> "Title"

Same design tokens as render_resume.py (Aptos, navy #1f3a5f on the name and rule) but
letter typography: 1in side margins, 11pt body, 1.45 line height, real paragraph spacing.
A "---" line renders as the navy rule under the header block. Check the page count: a
cover letter is one page, hard.
Environment: CHROME_PATH (browser binary), APTOS_DIR (folder with Aptos*.ttf) are optional overrides.
"""
import re, sys, os, shutil, subprocess

def _find_chrome():
    """Locate a Chrome/Chromium binary: CHROME_PATH env, then standard macOS paths, then PATH."""
    cands = [os.environ.get("CHROME_PATH"),
             "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
             "/Applications/Chromium.app/Contents/MacOS/Chromium"]
    for c in cands:
        if c and os.path.exists(c):
            return c
    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "chrome"):
        p = shutil.which(name)
        if p:
            return p
    sys.exit("ERROR: Chrome/Chromium not found. Install Google Chrome or set CHROME_PATH to the browser binary.")


def _font_dir():
    """Directory holding Aptos*.ttf: APTOS_DIR env, else Microsoft Word's bundled fonts on macOS."""
    d = os.environ.get("APTOS_DIR") or "/Applications/Microsoft Word.app/Contents/Resources/DFonts"
    return d if os.path.isdir(d) else None


def _print_pdf(html_path, pdf_path):
    chrome = _find_chrome()
    r = subprocess.run([chrome, "--headless", "--disable-gpu", "--no-pdf-header-footer",
                        f"--print-to-pdf={pdf_path}", "file://" + os.path.abspath(html_path)],
                       capture_output=True, text=True)
    os.remove(html_path)
    if not os.path.exists(pdf_path):
        sys.exit(f"ERROR: Chrome did not produce {pdf_path}\n{r.stderr[-800:]}")
    if shutil.which("pdfinfo"):
        info = subprocess.run(["pdfinfo", pdf_path], capture_output=True, text=True).stdout
        pages = [l for l in info.split("\n") if l.startswith("Pages")]
        print(f"{pdf_path}: {pages[0] if pages else 'rendered'}")
    else:
        print(f"{pdf_path}: rendered (install poppler for an automatic page count)")

if len(sys.argv) < 3:
    sys.exit(__doc__)
src, out, title = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "Cover Letter")
_pdf = out if out.endswith(".pdf") else None
out = out.replace(".pdf", ".html") if _pdf else out
t = open(src).read()
body = []
for line in t.split("\n"):
    l = line.rstrip()
    if l.startswith("# "):
        body.append(f"<h1>{l[2:]}</h1>"); continue
    if l.strip() == "---":
        body.append("<hr>"); continue
    if l.strip() == "":
        continue
    body.append(f"<p>{l}</p>")
h = "\n".join(body)
h = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', h)
h = re.sub(r'\*(.+?)\*', r'<i>\1</i>', h)
NAVY = "#1f3a5f"
DFONTS = _font_dir()
faces = ""
if DFONTS:
    faces = f"""
@font-face{{font-family:'Aptos';src:url('file://{DFONTS}/Aptos.ttf')}}
@font-face{{font-family:'Aptos';font-weight:bold;src:url('file://{DFONTS}/Aptos-Bold.ttf')}}
@font-face{{font-family:'Aptos';font-style:italic;src:url('file://{DFONTS}/Aptos-Italic.ttf')}}"""
css = f"""{faces}
@page{{size:Letter;margin:1in}}
body{{font-family:'Aptos',Calibri,'Helvetica Neue',Arial,sans-serif;font-size:11pt;line-height:1.45;color:#151515;margin:0}}
h1{{font-size:19pt;margin:0 0 3pt;letter-spacing:.5px;color:{NAVY}}}
h1+p{{font-size:10pt;color:#444;margin:0 0 8pt}}
hr{{border:none;border-top:1.5px solid {NAVY};margin:0 0 22pt}}
hr+p{{margin-bottom:20pt}}
p{{margin:0 0 11pt}}
p.sig{{margin-top:14pt}}"""
h = h.replace("<p>Sincerely,</p>", "<p class='sig'>Sincerely,</p>")
open(out, "w").write(f"<html><head><meta charset='utf-8'><title>{title}</title><style>{css}</style></head><body>{h}</body></html>")

if _pdf:
    _print_pdf(out, _pdf)
