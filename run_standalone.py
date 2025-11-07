from card_engine.domain import CardRequest
from card_engine.card_service import process_card_request
import os, sys
sys.path.append(os.path.dirname(__file__))


if __name__ == "__main__":
    req = CardRequest(occasion="birthday", recipient="Asha", sender="Harshini")
    greeting = "Happy Birthday, Asha! Wishing you laughter, health, and endless adventures ahead."
    out_dir = os.path.join(os.path.dirname(__file__), "output")
    result = process_card_request(req, greeting, out_dir)
    print("✅ Generated:", result.png_path)