import os
from PIL import ImageDraw
from .domain import CardRequest, CardResult
from .templates import load_template
from .assets import resolve_assets
from .render import compose
from .typography import fit_text

def process_card_request(req: CardRequest, greeting_text: str, out_dir: str) -> CardResult:
    # choose a template file safely with fallbacks
    tpl_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")
    candidates = []
    # prefer an explicit template_id on the request
    if getattr(req, "template_id", None):
        tid = req.template_id
        candidates.append(tid if tid.endswith(".json") else f"{tid}.json")
        # handle common suffixes like _v1: turn "birthday_basic_v1" -> "birthday_basic.json"
        base = tid.split("_v")[0]
        if base and not base.endswith(".json"):
            candidates.append(f"{base}.json")

    # try names derived from the occasion
    if getattr(req, "occasion", None):
        candidates.append(f"{req.occasion}.json")
        candidates.append(f"birthday_{req.occasion}.json")

    # some sensible defaults
    candidates.append("birthday_basic.json")

    # list available templates and try those as a final fallback
    try:
        available = [f for f in os.listdir(tpl_dir) if f.lower().endswith('.json')]
    except Exception:
        available = []
    candidates.extend(available)

    tpl_path = None
    tried = []
    for name in candidates:
        if not name:
            continue
        p = os.path.join(tpl_dir, name)
        tried.append(p)
        if os.path.exists(p):
            tpl_path = p
            break

    if tpl_path is None:
        raise FileNotFoundError(
            f"No template found. Tried: {tried}. Available templates: {available}"
        )

    tpl = load_template(tpl_path)

    mapping = resolve_assets(req.occasion)
    img = compose(tpl, mapping)
    draw = ImageDraw.Draw(img)

    # text box
    tx, ty = int(tpl.text.x*img.width), int(tpl.text.y*img.height)
    tw, th = int(tpl.text.w*img.width), int(tpl.text.h*img.height)
    font, lines = fit_text(draw, greeting_text, (tx,ty,tw,th), tpl.text.font, tpl.text.min_px, tpl.text.max_px, tpl.text.align)

    # vertical center
    line_h = font.getbbox("Ay")[3] - font.getbbox("Ay")[1]
    total_h = line_h * len(lines)
    y = ty + (th - total_h)//2
    for ln in lines:
        w = draw.textlength(ln, font=font)
        if tpl.text.align == "center":
            x = tx + (tw - w)//2
        elif tpl.text.align == "right":
            x = tx + tw - w
        else:
            x = tx
        draw.text((x, y), ln, fill=tpl.text.color, font=font)
        y += line_h

    # footer
    if tpl.footer:
        fx, fy = int(tpl.footer.x*img.width), int(tpl.footer.y*img.height)
        fw, fh = int(tpl.footer.w*img.width), int(tpl.footer.h*img.height)
        footer = f"With love, {req.sender}"
        ffont, flines = fit_text(draw, footer, (fx,fy,fw,fh), tpl.footer.font, 14, 36, "center")
        w = draw.textlength(footer, font=ffont)
        line_h = ffont.getbbox("Ay")[3] - ffont.getbbox("Ay")[1]
        draw.text((fx + (fw - w)//2, fy + (fh - line_h)//2), footer, fill=tpl.text.color, font=ffont)

    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{req.recipient}_card.png")
    img.convert("RGB").save(out_path, "PNG")
    return CardResult(png_path=out_path, template_id=tpl.id, message_used=greeting_text)