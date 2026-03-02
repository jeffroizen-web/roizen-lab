#!/usr/bin/env python3
"""
Remap fluorescence microscopy composites from original dye colors to purple/gold.

Three composites, each with different dye combinations requiring different strategies:

1. Brain PVN: Green (Sim1) + Red/Orange (DsRed) on black.
   Strategy: Standard channel remap. Green → Purple, Red → Gold.

2. VDR C2C12: Blue (DAPI) + Green (GFP) on black.
   Strategy: Channel remap. Green → Gold, Blue → Purple.

3. 3T3-L1: Magenta/Pink (RFP) + Blue (DAPI) on black.
   Strategy: Ratio-based separation with histogram equalization.
   Problem: Both RFP and DAPI contribute to R and B channels (green is zero).
   RFP emits in magenta range (high R + some B), DAPI emits in blue (high B + some R).
   Solution: Use R/(R+B) ratio, spatially smooth, histogram-equalize, sigmoid-sharpen
   to separate the two overlapping dye signals.

Target palette:
  - Purple: rich blue-violet (#6B0FEB / 105, 15, 235)
  - Gold: warm amber (#E6B91E / 230, 185, 30)
"""

import numpy as np
from PIL import Image
from scipy import ndimage
import os

BASE = "/Users/roizenj/Desktop/Claude Apps/Roizen Lab"

COMPOSITES = [
    ("hero-microscopy-composite-1-brain-pvn.png",
     "hero-microscopy-composite-1-brain-pvn-purple-gold.png",
     "pvn"),
    ("hero-microscopy-composite-2-vdr-c2c12.png",
     "hero-microscopy-composite-2-vdr-c2c12-purple-gold.png",
     "vdr"),
    ("hero-microscopy-composite-3-3t3l1-differentiation.png",
     "hero-microscopy-composite-3-3t3l1-differentiation-purple-gold.png",
     "ratio"),
]

# --- Color targets (0-255) ---
PURPLE = np.array([105, 15, 235])    # rich blue-violet
GOLD = np.array([230, 185, 30])      # warm amber-gold
COLOC_BOOST = 1.3


def sigmoid(x, center=0.5, steepness=8.0):
    """Push values away from center using a logistic curve."""
    return 1.0 / (1.0 + np.exp(-steepness * (x - center)))


def remap_pvn(input_path, output_path):
    """
    Brain PVN: Green (Sim1) + Red/Orange (DsRed) on black.
    Luminance-based dual-tone: bright regions → gold, dim regions → purple.
    This works well because the orange/cyan originals don't have clean
    channel separation — luminance-based approach produces better results.
    """
    img = Image.open(input_path).convert("RGB")
    arr = np.array(img, dtype=np.float64)

    r = arr[:, :, 0]
    g = arr[:, :, 1]
    b = arr[:, :, 2]

    r_norm = r / 255.0
    g_norm = g / 255.0
    b_norm = b / 255.0

    # Co-localization: where both green and red are present
    coloc = np.minimum(r_norm, g_norm)
    g_independent = np.clip(g_norm - coloc, 0, 1)
    r_independent = np.clip(r_norm - coloc, 0, 1)

    # Green → Purple, Red → Gold, overlap → boosted blend
    out_r = (g_independent * PURPLE[0] +
             r_independent * GOLD[0] +
             coloc * COLOC_BOOST * (PURPLE[0] * 0.4 + GOLD[0] * 0.6))

    out_g = (g_independent * PURPLE[1] +
             r_independent * GOLD[1] +
             coloc * COLOC_BOOST * (PURPLE[1] * 0.3 + GOLD[1] * 0.7))

    out_b = (g_independent * PURPLE[2] +
             r_independent * GOLD[2] +
             coloc * COLOC_BOOST * (PURPLE[2] * 0.5 + GOLD[2] * 0.5))

    # Blue channel as subtle cool tint (independent of green/red)
    b_independent = np.clip(b_norm - np.maximum(r_norm, g_norm) * 0.5, 0, 1)
    out_r += b_independent * 80
    out_g += b_independent * 30
    out_b += b_independent * 180

    out = np.stack([
        np.clip(out_r, 0, 255),
        np.clip(out_g, 0, 255),
        np.clip(out_b, 0, 255),
    ], axis=-1).astype(np.uint8)

    Image.fromarray(out).save(output_path, quality=95)
    print(f"  Saved: {output_path}")


