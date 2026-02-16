import random
from typing import List

FORBES_NAMES = [
    "Shaboozey", "Drew Afualo", "Jayson Tatum", "Bobbi Althoff", "Xandra Pohl",
    "Aidan Gomez", "Demi Guo", "Noah Kahan", "Aadit Palicha", "Kaivalya Vohra",
    "Rashmika Mandanna", "Aadit Palicha", "Ankit Alok Bagaria", "Viraj Khanna",
    "Shreyans Chopra", "Spriha Biswas", "Ajinkya Dhariya", "Anupam Kumar",
    "Arvind Bhardwaj", "Navajith Karkera"
]

TIME_NAMES = [
    "Dua Lipa", "Patrick Mahomes", "Taraji P. Henson", "Yulia Navalnaya",
    "21 Savage", "Alia Bhatt", "America Ferrera", "Fantasia Barrino",
    "Jack Antonoff", "James McBride", "Jenny Holzer", "Jonathan Anderson",
    "Kate Hudson", "Kelly Ripa", "Kingsley Ben-Adir", "LaToya Ruby Frazier",
    "Leslie Odom Jr.", "Mark Zuckerberg", "Maren Morris", "Michael J. Fox",
    "Michelle Obama", "Naomi Watts", "Ryan Reynolds", "Sofia Coppola"
]

GARTNER_NAMES = [
    "Eugene A. Hall", "Craig Safian", "Yvonne Genovese", "Scott Hensel",
    "Claire Herkes", "Akhil Jain", "Thomas Kim", "Robin Kranich",
    "John Rinello", "Altaf Rupani", "Dick van Ham", "Jim Wartinbee"
]

def get_random_curated_names(count: int = 25) -> List[str]:
    """
    Combines names from Forbes, Time, and Gartner and returns a random sample.
    """
    all_names = list(set(FORBES_NAMES + TIME_NAMES + GARTNER_NAMES))
    if count > len(all_names):
        count = len(all_names)
    return random.sample(all_names, count)
