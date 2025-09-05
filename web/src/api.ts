import axios from 'axios'
import { NewRound, GuessResult } from './types'

const API = import.meta.env.VITE_API_BASE;
if (!API) {
  throw new Error("VITE_API_BASE is not set. Please configure it in your environment variables.");
}

export async function newRound(): Promise<NewRound> {
  const { data } = await axios.post(`${API}/api/round`, {})
  return data
}

export async function submitGuess(roundId: string, lat: number, lon: number): Promise<GuessResult> {
  const { data } = await axios.post(`${API}/api/round/${roundId}/guess`, { lat, lon })
  return data
}