def remap_vdr(input_path, output_path):
    """
    VDR C2C12: Blue (DAPI nuclei) + Green (GFP-tagged VDR) on black.
    Red channel is essentially zero.
    Channel remap: Green (GFP dye) → Gold, Blue (DAPI dye) → Purple.
    This is faithful to the actual biology (GFP is the interesting signal).
    """
    img = Image.open(input_path).convert("RGB")
    arr = np.array(img, dtype=np.float64)

    g = arr[:, :, 1]  # GFP signal → will become gold
    b = arr[:, :, 2]  # DAPI signal → will become purple

    g_norm = g / 255.0
    b_norm = b / 255.0

    # Co-localization: where both DAPI and GFP are present
    coloc = np.minimum(g_norm, b_norm)
    g_independent = np.clip(g_norm - coloc, 0, 1)
    b_independent = np.clip(b_norm - coloc, 0, 1)

    # Green (GFP) → Gold, Blue (DAPI) → Purple
    out_r = (g_independent * GOLD[0] +
             b_independent * PURPLE[0] +
             coloc * COLOC_BOOST * (GOLD[0] * 0.5 + PURPLE[0] * 0.5))

    out_g = (g_independent * GOLD[1] +
             b_independent * PURPLE[1] +
             coloc * COLOC_BOOST * (GOLD[1] * 0.4 + PURPLE[1] * 0.6))

    out_b = (g_independent * GOLD[2] +
             b_independent * PURPLE[2] +
             coloc * COLOC_BOOST * (GOLD[2] * 0.3 + PURPLE[2] * 0.7))

    out = np.stack([
        np.clip(out_r, 0, 255),
        np.clip(out_g, 0, 255),
        np.clip(out_b, 0, 255),
    ], axis=-1).astype(np.uint8)

    Image.fromarray(out).save(output_path, quality=95)
    print(f"  Saved: {output_path}")


def remap_ratio(input_path, output_path):
    """
    Ratio-based remap for images where dyes share channels (e.g., 3T3-L1).

    When two fluorescent dyes both contribute to the same color channels,
    simple channel separation fails. Instead, we:
    1. Compute the R/(R+B) ratio as a continuous dye-identity signal
    2. Spatially smooth the ratio (adjacent pixels from the same structure
       should have similar dye identity, reducing CCD sensor noise)
    3. Histogram-equalize the smoothed ratio so that the full purple-to-gold
       color range is used evenly (maximizes visual separation)
    4. Apply sigmoid sharpening to push ambiguous pixels toward their
       dominant dye identity
    5. Mix purple/gold colors proportionally, scaled by luminance
    6. Boost saturation in well-separated regions
    """
    img = Image.open(input_path).convert("RGB")
    arr = np.array(img, dtype=np.float64)

    r = arr[:, :, 0]
    b = arr[:, :, 2]

    # === LUMINANCE ===
    luminance = np.sqrt(r**2 + b**2) / np.sqrt(2)
    lum_norm = luminance / 255.0

    # Tone curve: lift shadows gently, compress highlights slightly
    lum_curved = np.where(
        lum_norm < 0.5,
        np.power(lum_norm * 2, 0.75) / 2,
        1.0 - np.power((1.0 - lum_norm) * 2, 1.1) / 2
    )

    # === RATIO-BASED SEPARATION ===
    total = r + b + 1e-6
    rfp_raw = r / total  # 0 = pure DAPI (blue), 1 = pure RFP (red/magenta)

    # Spatial smoothing of ratio map (sigma=3 for structural disambiguation)
    rfp_smooth = ndimage.gaussian_filter(rfp_raw, sigma=3.0)

    # === HISTOGRAM EQUALIZATION (bright regions only) ===
    bright_mask = luminance > 12
    rfp_flat = rfp_smooth[bright_mask]

    sorted_order = np.argsort(rfp_flat)
    ranks = np.empty_like(rfp_flat)
    ranks[sorted_order] = np.linspace(0, 1, len(rfp_flat))

    rfp_equalized = np.zeros_like(rfp_smooth)
    rfp_equalized[bright_mask] = ranks

    # === SIGMOID SHARPENING ===
    rfp_sig = sigmoid(rfp_equalized, center=0.5, steepness=8.0)
    dapi_sig = 1.0 - rfp_sig

    # === COLOR MIXING ===
    out_r = lum_curved * (dapi_sig * PURPLE[0] + rfp_sig * GOLD[0])
    out_g = lum_curved * (dapi_sig * PURPLE[1] + rfp_sig * GOLD[1])
    out_b = lum_curved * (dapi_sig * PURPLE[2] + rfp_sig * GOLD[2])

    # === SATURATION BOOST for well-separated regions ===
    separation = np.clip(np.abs(rfp_equalized - 0.5) * 2, 0, 1)
    sat_boost = 1.0 + separation * 0.45

    gray = (out_r + out_g + out_b) / 3.0
    out_r = gray + (out_r - gray) * sat_boost
    out_g = gray + (out_g - gray) * sat_boost
    out_b = gray + (out_b - gray) * sat_boost

    # === Clean black background ===
    dark_mask = luminance < 8
    out_r[dark_mask] = 0
    out_g[dark_mask] = 0
    out_b[dark_mask] = 0

    out = np.stack([
        np.clip(out_r, 0, 255),
        np.clip(out_g, 0, 255),
        np.clip(out_b, 0, 255),
    ], axis=-1).astype(np.uint8)

    Image.fromarray(out).save(output_path, quality=95)
    print(f"  Saved: {output_path}")


REMAP_FN = {
    "pvn": remap_pvn,
    "vdr": remap_vdr,
    "ratio": remap_ratio,
}


if __name__ == "__main__":
    for src, dst, method in COMPOSITES:
        src_path = os.path.join(BASE, src)
        dst_path = os.path.join(BASE, dst)
        if not os.path.exists(src_path):
            print(f"  SKIP (not found): {src}")
            continue
        print(f"Remapping ({method}): {src}")
        REMAP_FN[method](src_path, dst_path)

    print("\nDone. Check the -purple-gold.png files.")
