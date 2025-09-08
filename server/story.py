import os
import json
import random
import re
import time
from typing import Dict, Any, Tuple, Optional
from math import radians, sin, cos, sqrt, atan2, exp
from pydantic import BaseModel, Field, ValidationError, field_validator
from collections import deque
from .game_data import PLACES, DEFAULT_CENTER, DEFAULT_ZOOM

RECENT_BLOCK = int(os.getenv("AI_RECENT_BLOCK", "10"))
AI_MAX_ATTEMPTS = int(os.getenv("AI_MAX_ATTEMPTS", "4"))

# Circuit breaker defaults
CB_FAIL_LIMIT = int(os.getenv("AI_CB_FAIL_LIMIT", "3"))          # consecutive parse/generation fails before cooldown
CB_COOLDOWN_SECS = int(os.getenv("AI_CB_COOLDOWN_SECS", "600"))  # 10 min for generic failures
CB_RATELIMIT_SECS = int(os.getenv("AI_CB_RATELIMIT_SECS", "900"))# 15 min for 429
CB_QUOTA_SECS = int(os.getenv("AI_CB_QUOTA_SECS", "3600"))       # 60 min for insufficient_quota / 401/403
CB_INIT_BACKOFF_SECS = int(os.getenv("AI_CB_INIT_BACKOFF", "60"))

_recent_cities = deque(maxlen=RECENT_BLOCK)
_recent_regions = deque(maxlen=RECENT_BLOCK)

AI_CITY_MODE = os.getenv("AI_CITY_MODE", "0").strip().lower() in {"1", "true", "yes"}
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# =========================
# Circuit breaker state
# =========================
_AI_DISABLED_UNTIL: float = 0.0
_AI_CONSEC_FAILS: int = 0

def _now() -> float:
    return time.time()

def _ai_available() -> bool:
    return bool(OPENAI_KEY) and _now() >= _AI_DISABLED_UNTIL

def _disable_ai(seconds: int, reason: str):
    global _AI_DISABLED_UNTIL, _AI_CONSEC_FAILS
    _AI_DISABLED_UNTIL = _now() + max(seconds, 1)
    _AI_CONSEC_FAILS = 0
    print(f"🔌 AI temporarily disabled for {seconds}s → {reason}")

def _note_ai_soft_fail():
    """Count soft failures (JSON/validation/etc) and trip the breaker after a threshold."""
    global _AI_CONSEC_FAILS
    _AI_CONSEC_FAILS += 1
    if _AI_CONSEC_FAILS >= CB_FAIL_LIMIT:
        _disable_ai(CB_COOLDOWN_SECS, f"{_AI_CONSEC_FAILS} consecutive AI generation/parse failures")

def _reset_ai_fail_counter():
    global _AI_CONSEC_FAILS
    _AI_CONSEC_FAILS = 0

# =========================
# Pydantic models (AI JSON)
# =========================
class Hints(BaseModel):
    cuisine: list[str] = Field(default_factory=list, max_items=5)
    habits: list[str]  = Field(default_factory=list, max_items=5)
    vibes: list[str]   = Field(default_factory=list, max_items=5)

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
        if not (-90 <= v <= 90): raise ValueError("lat out of range")
        return v

    @field_validator("lon")
    @classmethod
    def _lon_range(cls, v):
        if not (-180 <= v <= 180): raise ValueError("lon out of range")
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
    eats    = random.sample(place.cuisine, k=min(2, len(place.cuisine)))
    habits  = random.sample(place.habits, k=min(2, len(place.habits)))

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
        "modeUsed": "offline",
        "fallbackReason": None,
    }

