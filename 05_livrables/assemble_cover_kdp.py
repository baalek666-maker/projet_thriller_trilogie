#!/usr/bin/env python3
"""
assemble_cover_kdp.py — Assemble recto + tranche + quatrième en couverture KDP
aux dimensions exactes requises par Amazon.
"""
from PIL import Image
try:
    RESAMPLE = Image.Resampling.LANCZOS  # Pillow ≥ 9.1
except AttributeError:
    RESAMPLE = RESAMPLE             # Pillow < 9.1
import os

# ── Images source ──────────────────────────────────────────
FRONT_IMG = "/home/ubuntu/.hermes/image_cache/img_df9b7ce9836a.png"
BACK_IMG  = "/home/ubuntu/.hermes/image_cache/img_efc44f5e5445.png"
SPINE_IMG = "/home/ubuntu/.hermes/image_cache/img_34e0d0e6fa8d.png"

OUTPUT_PDF = "/home/ubuntu/projet_thriller_trilogie/05_livrables/Couverture_KDP_Tome1.pdf"
OUTPUT_PNG = "/home/ubuntu/projet_thriller_trilogie/05_livrables/cover_assembled.png"

# ── KDP specs (mm) ─────────────────────────────────────────
PAGES   = 331
TRIM_W  = 139.7    # 5.5"
TRIM_H  = 215.9    # 8.5"
BLEED   = 3.2      # 0.125"
SPINE   = PAGES * 0.0635  # Papier crème = 21.02mm

COVER_W = BLEED + TRIM_W + SPINE + TRIM_W + BLEED  # 306.82mm
COVER_H = BLEED + TRIM_H + BLEED                    # 222.3mm

DPI = 300
PX_PER_MM = DPI / 25.4

# Canvas dimensions in pixels
CANVAS_W = round(COVER_W * PX_PER_MM)
CANVAS_H = round(COVER_H * PX_PER_MM)

# Zone dimensions
BACK_W_PX  = round((BLEED + TRIM_W) * PX_PER_MM)   # back cover + left bleed
SPINE_W_PX = round(SPINE * PX_PER_MM)               # spine only
FRONT_W_PX = round((TRIM_W + BLEED) * PX_PER_MM)    # front cover + right bleed
ZONE_H_PX  = CANVAS_H                                # full height (with bleed)

print(f"KDP Cover: {COVER_W:.2f}mm × {COVER_H:.2f}mm ({COVER_W/25.4:.3f}\" × {COVER_H/25.4:.3f}\")")
print(f"Canvas:    {CANVAS_W} × {CANVAS_H} px @ {DPI} DPI")
print(f"Back zone: {BACK_W_PX}px | Spine zone: {SPINE_W_PX}px | Front zone: {FRONT_W_PX}px")
print(f"Total:     {BACK_W_PX + SPINE_W_PX + FRONT_W_PX}px (should = {CANVAS_W})")

# ── Create canvas ──────────────────────────────────────────
canvas = Image.new("RGB", (CANVAS_W, CANVAS_H), (255, 255, 255))

# ── Place BACK COVER (left) ────────────────────────────────
back = Image.open(BACK_IMG).convert("RGB")
back_resized = back.resize((BACK_W_PX, ZONE_H_PX), RESAMPLE)
canvas.paste(back_resized, (0, 0))
print(f"✅ Back cover placed: 0 → {BACK_W_PX}px")

# ── Place SPINE (center) ───────────────────────────────────
spine = Image.open(SPINE_IMG).convert("RGB")
spine_resized = spine.resize((SPINE_W_PX, ZONE_H_PX), RESAMPLE)
canvas.paste(spine_resized, (BACK_W_PX, 0))
print(f"✅ Spine placed: {BACK_W_PX} → {BACK_W_PX + SPINE_W_PX}px")

# ── Place FRONT COVER (right) ──────────────────────────────
front = Image.open(FRONT_IMG).convert("RGB")
front_resized = front.resize((FRONT_W_PX, ZONE_H_PX), RESAMPLE)
canvas.paste(front_resized, (BACK_W_PX + SPINE_W_PX, 0))
print(f"✅ Front cover placed: {BACK_W_PX + SPINE_W_PX} → {BACK_W_PX + SPINE_W_PX + FRONT_W_PX}px")

# ── Save PNG preview ───────────────────────────────────────
canvas.save(OUTPUT_PNG, "PNG")
print(f"\n📸 Preview saved: {OUTPUT_PNG} ({os.path.getsize(OUTPUT_PNG)/1024/1024:.1f} MB)")

# ── Save PDF at exact dimensions ───────────────────────────
# Convert pixels to points for PDF (1 inch = 72 points)
# Image at 300 DPI → save with dpi=(300, 300) so PDF is correct size
canvas.save(OUTPUT_PDF, "PDF", resolution=DPI)
print(f"📄 PDF saved: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF)/1024/1024:.1f} MB)")

# ── Verify ─────────────────────────────────────────────────
import subprocess
result = subprocess.run(["pdfinfo", OUTPUT_PDF], capture_output=True, text=True, timeout=10)
for line in result.stdout.split("\n"):
    if "Page size" in line or "Pages" in line:
        print(f"   {line.strip()}")
