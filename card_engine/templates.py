import json
from dataclasses import dataclass

@dataclass
class CanvasSpec:
    width: int
    height: int
    background: str = "#FFFFFF"

@dataclass
class Slot:
    key: str
    x: float
    y: float
    w: float
    h: float
    anchor: str = "topleft"
    fit: str = "contain"

@dataclass
class TextBox:
    x: float
    y: float
    w: float
    h: float
    align: str = "center"
    color: str = "#111111"
    font: str = ""
    min_px: int = 24
    max_px: int = 96

@dataclass
class TemplateSpec:
    id: str
    canvas: CanvasSpec
    slots: list
    text: TextBox
    footer: TextBox | None = None

def load_template(path: str) -> TemplateSpec:
    with open(path, "r") as f:
        data = json.load(f)
    c = data["canvas"]
    canvas = CanvasSpec(c["width"], c["height"], c.get("background","#FFFFFF"))
    slots = [Slot(**s) for s in data.get("slots",[])]
    t = data["text"]; text = TextBox(**t)
    footer = TextBox(**data["footer"]) if data.get("footer") else None
    return TemplateSpec(id=data["id"], canvas=canvas, slots=slots, text=text, footer=footer)