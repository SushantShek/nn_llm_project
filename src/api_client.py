from typing import Dict, Any
import requests
import requests_cache
import logging

logger = logging.getLogger(__name__)
requests_cache.install_cache("randomuser_cache", expire_after=300)

API_URL = "https://randomuser.me/api/"


def fetch_random_users(results: int = 20, seed: int | None = None) -> Dict[str, Any]:
    params = {"results": results}
    if seed:
        params["seed"] = seed
    logger.info("Fetching %d random users", results)
    resp = requests.get(API_URL, params=params, timeout=10, verify=False)
    resp.raise_for_status()
    return resp.json()
