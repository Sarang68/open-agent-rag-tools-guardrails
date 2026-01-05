import re

PROFANITY = ["badword1", "badword2"]  # expand later

def contains_profanity(text: str) -> bool:
    t = text.lower()
    for w in PROFANITY:
        if re.search(rf"\b{re.escape(w)}\b", t):
            return True
    return False

