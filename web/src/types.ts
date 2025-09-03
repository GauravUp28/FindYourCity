export type NewRound = {
  roundId: string
  character: string
  monologue: string
  hints: {
    cuisine: string[]
    habits: string[]
    vibes: string[]
  }
  mapDefault: {
    center: [number, number]
    zoom: number
  }
  maxScore: number
}

export type GuessResult = {
  distance_km: number
  score: number
  answer: {
    city: string
    country: string
    lat: number
    lon: number
    region: string
  }
}
