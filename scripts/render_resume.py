"""Render a resume markdown file to a print-ready PDF — the approved 2026 design.

    python3 scripts/render_resume.py <input.md> <output.pdf> "Full Name"

Inherited design spec (validated against 2026 resume-design research in the origin system):
Aptos 10.5pt (embedded from Word's font folder; Calibri fallback), 1.3 line height,
0.55in margins, 3pt bullet gaps, 9pt between jobs, 13pt before sections, single navy
accent (#1f3a5f) on name/headings/rules.
Always check the page count in the output against the page limit set at intake.
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
src,out,title=sys.argv[1],sys.argv[2],(sys.argv[3] if len(sys.argv)>3 else "Resume")
_pdf = out if out.endswith(".pdf") else None
out = out.replace(".pdf",".html") if _pdf else out
t=open(src).read()
body=[]
for line in t.split("\n"):
    l=line.rstrip()
    if l.startswith("# "): body.append(f"<h1>{l[2:]}</h1>"); continue
    if l.startswith("## "): body.append(f"<h2>{l[3:]}</h2>"); continue
    if l.startswith("### "): body.append(f"<h3>{l[4:]}</h3>"); continue
    if l.strip()=="---": continue
    if l.strip()=="===PAGEBREAK===": body.append("<div style='page-break-before:always'></div>"); continue
    if l.startswith("- "): body.append(f"<li>{l[2:]}</li>"); continue
    if l.startswith("  ") and body and body[-1].startswith("<li>"):
        body[-1]=body[-1][:-5]+" "+l.strip()+"</li>"; continue
    if l.strip()=="": body.append(""); continue
    body.append(f"<p>{l}</p>")
h="\n".join(body)
h=re.sub(r'\*\*(.+?)\*\*',r'<b>\1</b>',h)
h=re.sub(r'\*(.+?)\*',r'<i>\1</i>',h)
h=re.sub(r'(<li>.*</li>\n?)+',lambda m:"<ul>"+m.group(0)+"</ul>",h)
h=re.sub(r'<p></p>','',h)
NAVY="#1f3a5f"
DFONTS=_font_dir()
faces=""
if DFONTS:
    faces=f"""
@font-face{{font-family:'Aptos';src:url('file://{DFONTS}/Aptos.ttf')}}
@font-face{{font-family:'Aptos';font-weight:bold;src:url('file://{DFONTS}/Aptos-Bold.ttf')}}
@font-face{{font-family:'Aptos';font-style:italic;src:url('file://{DFONTS}/Aptos-Italic.ttf')}}
@font-face{{font-family:'Aptos';font-weight:bold;font-style:italic;src:url('file://{DFONTS}/Aptos-Bold-Italic.ttf')}}"""
css=f"""{faces}
@page{{size:Letter;margin:0.55in}}
body{{font-family:'Aptos',Calibri,'Helvetica Neue',Arial,sans-serif;font-size:10.5pt;line-height:1.3;color:#151515;margin:0}}
h1{{font-size:20pt;margin:0 0 2pt;letter-spacing:.5px;color:{NAVY}}}
h2{{font-size:10.5pt;text-transform:uppercase;letter-spacing:1.2px;color:{NAVY};border-bottom:1px solid {NAVY};margin:13pt 0 5pt;padding-bottom:2pt}}
h3{{font-size:10.5pt;margin:9pt 0 1pt;page-break-after:avoid}}
li{{page-break-inside:avoid}}
p{{margin:2pt 0}}
ul{{margin:2pt 0 5pt;padding-left:14pt}}
li{{margin:3pt 0}}
i{{color:#444}}"""
open(out,"w").write(f"<html><head><meta charset='utf-8'><title>{title}</title><style>{css}</style></head><body>{h}</body></html>")


if _pdf:
    _print_pdf(out, _pdf)
