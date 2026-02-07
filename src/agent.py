from src.llm import call_llm_single
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

def fetch_person_best_work(name: str) -> str:
    prompt = (
        f"Given the name '{name}', generate a concise (2-3 sentences) and creative description of this person. "
        "DO NOT include any Personally Identifiable Information (PII) such as email addresses, phone numbers, or specific street addresses in the description. "
        "Also, invent a 'unique ability' for them based on or inspired by their profile information. Ensure the unique ability is imaginative and logically (even if creatively) tied to some aspect of their data. "
        "Your output MUST be a pure JSON object with two keys: 'description' and 'unique_ability'."
    )
    return call_llm_single(prompt)

def get_best_work_for_names(names: List[str], limit: int = 5) -> Dict[str, str]:
    results = {}
    for name in names[:limit]:
        try:
            results[name] = fetch_person_best_work(name)
        except Exception as e:
            logger.error("Agent failed for %s: %s", name, e)
            results[name] = "No details available"
    return results
