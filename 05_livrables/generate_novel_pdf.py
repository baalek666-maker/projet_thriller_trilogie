#!/usr/bin/env python3
"""
generate_novel_pdf.py — Convertit le manuscrit La Remplaçante en PDF professionnel.
"""
import re
import markdown
import weasyprint
from pathlib import Path

MANUSCRIPT = Path("/home/ubuntu/projet_thriller_trilogie/04_manuscrits/la_remplacante_tome1.md")
OUTPUT_DIR = Path("/home/ubuntu/projet_thriller_trilogie/05_livrables")
OUTPUT_PDF = OUTPUT_DIR / "La_Remplacante_Tome1.pdf"
CSS_FILE = Path("/tmp/novel_style.css")

# ── 1. Read manuscript ──────────────────────────────────────
text = MANUSCRIPT.read_text(encoding="utf-8")

# ── 2. Pre-process ───────────────────────────────────────────
# Remove metadata header (Structure line + Narration line)
text = re.sub(r'## Structure :.*?\nNarration :.*?\n\n', '', text, count=1)

# Remove standalone --- (they'll be replaced by CSS page breaks)
text = re.sub(r'\n---\n', '\n', text)

# ── 3. Split into title + chapters ──────────────────────────
lines = text.split('\n')
title_line = lines[0].strip('# ')  # "La Remplaçante — Tome 1"
body_text = '\n'.join(lines[1:]).strip()

# ── 4. Convert markdown to HTML ──────────────────────────────
# Custom extension: wrap chapter headings in a <section> for page breaks
def chapterize(md_text):
    """Split on ## Chapitre markers and wrap each in a <section>."""
    parts = re.split(r'(?=## Chapitre \d+ :)', md_text)
    html_parts = []
    
    for i, part in enumerate(parts):
        if not part.strip():
            continue
        
        # Extract chapter number and title
        match = re.match(r'## Chapitre (\d+) : (.+?)(?:\n|$)', part)
        if match:
            num, title = match.group(1), match.group(2).strip()
            # Remove the heading from markdown, we'll add it as HTML
            body = re.sub(r'^## Chapitre \d+ : .+?\n', '', part, count=1)
            
            # Convert body markdown to HTML
            body_html = markdown.markdown(
                body,
                extensions=['smarty'],
            )
            
            # Wrap in section with chapter header
            section = f'''
<section class="chapter">
    <div class="chapter-header">
        <div class="chapter-deco"></div>
        <h2 class="chapter-title">{title}</h2>
        <p class="chapter-num">Chapitre {num}</p>
    </div>
    <div class="chapter-body">
{body_html}
    </div>
</section>
'''
            html_parts.append(section)
        else:
            # Non-chapter content (if any)
            body_html = markdown.markdown(part, extensions=['smarty'])
            html_parts.append(body_html)
    
    return '\n'.join(html_parts)

html_body = chapterize(body_text)

