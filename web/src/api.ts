import axios from 'axios'
import { NewRound, GuessResult } from './types'

const API = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export async function newRound(): Promise<NewRound> {
  const { data } = await axios.post(`${API}/api/round`, {})
  return data
}

export async function submitGuess(roundId: string, lat: number, lon: number): Promise<GuessResult> {
  const { data } = await axios.post(`${API}/api/round/${roundId}/guess`, { lat, lon })
  return data
}
