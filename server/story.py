import os
import json
import random
import re
from typing import Dict, Any, Tuple, Optional
from math import radians, sin, cos, sqrt, atan2, exp
from pydantic import BaseModel, Field, ValidationError, field_validator
from .game_data import PLACES, DEFAULT_CENTER, DEFAULT_ZOOM
from collections import deque

# How many recent cities to block; how many times to retry AI before giving up
RECENT_BLOCK = int(os.getenv("AI_RECENT_BLOCK", "10"))
AI_MAX_ATTEMPTS = int(os.getenv("AI_MAX_ATTEMPTS", "4"))

_recent_cities = deque(maxlen=RECENT_BLOCK)  # holds strings like "lisbon|portugal"
_recent_regions = deque(maxlen=RECENT_BLOCK) # optional: for region variety

# =========================
# Config
# =========================
AI_CITY_MODE = os.getenv("AI_CITY_MODE", "0").strip().lower() in {"1", "true", "yes"}
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# =========================
# Pydantic models (AI JSON)
# =========================
class Hints(BaseModel):
    cuisine: list[str] = Field(default_factory=list, max_items=5)
    habits: list[str] = Field(default_factory=list, max_items=5)
    vibes: list[str] = Field(default_factory=list, max_items=5)

class AIPlace(BaseModel):
    city: str
    country: str
    lat: float
    lon: float
    region: str
    character: str
    monologue: str
    hints: Hints

    @field_validator("lat")
    @classmethod
    def _lat_range(cls, v):
        if not (-90 <= v <= 90):
            raise ValueError("lat out of range")
        return v

    @field_validator("lon")
    @classmethod
    def _lon_range(cls, v):
        if not (-180 <= v <= 180):
            raise ValueError("lon out of range")
        return v

    @field_validator("monologue")
    @classmethod
    def _strip(cls, v):
        return (v or "").strip()
    

def _city_key(city: str, country: str) -> str:
    return f"{(city or '').strip().lower()}|{(country or '').strip().lower()}"

def _region_key(region: str) -> str:
    return (region or "").strip().lower()

# =========================
# Distance & scoring
# =========================
def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371.0
    dlat = radians(lat2 - lat1); dlon = radians(lon2 - lon1)
    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

def score_from_km(distance_km: float) -> int:
    return int(round(5000 * exp(-distance_km / 2000.0)))

# =========================
# Local (fallback) generator
# =========================
def _pick_from_local() -> Dict[str, Any]:
    place = random.choice(PLACES)

    name_seeds = ["Ava","Kai","Mina","Leo","Zara","Niko","Ravi","Mei","Ilya","Sofi"]
    last_seeds = ["Park","Silva","Okoye","Nguyen","Ivanov","Haddad","Singh","Moretti","Garcia","O'Neil"]
    character = f"{random.choice(name_seeds)} {random.choice(last_seeds)}"

    tidbits = random.sample(place.tidbits, k=min(2, len(place.tidbits)))
    eats = random.sample(place.cuisine, k=min(2, len(place.cuisine)))
    habits = random.sample(place.habits, k=min(2, len(place.habits)))

    base_story = (
        f"Hello! I'm {character}. My mornings usually involve {habits[0]}, and I often grab {eats[0]} on the go. "
        f"On weekends, I love exploring {tidbits[0]}. People here care about {tidbits[1]} and you'll hear plenty about it. "
        f"In the evenings, {habits[1]} is my routine, ideally followed by {eats[1]} with friends."
    )

    return {
        "place": {
            "city": place.city, "country": place.country,
            "lat": place.lat, "lon": place.lon, "region": place.region
        },
        "character": character,
        "monologue": base_story,
        "hints": {"cuisine": eats, "habits": habits, "vibes": tidbits},
        "mapDefault": {"center": DEFAULT_CENTER, "zoom": DEFAULT_ZOOM},
        "ai": False,
    }

# =========================
# Helpers for AI JSON output
# =========================
def build_ai_prompt(avoid_cities: list[str], nudge_region: Optional[str]) -> str:
    avoid_block = ""
    if avoid_cities:
        formatted = ", ".join(avoid_cities[:12])
        avoid_block = f"\n- Do NOT pick any of these recent answers: {formatted}"

    region_block = ""
    if nudge_region:
        region_block = f"\n- Prefer a city in a region different from: {nudge_region} (variety requested)."

    return (
        "You are a geography game narrator. Generate ONE round as STRICT JSON (no prose, no backticks).\n"
        "- Pick any real-world city (not necessarily famous)."
        f"{region_block}"
        f"{avoid_block}\n"
        "- Provide accurate lat and lon.\n"
        "- Write a 2-sentence DAILY-ROUTINE description addressing the player in SECOND PERSON (start with 'You ...'). "
        "It must not include names, 'I', or self-introductions. Hints only; do NOT name the city/country.\n"
        "- Include keys: city, country, lat, lon, region, character, monologue, hints {cuisine, habits, vibes}.\n"
        "- Each hints list up to 2–3 items; TOTAL hints across all categories ≤ 5.\n"
        "- Output JSON ONLY."
    )

