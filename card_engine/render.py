from PIL import Image
from .layout import frac_to_px, anchor_pos

def resize_fit(img: Image.Image, target_w: int, target_h: int, mode: str):
    iw, ih = img.size
    if mode == "cover":
        scale = max(target_w/iw, target_h/ih)
    else:
        scale = min(target_w/iw, target_h/ih)
    nw, nh = max(1,int(iw*scale)), max(1,int(ih*scale))
    return img.resize((nw, nh), Image.LANCZOS)

def compose(template, slot_to_path: dict):
    W,H = template.canvas.width, template.canvas.height
    bg = Image.new("RGBA", (W,H), template.canvas.background)
    # place images
    for slot in template.slots:
        path = slot_to_path.get(slot.key)
        if not path: continue
        try:
            img = Image.open(path).convert("RGBA")
        except Exception:
            continue
        ax, ay, aw, ah = frac_to_px(slot.x, slot.y, slot.w, slot.h, W, H)
        fitted = resize_fit(img, aw, ah, slot.fit)
        px, py = anchor_pos(ax, ay, aw, ah, fitted.size[0], fitted.size[1], slot.anchor)
        bg.alpha_composite(fitted, dest=(px, py))
    return bg