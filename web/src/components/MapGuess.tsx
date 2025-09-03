import React, { useMemo } from 'react'
import { MapContainer, TileLayer, Marker, Polyline, useMapEvents } from 'react-leaflet'
import L, { LatLngExpression } from 'leaflet'
const maptilerKey = import.meta.env.VITE_MAPTILER_KEY as string | undefined
import { Icon } from 'leaflet'

import markerRetina from 'leaflet/dist/images/marker-icon-2x.png'
import marker from 'leaflet/dist/images/marker-icon.png'
import shadow from 'leaflet/dist/images/marker-shadow.png'

const defaultIcon = new Icon({
  iconRetinaUrl: markerRetina,
  iconUrl: marker,
  shadowUrl: shadow,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
})

const tileUrl = maptilerKey
  ? `https://api.maptiler.com/maps/streets-v2/{z}/{x}/{y}.png?key=${maptilerKey}&language=en`
  : 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

const tileAttribution = maptilerKey
  ? '&copy; <a href="https://www.maptiler.com/copyright/">MapTiler</a> &copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
  : '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'

type Props = {
  defaultCenter: [number, number]
  defaultZoom: number
  guess: { lat:number, lon:number } | null
  setGuess: (g: { lat:number, lon:number } | null) => void
  reveal: boolean
  answer: { lat:number, lon:number } | null
}

function ClickHandler({ onClick }: { onClick: (lat:number, lon:number)=>void }) {
  useMapEvents({
    click(e) {
      onClick(e.latlng.lat, e.latlng.lng)
    }
  })
  return null
}

export default function MapGuess({ defaultCenter, defaultZoom, guess, setGuess, reveal, answer }: Props) {
  const center = useMemo<LatLngExpression>(()=> defaultCenter, [defaultCenter])

  const linePositions = useMemo(() => {
    if (!reveal || !answer || !guess) return null
    return [
      [guess.lat, guess.lon] as [number, number],
      [answer.lat, answer.lon] as [number, number]
    ]
  }, [reveal, answer, guess])

  return (
    <div className="map-wrap">
      <MapContainer center={center} zoom={defaultZoom} scrollWheelZoom className="map">
        <TileLayer
  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/">CARTO</a>'
  url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png"
/>
        <ClickHandler onClick={(lat,lon)=> setGuess({lat,lon})} />
        {guess && (
  <Marker
    position={[guess.lat, guess.lon]}
    icon={defaultIcon}
    draggable
    eventHandlers={{
      dragend: (e) => {
        const m = e.target as L.Marker
        const p = m.getLatLng()
        setGuess({ lat: p.lat, lon: p.lng })
      }
    }}
  />
)}

{reveal && answer && (
  <Marker position={[answer.lat, answer.lon]} icon={defaultIcon} />
)}
        {linePositions && (
          <Polyline positions={linePositions} />
        )}
      </MapContainer>
    </div>
  )
}
