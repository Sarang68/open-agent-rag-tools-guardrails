from app.config import settings
from app.guardrails.profanity import contains_profanity

def guardrail_check(user_input: str) -> tuple[bool, str]:
    if settings.ENABLE_PROFANITY_FILTER and contains_profanity(user_input):
        return False, "Request blocked by guardrails (profanity)."
    return True, ""

