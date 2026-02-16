from typing import Dict, Any
import requests
import requests_cache
import logging
from src.config import settings

import json
import os
from src.config import settings

logger = logging.getLogger(__name__)
requests_cache.install_cache("randomuser_cache", expire_after=settings.CACHE_EXPIRATION)

def load_mock_data() -> Dict[str, Any]:
    mock_path = os.path.join(os.path.dirname(__file__), "mock_data.json")
    with open(mock_path, "r") as f:
        return json.load(f)

def fetch_random_users(results: int = 20, seed: int | None = None) -> Dict[str, Any]:
    params = {"results": results}
    if seed:
        params["seed"] = seed
    logger.info("Fetching %d random users", results)
    try:
        resp = requests.get(
            settings.RANDOM_USER_API_URL, 
            params=params, 
            timeout=5, 
            verify=settings.SSL_VERIFY
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("results"):
            return data
        logger.warning("API returned empty results, using mock data fallback")
    except Exception as e:
        logger.error("API request failed: %s. Using mock data fallback", e)
    
    return load_mock_data()
