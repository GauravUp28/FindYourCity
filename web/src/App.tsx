import React, { useEffect, useState } from 'react'
import MapGuess, { type MapStyle } from './components/MapGuess'
import { newRound, submitGuess, type GameMode } from './api'
import { NewRound, GuessResult } from './types'

const MAP_STYLE_DEFAULT: MapStyle = 'satellite'

const resolveStoredMapStyle = (): MapStyle => {
  try {
    const stored = localStorage.getItem('mapStyle')
    return stored === 'satellite' || stored === 'dark' || stored === 'streets'
      ? stored
      : MAP_STYLE_DEFAULT
  } catch {
    return MAP_STYLE_DEFAULT
  }
}

export default function App() {
  const [mode, setMode] = useState<GameMode>(() => (localStorage.getItem('mode') as GameMode) || 'offline')
  const [round, setRound] = useState<NewRound | null>(null)
  const [guess, setGuess] = useState<{ lat: number, lon: number } | null>(null)
  const [result, setResult] = useState<GuessResult | null>(null)
  const [loading, setLoading] = useState(false)           // submit-guess loading
  const [roundLoading, setRoundLoading] = useState(false) // new-round loading
  const [error, setError] = useState<string | null>(null)
  const [mapStyle, setMapStyle] = useState<MapStyle>(() => resolveStoredMapStyle())

  // Accept either a GameMode or a MouseEvent, and normalize
  const startRound = async (arg?: GameMode | React.MouseEvent) => {
    const selected =
      arg === 'offline' || arg === 'ai' ? arg : mode; // use explicit mode or current state

    setError(null); setResult(null); setGuess(null)
    setRoundLoading(true)
    try {
      const r = await newRound(selected)   // <-- always a valid 'offline' | 'ai'
      setRound(r)
    } catch (e: any) {
      setError(e?.message ?? 'Failed to start a round.')
    } finally {
      setRoundLoading(false)
    }
  }


  useEffect(() => { startRound() }, []) // first round on load

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

  const onModeChange = (m: GameMode) => {
    setMode(m)
    localStorage.setItem('mode', m)
    startRound(m)        // pass the mode explicitly
  }

  const onMapStyleChange = (style: MapStyle) => {
    setMapStyle(style)
    localStorage.setItem('mapStyle', style)
  }

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

      <header className="container app-header">
        <h1>FindYourCity</h1>
        <p className="tagline">🗺️ Decode the story, drop your pin, test your world sense.</p>
        {/* Mode toggle */}
        {/* Mode toggle */}
        <div className="mode-toggle">
          <span className="mode-label">Mode:</span>
          <label className={`pill ${mode === 'offline' ? 'active' : ''}`}>
            <input
              type="radio"
              name="mode"
              checked={mode === 'offline'}
              onChange={() => !roundLoading && onModeChange('offline')}
              disabled={roundLoading}
            />
            Offline
          </label>

          <label className={`pill ${mode === 'ai' ? 'active' : ''}`}>
            <input
              type="radio"
              name="mode"
              checked={mode === 'ai'}
              onChange={() => !roundLoading && onModeChange('ai')}
              disabled={roundLoading}
            />
            AI
          </label>

        </div>
      </header>

      <main className={`container ${anyLoading ? 'is-busy' : ''}`}>
        {!round && !roundLoading && <p>Loading…</p>}

        {round && (
          <div className="panel">
            <div className="clue">
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
              locked={!!result}
              answer={result ? { lat: result.answer.lat, lon: result.answer.lon } : null}
              mapStyle={mapStyle}
              onStyleChange={onMapStyleChange}
            />

            <div className="actions">
              <button
                onClick={() => startRound()}   // <-- wrap in arrow, no event argument
                className="secondary"
                disabled={roundLoading}
              >
                New Round
              </button>
              <button
                onClick={onSubmitGuess}
                disabled={!guess || loading || !!result || roundLoading}
              >
                {result ? 'Result Shown' : 'Submit Guess'}
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
        <span>© FindYourCity • Built with FastAPI, React & Leaflet</span>
        <a
          className="footer-link"
          href="https://github.com/GauravUp28/FindYourCity"
          target="_blank"
          rel="noreferrer"
        >
          GitHub Repo
        </a>
      </footer>
    </div>
  )
}