def _scrub_backticks(s: str) -> str:
    s = s.strip()
    if s.startswith("```"):
        s = re.sub(r"^```(?:json)?\s*|\s*```$", "", s, flags=re.IGNORECASE | re.DOTALL).strip()
    return s

def _redact_leaks(text: str, city: str, country: str) -> str:
    redacted = text
    tokens = {city, country}
    # also scrub any known PLACES tokens as a best-effort guard
    for p in PLACES:
        tokens.add(p.city); tokens.add(p.country)
    for t in sorted({t for t in tokens if t and len(t) >= 3}, key=lambda x: -len(x)):
        redacted = re.sub(rf"\b{re.escape(t)}\b", "[redacted]", redacted, flags=re.IGNORECASE)
    return redacted

# =========================
# OpenAI client (lazy)
# =========================
_openai_client = None
def get_openai_client():
    global _openai_client
    if _openai_client is not None:
        return _openai_client
    key = OPENAI_KEY
    if not key:
        return None
    try:
        from openai import OpenAI
        _openai_client = OpenAI(api_key=key)
        return _openai_client
    except Exception as e:
        print("⚠️ Failed to init OpenAI client:", e)
        _openai_client = None
        return None

def _pick_from_ai() -> Optional[Dict[str, Any]]:
    client = get_openai_client()
    if not client:
        return None

    # Build avoidance list like "Lisbon (Portugal), Tokyo (Japan)"
    human_avoid = [f"{c.split('|')[0].title()} ({c.split('|')[1].title()})" for c in list(_recent_cities)]
    last_region = _recent_regions[-1] if _recent_regions else None
    prompt = build_ai_prompt(human_avoid, last_region.title() if last_region else None)

    for attempt in range(AI_MAX_ATTEMPTS):
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=1.1,   # a touch more diversity
                max_tokens=240,
                presence_penalty=0.2,  # gentle nudge away from repetition (supported for chat/completions)
            )
            raw = (resp.choices[0].message.content or "").strip()
            raw = _scrub_backticks(raw)

            data = json.loads(raw)
            obj = AIPlace(**data)  # validate

            key = _city_key(obj.city, obj.country)
            if key in _recent_cities:
                print(f"↩️ AI returned recent city again ({obj.city}, {obj.country}); retry {attempt+1}/{AI_MAX_ATTEMPTS}")
                # On the next iteration, lightly nudge the prompt again by appending a hint:
                prompt += f"\n- IMPORTANT: Do not choose {obj.city}, {obj.country}."
                continue

            # Accept this city → record it
            _recent_cities.append(key)
            _recent_regions.append(_region_key(obj.region))

            redacted = _redact_leaks(obj.monologue, obj.city, obj.country)
            print("✨ Using AI-city mode (new city from model)")
            return {
                "place": {
                    "city": obj.city, "country": obj.country,
                    "lat": obj.lat, "lon": obj.lon, "region": obj.region
                },
                "character": obj.character,
                "monologue": redacted,
                "hints": obj.hints.model_dump(),
                "mapDefault": {"center": DEFAULT_CENTER, "zoom": DEFAULT_ZOOM},
                "ai": True,
            }

        except (json.JSONDecodeError, ValidationError) as ve:
            print("⚠️ AI JSON issue:", ve)
        except Exception as e:
            print("⚠️ AI generation failed:", e)

    # All attempts failed or kept repeating → give up this round; fallback
    return None

# =========================
# Public API
# =========================
def pick_place(force_mode: Optional[str] = None) -> Dict[str, Any]:
    """
    force_mode:
      - "offline" => always use local list
      - "ai"      => try AI (falls back to local on failure)
      - None      => use env defaults (AI_CITY_MODE + OPENAI_KEY)
    """
    mode = (force_mode or "").strip().lower()
    if mode == "offline":
        return _pick_from_local()

    if mode == "ai":
        bundle = _pick_from_ai()
        if bundle:
            return bundle
        print("⚠️ Forced AI mode failed; falling back to local list")
        return _pick_from_local()

    # default behavior (env-driven)
    if AI_CITY_MODE and OPENAI_KEY:
        bundle = _pick_from_ai()
        if bundle:
            return bundle
        print("⚠️ AI mode failed or repeated cities, falling back to local list")
    return _pick_from_local()

def evaluate_guess(secret: Tuple[float, float], guess: Tuple[float, float]):
    dist_km = haversine_km(secret[0], secret[1], guess[0], guess[1])
    score = score_from_km(dist_km)
    return dist_km, score
