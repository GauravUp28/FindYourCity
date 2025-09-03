import React, { useEffect, useState } from 'react'
import { newRound, submitGuess } from './api'
import { NewRound, GuessResult } from './types'
import MapGuess from './components/MapGuess'

export default function App() {
  const [round, setRound] = useState<NewRound | null>(null)
  const [guess, setGuess] = useState<{lat:number, lon:number} | null>(null)
  const [result, setResult] = useState<GuessResult | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const startRound = async () => {
    setError(null); setResult(null); setGuess(null)
    try {
      const r = await newRound()
      setRound(r)
    } catch (e:any) {
      setError(e?.message ?? 'Failed to start a round.')
    }
  }

  const onSubmitGuess = async () => {
    if (!round || !guess) return
    setLoading(true); setError(null)
    try {
      const res = await submitGuess(round.roundId, guess.lat, guess.lon)
      setResult(res)
    } catch (e:any) {
      setError(e?.message ?? 'Failed to submit guess.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { startRound() }, [])

  return (
    <div className="app">
      <header className="container">
        <h1>FindMyCity</h1>
        <p className="tagline">AI-flavored geography guessing: read the clues, drop a pin, score big.</p>
      </header>

      <main className="container">
        {!round && <p>Loading…</p>}

        {round && (
          <div className="panel">
            <div className="clue">
              <h2>Meet <span className="accent">{round.character}</span></h2>
              <p className="mono">{round.monologue}</p>
              <div className="chips">
                <span>Hints:</span>
                {round.hints.cuisine.map((c,i)=>(<span className="chip" key={i}>{c}</span>))}
                {round.hints.vibes.map((v,i)=>(<span className="chip" key={`v${i}`}>{v}</span>))}
                {round.hints.habits.map((h,i)=>(<span className="chip" key={`h${i}`}>{h}</span>))}
              </div>
            </div>

            <MapGuess
              defaultCenter={round.mapDefault.center}
              defaultZoom={round.mapDefault.zoom}
              guess={guess}
              setGuess={setGuess}
              reveal={!!result}
              answer={result ? {lat: round ? result.answer.lat : 0, lon: round ? result.answer.lon : 0} : null}
            />

            <div className="actions">
              <button onClick={startRound} className="secondary">New Round</button>
              <button onClick={onSubmitGuess} disabled={!guess || loading}>Submit Guess</button>
              <button onClick={()=> setResult(prev=> prev ? {...prev} : null)} disabled={!result}>Reveal</button>
            </div>

            {error && <div className="error">{error}</div>}

            {result && (
              <div className="result">
                <div><strong>Distance:</strong> {result.distance_km} km</div>
                <div><strong>Score:</strong> {result.score} / {round.maxScore}</div>
                <div className="muted">
                  Answer: {result.answer.city}, {result.answer.country} ({result.answer.lat.toFixed(3)}, {result.answer.lon.toFixed(3)})
                </div>
              </div>
            )}
          </div>
        )}
      </main>

      <footer className="container footer">
        <span>© FindMyCity • Built with FastAPI, React & Leaflet</span>
      </footer>
    </div>
  )
}
