import logging
from src.curated_data import get_random_curated_names
from src.llm import identify_persons_with_llm
from src.agent import get_best_work_for_names
from src.config import settings
from pprint import pprint

logging.basicConfig(level=settings.LOG_LEVEL)

def main():
    # Pull 25 names from Forbes, Time, and Gartner
    names = get_random_curated_names(count=25)
    print(f"Data Source: Curated (Forbes, Time, Gartner)")
    print(f"Selected {len(names)} names. Showing first 10:")
    pprint(names[:10])

    # Process a subset with LLM (top 10 for efficiency)
    llm_identifications = identify_persons_with_llm(names, top_k=10)
    print("\nLLM identifications (top 10):")
    pprint(llm_identifications)

    best_work = get_best_work_for_names(list(llm_identifications.keys()), limit=10)
    print("\nBest work suggestions:")
    pprint(best_work)

if __name__ == "__main__":
    main()
