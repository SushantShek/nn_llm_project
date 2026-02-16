import os
import json
from langchain_openai import ChatOpenAI
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, wait_exponential, stop_after_attempt
from typing import List, Dict
import logging
import requests
from src.config import settings

logger = logging.getLogger(__name__)

@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(3))
def call_llm_single(prompt: str, max_tokens: int = 512) -> str:
    if not settings.OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set in environment or settings")
        
    llm = ChatOpenAI(
        model=settings.MODEL_NAME,
        openai_api_key=settings.OPENAI_API_KEY, 
        max_tokens=max_tokens
    )
    # Using default session which respects SSL settings if possible, 
    # but langchain handle its own requests. 
    # For custom backend with SSL check:
    out = llm.invoke(input=prompt)
    if hasattr(out, 'content'):
        return out.content.strip()
    return str(out).strip()

def identify_persons_with_llm(names: List[str], top_k: int = 5) -> Dict[str, str]:
    results = {}
    subset = names[:top_k]
    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = {ex.submit(call_llm_single, f"Who is {name}? generate a concise (2-3 sentences) and creative description of this person. "
        "DO NOT include any Personally Identifiable Information (PII) such as email addresses, phone numbers, or specific street addresses in the description. "
        "Also, invent a 'unique ability' for them based on or inspired by their profile information. Ensure the unique ability is imaginative and logically (even if creatively) tied to some aspect of their data. "
        "Your output MUST be a pure JSON object with two keys: 'description' and 'unique_ability'."): name for name in subset}
        for fut in as_completed(futures):
            name = futures[fut]
            try:
                results[name] = fut.result()
            except Exception as e:
                logger.error("LLM call failed for %s: %s", name, e)
                results[name] = json.dumps({
                    "description": "LLM identification failed",
                    "unique_ability": "N/A"
                })
    return results
