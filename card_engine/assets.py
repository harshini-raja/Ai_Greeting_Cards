import os
from typing import Dict

def resolve_assets(occasion: str) -> Dict[str, str]:
    base_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", occasion, "base")
    return {
        "confetti_tl": os.path.join(base_dir, "confetti.png"),
        "gift_tr": os.path.join(base_dir, "gift.png"),
        "balloons_bl": os.path.join(base_dir, "balloons.png"),
    }