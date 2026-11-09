"""Local JSON storage for good things."""
import json
from datetime import datetime
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
DATA_FILE = DATA_DIR / "good_things.json"


def load_good_things() -> list[dict]:
    if not DATA_FILE.exists():
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def save_good_thing(text: str) -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    good_things = load_good_things()
    good_things.append(
        {
            "date": datetime.now().isoformat(timespec="seconds"),
            "text": text,
        }
    )
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(good_things, f, ensure_ascii=False, indent=2)
