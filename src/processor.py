from typing import List, Dict
from datetime import datetime
import logging
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class Person(BaseModel):
    first: str
    last: str
    dob_date: datetime

def parse_person(raw: Dict) -> Person:
    name = raw["name"]
    dob = raw["dob"]["date"]
    return Person(first=name["first"], last=name["last"], dob_date=datetime.fromisoformat(dob.rstrip("Z")))

def format_names_after_2000(data: Dict) -> List[str]:
    results = data.get("results", [])
    people = []
    logger.debug("Processing %d results", len(results))
    for raw in results:
        try:
            p = parse_person(raw)
            logger.debug("Parsed person: %s %s, DOB Year: %d", p.first, p.last, p.dob_date.year)
            if p.dob_date.year > 2000:
                full = f"{p.first.strip().title()} {p.last.strip().title()}"
                people.append(full)
        except Exception as e:
            logger.warning("Skipping entry due to parse error: %s", e)
    logger.info("Found %d people born after 2000", len(people))
    return people
