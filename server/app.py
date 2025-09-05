from pathlib import Path
from dotenv import load_dotenv

# Load server/.env BEFORE any other imports read env vars
load_dotenv(dotenv_path=Path(__file__).with_name(".env"), override=True, encoding="utf-8")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Dict, Any
from .store import RoundStore
from .story import pick_place, evaluate_guess

app = FastAPI(title="FindYourCity API", version="0.1.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

store = RoundStore(ttl_seconds=20 * 60)  # 20 min TTL

class NewRoundRequest(BaseModel):
    pass

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

class GuessResponse(BaseModel):
    distance_km: float
    score: int
    answer: Dict[str, Any]

@app.get("/api/health")
def health():
    return {"ok": True}

@app.post("/api/round", response_model=NewRoundResponse)
def new_round(_: NewRoundRequest | None = None):
    bundle = pick_place()
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
    return GuessResponse(
        distance_km=round(dist_km, 2),
        score=score,
        answer=meta["place"],
    )
