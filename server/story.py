import os
import random
from typing import Dict, Any, Tuple
from .game_data import PLACES, DEFAULT_CENTER, DEFAULT_ZOOM
from math import radians, sin, cos, sqrt, atan2, exp

try:
    # Optional OpenAI embellisher
    from openai import OpenAI
    _OPENAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else None
except Exception:
    _OPENAI = None

def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def score_from_km(distance_km: float) -> int:
    return int(round(5000 * exp(-distance_km / 2000.0)))

def pick_place() -> Dict[str, Any]:
    place = random.choice(PLACES)
    name_seeds = ["Ava", "Kai", "Mina", "Leo", "Zara", "Niko", "Ravi", "Mei", "Ilya", "Sofi"]
    last_seeds = ["Park", "Silva", "Okoye", "Nguyen", "Ivanov", "Haddad", "Singh", "Moretti", "Garcia", "O'Neil"]
    character = f"{random.choice(name_seeds)} {random.choice(last_seeds)}"
    tidbits = random.sample(place.tidbits, k=min(2, len(place.tidbits)))
    eats = random.sample(place.cuisine, k=min(2, len(place.cuisine)))
    habits = random.sample(place.habits, k=min(2, len(place.habits)))

    base_story = (
        f"Hello! I'm {character}. My mornings usually involve {habits[0]}, and I often grab {eats[0]} on the go. "
        f"On weekends, I love exploring {tidbits[0]}. People here care about {tidbits[1]} and you'll hear plenty about it. "
        f"In the evenings, {habits[1]} is my routine, ideally followed by {eats[1]} with friends."
    )

    if _OPENAI:
        try:
            prompt = (
                "You are a travel game narrator. Rewrite the following short persona into a playful, vivid, "
                "two-sentence monologue that hints at their city without naming it. Keep it concise:\n\n"
                f"{base_story}\n\nTwo-sentence monologue:"
            )
            resp = _OPENAI.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role":"user","content":prompt}],
                temperature=0.9,
                max_tokens=140,
            )
            monologue = resp.choices[0].message.content.strip()
        except Exception:
            monologue = base_story
    else:
        monologue = base_story

    return {
        "place": {
            "city": place.city,
            "country": place.country,
            "lat": place.lat,
            "lon": place.lon,
            "region": place.region,
        },
        "character": character,
        "monologue": monologue,
        "hints": {
            "cuisine": eats,
            "habits": habits,
            "vibes": tidbits,
        },
        "mapDefault": {"center": DEFAULT_CENTER, "zoom": DEFAULT_ZOOM},
    }

def evaluate_guess(secret: Tuple[float, float], guess: Tuple[float, float]):
    dist_km = haversine_km(secret[0], secret[1], guess[0], guess[1])
    score = score_from_km(dist_km)
    return dist_km, score
