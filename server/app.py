from pathlib import Path
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=True, encoding="utf-8")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any, Optional, Literal
from .store import RoundStore
from .story import pick_place, evaluate_guess

app = FastAPI(title="FindYourCity API", version="0.1.2")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "https://findyourcity.vercel.app",
    ],
    allow_origin_regex=r"https://.*\.vercel\.app",
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
    max_age=600,
)

store = RoundStore(ttl_seconds=20 * 60)  # 20 minutes

# ====== Models ======
class NewRoundRequest(BaseModel):
    # Toggle coming from the UI. If omitted, server uses its env defaults.
    mode: Optional[Literal["offline", "ai"]] = None

class NewRoundResponse(BaseModel):
    roundId: str
    character: str
    monologue: str
    hints: Dict[str, Any]
    mapDefault: Dict[str, Any]
    maxScore: int = 5000
    aiEmbellished: bool = False

class GuessRequest(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lon: float = Field(..., ge=-180, le=180)

class Answer(BaseModel):
    city: str
    country: str
    region: str
    lat: float
    lon: float

class GuessResponse(BaseModel):
    distance_km: float
    score: int
    answer: Answer

# ====== Routes ======
@app.get("/")
def root():
    return {"ok": True, "service": "FindYourCity API"}

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/round", response_model=NewRoundResponse)
def new_round(body: NewRoundRequest | None = None):
    forced_mode = (body.mode if body else None)  # 'offline' | 'ai' | None
    bundle = pick_place(force_mode=forced_mode)

    place = bundle["place"]
    rid = store.new_round(place["lat"], place["lon"], {"place": place})
    return NewRoundResponse(
        roundId=rid,
        character=bundle["character"],
        monologue=bundle["monologue"],
        hints=bundle["hints"],
        mapDefault=bundle["mapDefault"],
        aiEmbellished=bundle.get("ai", False),
    )

@app.post("/api/round/{round_id}/guess", response_model=GuessResponse)
def submit_guess(round_id: str, body: GuessRequest):
    answer = store.get_answer(round_id)
    if not answer:
        raise HTTPException(status_code=404, detail="Round not found or expired.")
    lat, lon, meta = answer
    dist_km, score = evaluate_guess((lat, lon), (body.lat, body.lon))
    place = meta["place"]
    return GuessResponse(
        distance_km=round(dist_km, 2),
        score=score,
        answer=Answer(
            city=place["city"], country=place["country"], region=place["region"],
            lat=place["lat"], lon=place["lon"],
        ),
    )
