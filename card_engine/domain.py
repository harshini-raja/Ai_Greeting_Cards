from dataclasses import dataclass

@dataclass(frozen=True)
class CardRequest:
    occasion: str
    recipient: str
    sender: str
    tone: str = "warm"
    language: str = "en"
    template_id: str = "birthday_basic_v1"

@dataclass(frozen=True)
class CardResult:
    png_path: str
    template_id: str
    message_used: str
