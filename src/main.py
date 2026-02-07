import logging
from src.api_client import fetch_random_users
from src.processor import format_names_after_2000
from src.llm import identify_persons_with_llm
from src.agent import get_best_work_for_names
import os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()
logging.basicConfig(level=os.environ.get("LOG_LEVEL", "INFO"))

def main():
    raw = fetch_random_users(results=20)
    names = format_names_after_2000(raw)
    print("Filtered names:")
    pprint(names)

    llm_identifications = identify_persons_with_llm(names, top_k=5)
    print("\nLLM identifications:")
    pprint(llm_identifications)

    best_work = get_best_work_for_names(list(llm_identifications.keys()), limit=5)
    print("\nBest work suggestions:")
    pprint(best_work)

if __name__ == "__main__":
    main()
