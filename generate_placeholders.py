from PIL import Image, ImageDraw
import os, random

assets_base = "assets/birthday/base"

def draw_confetti(path, size=(512,512)):
    img = Image.new("RGBA", size, (0,0,0,0))
    d = ImageDraw.Draw(img)
    palette = [(255,99,132,200),(54,162,235,200),(255,206,86,200),(75,192,192,200),(153,102,255,200)]
    for _ in range(240):
        x = random.randint(0,size[0]-1)
        y = random.randint(0,size[1]-1)
        r = random.randint(2,6)
        d.ellipse((x-r,y-r,x+r,y+r), fill=random.choice(palette))
    img.save(path, "PNG")

def draw_gift(path, size=(512,512)):
    img = Image.new("RGBA", size, (0,0,0,0))
    d = ImageDraw.Draw(img)
    w,h = size
    d.rounded_rectangle((w*0.15,h*0.35,w*0.85,h*0.85), radius=30, fill=(255,180,180,255))
    d.rectangle((w*0.47,h*0.35,w*0.53,h*0.85), fill=(220,60,60,255))
    d.rectangle((w*0.15,h*0.57,w*0.85,h*0.63), fill=(220,60,60,255))
    img.save(path, "PNG")

def draw_balloons(path, size=(512,512)):
    img = Image.new("RGBA", size, (0,0,0,0))
    d = ImageDraw.Draw(img)
    w,h = size
    colors = [(255,99,132,230),(54,162,235,230),(255,206,86,230)]
    centers = [(w*0.35,h*0.45),(w*0.5,h*0.4),(w*0.65,h*0.48)]
    for (cx,cy),col in zip(centers, colors):
        d.ellipse((cx-90,cy-120,cx+90,cy+120), fill=col, outline=(255,255,255,255), width=4)
    img.save(path, "PNG")

os.makedirs(assets_base, exist_ok=True)
draw_confetti(os.path.join(assets_base, "confetti.png"))
draw_gift(os.path.join(assets_base, "gift.png"))
draw_balloons(os.path.join(assets_base, "balloons.png"))
print("✅ Placeholder images created.")