# ── 5. Write CSS ──────────────────────────────────────────────
css = """
/* ── Page Setup ───────────────────────────────────────── */
@page {
    size: 140mm 210mm;  /* A5 — format roman français */
    margin: 2cm 2.2cm 2.5cm 2.2cm;
    background: white;
    
    @bottom-center {
        content: counter(page);
        font-family: 'Liberation Serif', 'Times New Roman', serif;
        font-size: 9pt;
        color: #999;
        vertical-align: bottom;
    }
}

@page:first {
    @bottom-center { content: none; }
}

/* ── Body ─────────────────────────────────────────────── */
body {
    font-family: 'Liberation Serif', 'Times New Roman', serif;
    font-size: 10pt;
    line-height: 1.55;
    color: #1c1c1c;
    background: white;
    text-align: justify;
    text-justify: inter-word;
    hyphens: auto;
    hyphenate-limit-chars: 6 3 3;
    orphans: 3;
    widows: 3;
}

p {
    margin: 0 0 0.5em 0;
    text-indent: 1.5em;
    text-align: justify !important;
}

p:first-child {
    text-indent: 0;
}

/* ── Title Page ───────────────────────────────────────── */
.title-page {
    text-align: center;
    padding-top: 5cm;
    page-break-after: always;
}

.title-page h1 {
    font-family: 'Liberation Serif', 'Times New Roman', serif;
    font-size: 22pt;
    font-weight: normal;
    color: #1c1c1c;
    margin-bottom: 0.5cm;
    letter-spacing: 2pt;
}

.title-page .subtitle {
    font-size: 13pt;
    font-style: italic;
    color: #555;
    margin-bottom: 2cm;
}

.title-page .author {
    font-size: 11pt;
    color: #555;
    margin-top: 3cm;
}

/* ── Copyright Page ───────────────────────────────────── */
.copyright-page {
    page-break-before: always;
    page-break-after: always;
    padding-top: 5cm;
    text-align: center;
    font-family: 'Liberation Serif', 'Times New Roman', serif;
    font-size: 9pt;
    color: #666;
    line-height: 1.8;
}

.copyright-page p {
    text-indent: 0;
    text-align: center;
}

/* ── Chapter Headers ──────────────────────────────────── */
.chapter {
    page-break-before: always;
    margin-top: 1.5cm;
}

.chapter:first-of-type {
    page-break-before: avoid;
}

.chapter-header {
    text-align: center;
    margin-bottom: 1.5cm;
}

.chapter-deco {
    width: 3cm;
    height: 1px;
    background: #bbb;
    margin: 0 auto 1cm auto;
}

.chapter-title {
    font-family: 'Liberation Serif', 'Times New Roman', serif;
    font-size: 15pt;
    font-weight: normal;
    color: #1c1c1c;
    margin: 0 0 0.3cm 0;
    letter-spacing: 1pt;
}

.chapter-num {
    font-family: 'Liberation Serif', 'Times New Roman', serif;
    font-size: 9pt;
    color: #999;
    text-transform: uppercase;
    letter-spacing: 3pt;
    margin: 0;
}

/* ── Body Text ────────────────────────────────────────── */
.chapter-body > p:first-child {
    text-indent: 0;
}

/* ── Italics ──────────────────────────────────────────── */
em {
    font-style: italic;
    color: inherit;
}

strong {
    font-weight: bold;
}

/* ── Letter excerpts (italic blocks) ──────────────────── */
p > em:only-child {
    display: block;
    margin: 1em 2em;
    font-style: italic;
    line-height: 1.5;
}

br {
    line-height: 1.2;
}

/* ── Separators within chapters ───────────────────────── */
hr {
    border: none;
    text-align: center;
    margin: 2em 0;
}

hr::after {
    content: "❦";
    color: #ccc;
    font-size: 14pt;
}
"""

CSS_FILE.write_text(css, encoding="utf-8")

# ── 6. Generate full HTML ────────────────────────────────────
html_full = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<title>La Remplaçante — Tome 1</title>
<style>
{css}
</style>
</head>
<body>

<!-- Title Page -->
<div class="title-page">
    <h1>La Remplaçante</h1>
    <p class="subtitle">Tome 1</p>
    <div class="chapter-deco"></div>
</div>

<!-- Copyright Page -->
<div class="copyright-page">
    <p><em>La Remplaçante</em> — Tome 1</p>
    <p>Roman</p>
    <p>&nbsp;</p>
    <p>Ce livre est une œuvre de fiction. Toute ressemblance avec des personnes<br>
    ou des événements réels serait purement fortuite.</p>
    <p>&nbsp;</p>
    <p>&copy; 2026 — Tous droits réservés</p>
</div>

{html_body}

</body>
</html>
"""

# ── 7. Generate PDF ───────────────────────────────────────────
print("Generating PDF...")
HTML = weasyprint.HTML(string=html_full)
HTML.write_pdf(str(OUTPUT_PDF))

# Check result
file_size = OUTPUT_PDF.stat().st_size
page_count = "?"  # WeasyPrint 69 doesn't expose page count easily
print(f"✅ PDF generated: {OUTPUT_PDF}")
print(f"   Size: {file_size / 1024:.0f} KB")

# Try to count pages via pdfinfo if available
import subprocess
try:
    result = subprocess.run(['pdfinfo', str(OUTPUT_PDF)], capture_output=True, text=True, timeout=10)
    for line in result.stdout.split('\n'):
        if 'Pages' in line:
            print(f"   {line.strip()}")
except:
    pass