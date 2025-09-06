// web/src/api.ts
import axios from 'axios'
import { NewRound, GuessResult } from './types'

export type GameMode = 'offline' | 'ai'

// Robust resolve + safe dev fallback so the app never blanks
const API =
  (import.meta as any)?.env?.VITE_API_BASE ||
  import.meta.env?.VITE_API_BASE ||
  'http://localhost:8000'

if (import.meta.env.DEV) {
  console.log('[FindYourCity] API base =', API)
}

export async function newRound(mode: GameMode = 'offline'): Promise<NewRound> {
  const { data } = await axios.post(`${API}/api/round`, { mode })
  return data
}

export async function submitGuess(
  roundId: string,
  lat: number,
  lon: number
): Promise<GuessResult> {
  const { data } = await axios.post(`${API}/api/round/${roundId}/guess`, { lat, lon })
  return data
}
