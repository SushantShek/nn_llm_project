import logging
import json
import re
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from src.curated_data import get_random_curated_names
from src.llm import identify_persons_with_llm
from src.config import settings

# Initialize logger
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(title="Person Finder AI")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

def clean_json_string(s: str) -> str:
    """Extracts JSON content from Markdown-style code blocks if present."""
    s = s.strip()
    # Handle ```json ... ``` blocks
    match = re.search(r"```json\s*(.*?)\s*```", s, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Handle ``` ... ``` blocks
    match = re.search(r"```\s*(.*?)\s*```", s, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Handle cases where there might be text before/after the first { and last }
    match = re.search(r"(\{.*\})", s, re.DOTALL)
    if match:
        return match.group(1).strip()
    return s

@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes"""
    logger.info("Health check: OK")
    return {"status": "healthy", "message": "Person Finder API is running"}

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("static/index.html", "r") as f:
        return f.read()

@app.get("/find")
async def find_people():
    try:
        # Get random names from curated sources
        names = get_random_curated_names(count=25)
        
        # Identify with LLM (using top 10 for speed in UI)
        identifications = identify_persons_with_llm(names, top_k=10)
        
        results = []
        for name, raw_content in identifications.items():
            try:
                # Clean and parse the LLM output
                cleaned = clean_json_string(raw_content)
                parsed = json.loads(cleaned)
                results.append({
                    "name": name,
                    "description": parsed.get("description", "No description available"),
                    "unique_ability": parsed.get("unique_ability", "No ability found")
                })
            except Exception as e:
                logger.error(f"Failed to parse LLM output for {name}: {e}")
                logger.debug(f"Raw output for {name}: {raw_content}")
                results.append({
                    "name": name,
                    "description": "Error parsing LLM response",
                    "unique_ability": "N/A"
                })
        
        return {"results": results}
    except Exception as e:
        logger.error(f"Internal Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