# =========================
# Helpers for AI JSON output
# =========================
def build_ai_prompt(avoid_cities: list[str], nudge_region: Optional[str]) -> str:
    avoid_block = ""
    if avoid_cities:
        formatted = ", ".join(avoid_cities[:12])
        avoid_block = f"\n- Do NOT pick any of these recent answers: {formatted}"
    region_block = f"\n- Prefer a different region than: {nudge_region}." if nudge_region else ""
    return (
        "You are a geography game narrator. Generate ONE round as STRICT JSON (no prose, no backticks).\n"
        "- Pick any real-world city (not necessarily famous)."
        f"{region_block}"
        f"{avoid_block}\n"
        "- Provide accurate lat and lon.\n"
        "- Write a 2-sentence FIRST-PERSON traveler monologue that hints at the city WITHOUT naming it.\n"
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
    if not OPENAI_KEY:
        return None
    try:
        from openai import OpenAI
        _openai_client = OpenAI(api_key=OPENAI_KEY)
        return _openai_client
    except Exception as e:
        print("⚠️ Failed to init OpenAI client:", e)
        return None

# =========================
# AI picker (with breaker)
# =========================
def _is_quota_or_auth_error(e: Exception) -> bool:
    msg = str(e).lower()
    return ("insufficient_quota" in msg) or ("invalid_api_key" in msg) or ("401" in msg) or ("403" in msg)

def _is_rate_limit_error(e: Exception) -> bool:
    msg = str(e).lower()
    return ("rate limit" in msg) or ("429" in msg)

def _pick_from_ai() -> Optional[Dict[str, Any]]:
    if not _ai_available():
        return None

    client = get_openai_client()
    if not client:
        return None

    human_avoid = [f"{c.split('|')[0].title()} ({c.split('|')[1].title()})" for c in list(_recent_cities)]
    last_region = _recent_regions[-1] if _recent_regions else None
    prompt = build_ai_prompt(human_avoid, last_region.title() if last_region else None)

    for attempt in range(AI_MAX_ATTEMPTS):
        try:
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                temperature=1.1,
                max_tokens=240,
                presence_penalty=0.2,
            )
            raw = (resp.choices[0].message.content or "").strip()
            raw = _scrub_backticks(raw)

            data = json.loads(raw)
            obj = AIPlace(**data)  # validate

            key = _city_key(obj.city, obj.country)
            if key in _recent_cities:
                print(f"↩️ AI returned recent city again ({obj.city}, {obj.country}); retry {attempt+1}/{AI_MAX_ATTEMPTS}")
                prompt += f"\n- IMPORTANT: Do not choose {obj.city}, {obj.country}."
                _note_ai_soft_fail()
                continue

            _recent_cities.append(key)
            _recent_regions.append(_region_key(obj.region))
            _reset_ai_fail_counter()

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
                "modeUsed": "ai",
                "fallbackReason": None,
            }

        except (json.JSONDecodeError, ValidationError) as ve:
            print("⚠️ AI JSON issue:", ve)
            _note_ai_soft_fail()
        except Exception as e:
            print("⚠️ AI generation failed:", e)
            # classify and disable for a while
            if _is_quota_or_auth_error(e):
                _disable_ai(CB_QUOTA_SECS, "quota/auth error from OpenAI")
                break
            elif _is_rate_limit_error(e):
                _disable_ai(CB_RATELIMIT_SECS, "rate limit")
                break
            else:
                # minor backoff per attempt to avoid hammering
                time.sleep(min(2 + attempt, 6))

    # run out of attempts → soft disable if not already disabled
    if _ai_available():
        _disable_ai(CB_COOLDOWN_SECS, f"exhausted attempts ({AI_MAX_ATTEMPTS})")
    return None

# =========================
# Public API
# =========================
def pick_place(force_mode: Optional[str] = None) -> Dict[str, Any]: 
    """
    force_mode:
      - "offline" => always use local list
      - "ai"      => try AI (falls back to local on failure, and may disable AI for a cooldown)
      - None      => env default (AI_CITY_MODE + OPENAI_KEY with breaker)
    """
    mode = (force_mode or "").strip().lower()
    if mode == "offline":
        return _pick_from_local()

    if mode == "ai":
        bundle = _pick_from_ai()
        if bundle:
            return bundle
        print("⚠️ Forced AI mode unavailable → falling back to local list")
        offline = _pick_from_local()
        offline["fallbackReason"] = "ai_unavailable"
        return offline

    # env-driven default path
    if AI_CITY_MODE and _ai_available():
        bundle = _pick_from_ai()
        if bundle:
            return bundle
        print("⚠️ AI mode failed/unavailable → falling back to local list")
    return _pick_from_local()

def evaluate_guess(secret: Tuple[float, float], guess: Tuple[float, float]):
    dist_km = haversine_km(secret[0], secret[1], guess[0], guess[1])
    score = score_from_km(dist_km)
    return dist_km, score
