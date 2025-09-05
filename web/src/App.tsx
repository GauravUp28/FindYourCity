// at top with other imports
import React, { useEffect, useState } from 'react'
import { newRound, submitGuess } from './api'
import { NewRound, GuessResult } from './types'
import MapGuess from './components/MapGuess'

export default function App() {
  const [round, setRound] = useState<NewRound | null>(null)
  const [guess, setGuess] = useState<{ lat: number, lon: number } | null>(null)
  const [result, setResult] = useState<GuessResult | null>(null)
  const [loading, setLoading] = useState(false)           // submit-guess loading
  const [roundLoading, setRoundLoading] = useState(false) // NEW: new-round loading
  const [error, setError] = useState<string | null>(null)

  const startRound = async () => {
    setError(null); setResult(null); setGuess(null)
    setRoundLoading(true)              // <-- start overlay
    try {
      const r = await newRound()
      setRound(r)
    } catch (e: any) {
      setError(e?.message ?? 'Failed to start a round.')
    } finally {
      setRoundLoading(false)           // <-- stop overlay
    }
  }

  const onSubmitGuess = async () => {
    if (!round || !guess) return
    setLoading(true); setError(null)
    try {
      const res = await submitGuess(round.roundId, guess.lat, guess.lon)
      setResult(res)
    } catch (e: any) {
      setError(e?.message ?? 'Failed to submit guess.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { startRound() }, [])

  const anyLoading = roundLoading || loading

  return (
    <div className="app">
      {/* Loading overlay */}
      {roundLoading && (
        <div className="loading-overlay" role="status" aria-live="polite">
          <div className="loader-spinner" />
          <div className="loader-text">Spinning up a new persona…</div>
          <div className="loader-sub">crafting clues & habits</div>
        </div>
      )}

      <header className="container">
        <h1>GeoPersona</h1>
        <p className="tagline">AI-flavored geography guessing: read the clues, drop a pin, score big.</p>
      </header>

      <main className={`container ${anyLoading ? 'is-busy' : ''}`}>
        {!round && !roundLoading && <p>Loading…</p>}

        {round && (
          <div className="panel">
            <div className="clue">
              <h2>Meet <span className="accent">{round.character}</span></h2>
              <p className={`mono ${roundLoading ? 'skeleton' : ''}`}>{round.monologue}</p>

              <div className="chips">
                <span>Hints:</span>
                {round.hints.cuisine.map((c, i) => (<span className="chip" key={i}>{c}</span>))}
                {round.hints.vibes.map((v, i) => (<span className="chip" key={`v${i}`}>{v}</span>))}
                {round.hints.habits.map((h, i) => (<span className="chip" key={`h${i}`}>{h}</span>))}
              </div>
            </div>

            <MapGuess
              defaultCenter={round.mapDefault.center}
              defaultZoom={round.mapDefault.zoom}
              guess={guess}
              setGuess={setGuess}
              locked={!!result}                                  // <— NEW: true once a result exists
              answer={result ? { lat: result.answer.lat, lon: result.answer.lon } : null}
            />

            <div className="actions">
              {/* New Round always enabled (unless roundLoading) */}
              <button
                onClick={startRound}
                className="secondary"
                disabled={roundLoading}
              >
                New Round
              </button>
              <button
                onClick={onSubmitGuess}
                disabled={!guess || loading || !!result || roundLoading}
              >
                {result ? "Result Shown" : "Submit Guess"}
              </button>
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
        <span>© GeoPersona • Built with FastAPI, React & Leaflet</span>
      </footer>
    </div>
  )
}
