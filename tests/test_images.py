"""Modern-image-format guard (web-quality PR-2, gap #2, 2026-07-01).

The site's raster images were modernized to WebP: content <img> are wrapped in
<picture> with a WebP <source> + the original jpg/png as fallback; the hero CSS
background uses image-set() with a WebP + jpg fallback. Photos/hero are lossy
q80; the science figures are lossless WebP (crisp lines/text).

Guards:
- every WebP referenced by the page exists on disk,
- every content <img> pointing at a converted raster is wrapped in a <picture>
  with a matching WebP <source> (no un-modernized large raster),
- the hero background serves WebP via image-set with a jpg fallback,
- the original raster fallbacks still exist (progressive enhancement intact).

CWV (LCP/CLS/INP) is verified at deploy via Lighthouse — NOT measurable in this
environment; this guard covers correctness of the format wiring, not the metric.

Run: python3 -m pytest tests/test_images.py -q
"""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HTML = (ROOT / "compare-purple-gold.html").read_text()

# Content images that were converted (the two 8K institution logos were left as PNG).
CONVERTED = {
    "photos/1760650722715.jpg", "photos/benchwork.jpg", "photos/dryIce.jpg",
    "photos/lab-group-hires.jpg", "photos/pipette.jpg", "photos/roizen-portrait.jpg",
    "photos/talkingWide.jpg",
    "extracted-figures/curated-for-website/q1-causation.png",
    "extracted-figures/curated-for-website/q4-dose-response.png",
    "extracted-figures/curated-for-website/q5-diabetes-prevention.png",
    "extracted-figures/from-archivist/reverse-causation-bmi-vitd.png",
}


def test_referenced_webp_exist_on_disk():
    for srcset in re.findall(r'<source type="image/webp" srcset="([^"]+)">', HTML):
        assert (ROOT / srcset).exists(), f"WebP <source> references a missing file: {srcset}"


def test_converted_images_are_picture_wrapped():
    """Each converted raster must appear as an <img> inside a <picture> with a
    matching WebP <source> — and its WebP + original fallback both exist."""
    missing_wrap, missing_file = [], []
    for raster in CONVERTED:
        webp = raster.rsplit(".", 1)[0] + ".webp"
        pat = re.compile(
            r'<picture><source type="image/webp" srcset="' + re.escape(webp) + r'">'
            r'<img\b[^>]*src="' + re.escape(raster) + r'"[^>]*></picture>')
        if not pat.search(HTML):
            missing_wrap.append(raster)
        if not (ROOT / webp).exists() or not (ROOT / raster).exists():
            missing_file.append(raster)
    assert not missing_wrap, f"converted rasters not <picture>-wrapped with WebP: {missing_wrap}"
    assert not missing_file, f"converted raster or its WebP missing on disk: {missing_file}"


def test_hero_background_uses_webp_imageset_with_fallback():
    hero = re.search(r'\.hero\s*\{[^}]*\}', HTML)
    assert hero, ".hero rule not found"
    body = hero.group(0)
    assert "image-set(" in body, "hero background missing image-set()"
    assert "hero-microscopy-composite-2-vdr-c2c12.webp" in body, "hero image-set missing WebP source"
    assert "hero-microscopy-composite-2-vdr-c2c12.jpg" in body, "hero missing jpg fallback"
    assert (ROOT / "hero-microscopy-composite-2-vdr-c2c12.webp").exists()
