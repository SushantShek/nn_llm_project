import os
from langchain_huggingface import HuggingFaceEndpoint

from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, PromptTemplate
from concurrent.futures import ThreadPoolExecutor, as_completed
from tenacity import retry, wait_exponential, stop_after_attempt
from typing import List, Dict
import logging

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import requests
from huggingface_hub import configure_http_backend

os.environ["HF_API_KEY"]="your_hf_api_key_here"

def backend_factory() -> requests.Session:
    session = requests.Session()
    session.verify = False
    return session

configure_http_backend(backend_factory=backend_factory)

logger = logging.getLogger(__name__)

MODEL = os.environ.get("gpt-4", "google/flan-t5-small")
API_KEY = os.environ.get("OPENAI_API_KEY")

@retry(wait=wait_exponential(multiplier=1, min=1, max=10), stop=stop_after_attempt(1))
def call_llm_single(prompt: str, max_tokens: int = 256) -> str:
    llm = ChatOpenAI(model=MODEL,openai_api_key=API_KEY, max_tokens=max_tokens)
    out = llm.invoke(input=prompt)
    return out.strip()

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
                results[name] = "LLM error"
    return results
