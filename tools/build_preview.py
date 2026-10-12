"""Build an offline, dependency-light preview when Quarto is unavailable.

Quarto remains the source of truth. Running `quarto render` replaces this
preview with a native Quarto website in the same docs/ directory.
"""

from pathlib import Path
import re
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs"
OUT.mkdir(exist_ok=True)


def body(filename: str, *, sections: bool = False) -> str:
    command = [
        "pandoc", str(ROOT / filename), "--from", "markdown+fenced_divs",
        "--to", "html5", "--mathml",
    ]
    if sections:
        command.append("--section-divs")
    return subprocess.check_output(command, text=True)


home = body("index.qmd").replace('href="slides.qmd"', 'href="slides.html"')
home = home.replace('href="follow-along.ipynb"', 'href="follow-along.ipynb"')
home_html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>STAT 386 | Data cleaning and string operations</title>
<link rel="stylesheet" href="styles.css">
<style>body{{max-width:850px;margin:auto;padding:1rem 2rem 4rem;font:18px/1.55 system-ui,sans-serif}}
nav{{display:flex;gap:1.5rem;border-bottom:1px solid #cbd8e0;padding:.7rem 0}}
code{{background:#edf3f6;padding:.12rem .24rem}}
@media(max-width:600px){{body{{padding:1rem}}}}</style></head><body>
<nav><a href="index.html">Home</a><a href="slides.html">Lecture slides</a>
<a href="follow-along.ipynb">Notebook</a></nav>
{home}</body></html>"""
(OUT / "index.html").write_text(home_html)

slide_content = body("slides.qmd", sections=True)
count = len(re.findall(r'<section\b[^>]*class="level2"', slide_content)) + 1
slides_html = f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>STAT 386 | Data cleaning and string operations</title>
<link rel="stylesheet" href="slide.css">
<style>html,body{{margin:0;min-height:100%;font-family:system-ui,sans-serif;background:#fafcfd}}
.reveal .slides > section{{display:none;box-sizing:border-box;min-height:100vh;padding:5vh 6vw 8vh;overflow:auto}}
.reveal .slides > section.active{{display:block}}
.controls{{position:fixed;right:1.4rem;bottom:.5rem;font:16px system-ui;background:#fffdfaee;padding:.3rem .65rem;border-radius:6px}}
.controls button{{border:0;background:transparent;color:#185d70;font-size:22px;cursor:pointer}}
.home{{position:fixed;left:1rem;bottom:1rem;font:15px system-ui}}
@media print{{.reveal .slides > section{{display:block!important;min-height:100vh;break-after:page}}.controls,.home{{display:none}}}}
</style></head><body><main class="reveal"><div class="slides">
<section id="title" class="active"><h1>Data cleaning and string operations</h1>
<p>Reproducible processing of talk data</p><p>STAT 386 · October 12, 2026</p></section>
{slide_content}</div></main>
<a class="home" href="index.html">Course home</a>
<div class="controls"><button id="prev" aria-label="Previous slide">‹</button>
<span id="position">1 / {count}</span><button id="next" aria-label="Next slide">›</button></div>
<script>
const slides=[...document.querySelectorAll('.slides > section')];
let current=Math.max(0, Math.min(slides.length-1, Number(location.hash.slice(1)) || 0));
function show(n){{current=Math.max(0,Math.min(slides.length-1,n));
  slides.forEach((s,i)=>s.classList.toggle('active',i===current));
  document.getElementById('position').textContent=(current+1)+' / '+slides.length;
  history.replaceState(null,'','#'+current);window.scrollTo(0,0);}}
document.getElementById('prev').onclick=()=>show(current-1);
document.getElementById('next').onclick=()=>show(current+1);
document.addEventListener('keydown', e=>{{
  if(['ArrowRight','PageDown',' '].includes(e.key)){{e.preventDefault();show(current+1)}}
  if(['ArrowLeft','PageUp'].includes(e.key)){{e.preventDefault();show(current-1)}}
}});
window.addEventListener('hashchange',()=>show(Number(location.hash.slice(1))||0));
show(current);
</script></body></html>"""
(OUT / "slides.html").write_text(slides_html)

for filename in ["slide.css", "styles.css", "follow-along.ipynb", "cleaning.py"]:
    shutil.copy2(ROOT / filename, OUT / filename)
(OUT / "data").mkdir(exist_ok=True)
for item in (ROOT / "data").glob("*.csv"):
    shutil.copy2(item, OUT / "data" / item.name)
(OUT / ".nojekyll").touch()
print(f"Built {count} slides and the site in {OUT}")
