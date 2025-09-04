# FindMyCity
**FindMyCity** is an interactive, AI-flavored geography guessing game. Players read a fictional character's clues and habits, then drop a pin on the map to guess where they live. 

Tech: **FastAPI (Python)** backend + **React + Vite + Leaflet** frontend.

---

## Quickstart

### 1) Backend
```bash
cd server
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app:app --reload --port 8000
```
The API will be at `http://localhost:8000`

### 2) Frontend
Open a second terminal:
```bash
cd web
npm i
# Optionally set the backend base in a .env file:
echo "VITE_API_BASE=http://localhost:8000" > .env
npm run dev
```
Open `http://localhost:5173`

---

## How to Play
1. Click **New Round** to receive a character and story clues.
2. Click on the map to place your **guess** (you can drag the marker).
3. Hit **Submit Guess** to see your **distance** and **score** (0–5000).
4. Click **Reveal** to see the correct location and a line from your guess.
5. Play another round!

### Scoring
We use a smooth exponential curve based on great-circle distance (Haversine):
```
score = round(5000 * exp(-distance_km / 2000))
```
Closer = more points; ~0 km ≈ 5000 pts; ~2000 km ≈ 1839 pts; ~5000 km ≈ 410 pts.

---

## Optional: Bring your own LLM
By default, FindMyCity assembles fun, varied clues locally (no external calls).
If you set `OPENAI_API_KEY` in the backend environment, the story generator will ask an LLM to “embellish” the clue text for richer personas.

```bash
export OPENAI_API_KEY=sk-...
uvicorn app:app --reload
```

---

## Project Structure
```
FindMyCity/
├─ server/            # FastAPI backend
│  ├─ app.py          # API routes, CORS, scoring
│  ├─ story.py        # persona + clue generation (local + optional LLM)
│  ├─ game_data.py    # curated world locations + facts
│  ├─ store.py        # in-memory round store with TTL
│  └─ requirements.txt
└─ web/               # React + Vite + Leaflet frontend
   ├─ index.html
   ├─ vite.config.ts
   ├─ tsconfig.json
   ├─ package.json
   └─ src/
      ├─ main.tsx
      ├─ App.tsx
      ├─ api.ts
      ├─ types.ts
      ├─ leafletFix.ts
      ├─ components/
      │  └─ MapGuess.tsx
      └─ styles.css
```

---

## Notes
- Map tiles: OpenStreetMap. Please respect their usage policy for heavy use.
- The backend stores round answers in memory with a short TTL. For multi-instance or persistent play, swap `store.py` with Redis/Postgres.
- This is a starter; extend the dataset, add difficulty tiers, streaks, and leaderboards!