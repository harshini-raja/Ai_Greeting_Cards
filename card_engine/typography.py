from PIL import ImageFont, ImageDraw
import textwrap

def load_font(path: str | None, size: int):
    try:
        if path:
            return ImageFont.truetype(path, size=size)
    except Exception:
        pass
    return ImageFont.load_default()

def fit_text(draw: ImageDraw.ImageDraw, text: str, box, font_path: str | None, min_px: int, max_px: int, align: str):
    x,y,w,h = box
    lo, hi = min_px, max_px
    best = (lo, [""])
    while lo <= hi:
        mid = (lo + hi)//2
        font = load_font(font_path, mid)
        # naive wrapping by character width estimate
        lines = []
        for para in text.split("\\n"):
            if not para:
                lines.append("")
                continue
            # estimate wrap by measuring progressively
            words = para.split(" ")
            cur = ""
            for wd in words:
                test = (cur + " " + wd).strip()
                if draw.textlength(test, font=font) <= w:
                    cur = test
                else:
                    if cur:
                        lines.append(cur)
                    cur = wd
            if cur:
                lines.append(cur)
        line_h = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
        total_h = line_h * len(lines)
        max_w = max(draw.textlength(ln, font=font) for ln in lines) if lines else 0
        if total_h <= h and max_w <= w:
            best = (mid, lines)
            lo = mid + 1
        else:
            hi = mid - 1
    size, lines = best
    return load_font(font_path, size), lines