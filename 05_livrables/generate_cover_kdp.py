#!/usr/bin/env python3
"""
generate_cover_kdp.py — Génère la couverture KDP complète (recto + dos + verso)
aux dimensions exactes requises par Amazon KDP.
"""
import weasyprint
from pathlib import Path

OUTPUT_DIR = Path("/home/ubuntu/projet_thriller_trilogie/05_livrables")
OUTPUT_PDF = OUTPUT_DIR / "Couverture_KDP_Tome1.pdf"

# ── Calculs KDP officiels ──────────────────────────────────
PAGES = 331
TRIM_W = 139.7   # mm (5.5")
TRIM_H = 215.9   # mm (8.5")
BLEED = 3.2      # mm (0.125")
SPINE = PAGES * 0.0635  # Papier crème = 22.03mm

COVER_W = BLEED + TRIM_W + SPINE + TRIM_W + BLEED  # 307.83mm
COVER_H = BLEED + TRIM_H + BLEED                     # 222.3mm

print(f"Cover dimensions: {COVER_W:.2f}mm × {COVER_H:.2f}mm")
print(f"  = {COVER_W/25.4:.3f}\" × {COVER_H/25.4:.3f}\"")
print(f"Spine: {SPINE:.2f}mm")

# ── HTML + CSS ─────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<style>
@page {{
    size: {COVER_W}mm {COVER_H}mm;
    margin: 0;
}}

* {{ margin: 0; padding: 0; box-sizing: border-box; }}

body {{
    width: {COVER_W}mm;
    height: {COVER_H}mm;
    display: flex;
    font-family: 'Liberation Serif', 'Times New Roman', Georgia, serif;
}}

/* ══ BACK COVER (gauche) ════════════════════════════════ */
.back-cover {{
    width: {TRIM_W + BLEED}mm;  /* trim + bleed gauche */
    height: {COVER_H}mm;
    background: #0d0d0f;
    padding: {BLEED + 6.4}mm {BLEED + 6.4}mm {BLEED + 6.4}mm {BLEED + 12}mm;
    display: flex;
    flex-direction: column;
    justify-content: flex-start;
    color: #c8c8cc;
    position: relative;
}}

.back-cover .blurb {{
    margin-top: 30mm;
    font-size: 9pt;
    line-height: 1.7;
    text-align: justify;
    color: #b0b0b5;
}}

.back-cover .blurb p {{
    margin-bottom: 1.2em;
}}

.back-cover .blurb .hook {{
    font-style: italic;
    color: #d0d0d5;
    font-size: 10pt;
}}

.back-cover .author-line {{
    margin-top: auto;
    margin-bottom: 20mm;
    font-size: 8pt;
    color: #666;
    letter-spacing: 1pt;
    text-transform: uppercase;
}}

/* Zone barcode — blanc pour auto-placement KDP */
.barcode-zone {{
    position: absolute;
    bottom: {BLEED + 6.4}mm;
    right: {BLEED + 6.4}mm;
    width: 50.8mm;  /* 2" */
    height: 25.4mm; /* 1" */
    background: white;
}}

/* ══ SPINE (centre) ═════════════════════════════════════ */
.spine {{
    width: {SPINE}mm;
    height: {COVER_H}mm;
    background: #050507;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: space-between;
    padding: 20mm 0 20mm 0;
    overflow: visible;
}}

.spine .title {{
    font-size: 7pt;
    letter-spacing: 0.5pt;
    color: #e8e8ec;
    font-weight: normal;
    writing-mode: vertical-rl;
    text-orientation: mixed;
}}

.spine .author {{
    font-size: 6pt;
    letter-spacing: 0.5pt;
    color: #888;
    writing-mode: vertical-rl;
    text-orientation: mixed;
}}

