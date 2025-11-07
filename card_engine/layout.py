# card_engine/layout.py
from typing import Tuple

def frac_to_px(x: float, y: float, w: float, h: float, W: int, H: int) -> Tuple[int,int,int,int]:
    """Convert fractional (0..1) rect to pixels on a W x H canvas."""
    return int(x * W), int(y * H), int(w * W), int(h * H)

def anchor_pos(ax: int, ay: int, aw: int, ah: int, iw: int, ih: int, anchor: str):
    """Place an image (iw, ih) inside anchor rect (ax,ay,aw,ah) per anchor keyword."""
    cx = ax + aw // 2
    cy = ay + ah // 2
    left, top, right, bottom = ax, ay, ax + aw, ay + ah
    mapping = {
        "topleft":     (left, top),
        "top":         (cx - iw // 2, top),
        "topright":    (right - iw, top),
        "left":        (left, cy - ih // 2),
        "center":      (cx - iw // 2, cy - ih // 2),
        "right":       (right - iw, cy - ih // 2),
        "bottomleft":  (left, bottom - ih),
        "bottom":      (cx - iw // 2, bottom - ih),
        "bottomright": (right - iw, bottom - ih),
    }
    return mapping.get(anchor, (left, top))