/* ══ FRONT COVER (droite) ═══════════════════════════════ */
.front-cover {{
    width: {TRIM_W + BLEED}mm;
    height: {COVER_H}mm;
    background: linear-gradient(170deg, #0a0a0c 0%, #12121a 40%, #0d0d12 100%);
    padding: {BLEED}mm;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    text-align: center;
    position: relative;
    overflow: hidden;
}}

/* Effet atmosphérique subtil */
.front-cover::before {{
    content: "";
    position: absolute;
    top: 20%;
    right: -20%;
    width: 200%;
    height: 60%;
    background: radial-gradient(ellipse, rgba(30, 40, 60, 0.15) 0%, transparent 60%);
    pointer-events: none;
}}

/* Ligne décorative */
.front-cover .deco-line {{
    width: 40mm;
    height: 1px;
    background: #333;
    margin: 12mm auto;
}}

.front-cover .title {{
    font-size: 30pt;
    font-weight: normal;
    color: #e8e8ec;
    letter-spacing: 4pt;
    line-height: 1.15;
    margin: 0;
    padding: 0 10mm;
    text-shadow: 0 0 30px rgba(0,0,0,0.8);
    z-index: 1;
}}

.front-cover .subtitle {{
    font-size: 11pt;
    color: #555;
    letter-spacing: 6pt;
    margin-top: 4mm;
    text-transform: uppercase;
    z-index: 1;
}}

.front-cover .author {{
    font-size: 12pt;
    color: #888;
    letter-spacing: 3pt;
    margin-top: auto;
    margin-bottom: 25mm;
    text-transform: uppercase;
    z-index: 1;
}}

.front-cover .publisher {{
    font-size: 7pt;
    color: #333;
    margin-top: 8mm;
    letter-spacing: 2pt;
}}
</style>
</head>
<body>

<!-- ════════ BACK COVER ════════ -->
<div class="back-cover">
    <div class="blurb">
        <p class="hook">Ma sœur est morte ce matin. Et la première chose qu'on m'a demandée, c'était quelle taille je faisais.</p>
        
        <p>Quand Clémence rentre dans la maison familiale de Kerfany pour recueillir la fille de sa sœur jumelle — qu'on lui a dit morte dans un accident —, elle y trouve une femme qui porte son visage. Son nom. Ses vêtements. Sa vie.</p>
        
        <p>La petite fille ne parle pas. La belle-sœur observe. La mère calcule. Et dans le journal de Charlotte, les pages se couvrent de notes manuscrites qui décrivent une transformation.</p>
        
        <p>Deux sœurs ne peuvent pas habiter le même corps. Ni la même maison. Ni le même secret.</p>
    </div>
    
    <div class="author-line">S. Varo Rosen</div>
    
    <!-- Zone barcode auto-placée par KDP -->
    <div class="barcode-zone"></div>
</div>

<!-- ════════ SPINE ════════ -->
<div class="spine">
    <div class="title">LA REMPLAÇANTE</div>
    <div class="author">S. VARO ROSEN</div>
</div>

<!-- ════════ FRONT COVER ════════ -->
<div class="front-cover">
    <div class="title">LA<br>REMPLAÇANTE</div>
    <div class="deco-line"></div>
    <div class="subtitle">Tome 1</div>
    <div class="author">S. VARO ROSEN</div>
    <div class="publisher">THRILLER</div>
</div>

</body>
</html>
"""

# ── Generate PDF ───────────────────────────────────────────
print("Generating cover PDF...")
HTML = weasyprint.HTML(string=html)
HTML.write_pdf(str(OUTPUT_PDF))

file_size = OUTPUT_PDF.stat().st_size
print(f"✅ Cover generated: {OUTPUT_PDF}")
print(f"   Size: {file_size / 1024:.0f} KB")

# Verify dimensions
import subprocess
try:
    result = subprocess.run(['pdfinfo', str(OUTPUT_PDF)], capture_output=True, text=True, timeout=10)
    for line in result.stdout.split('\n'):
        if 'Page size' in line or 'Pages' in line:
            print(f"   {line.strip()}")
except:
    pass
