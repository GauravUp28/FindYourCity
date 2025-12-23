import React, { useMemo } from 'react'
import { MapContainer, TileLayer, Marker, Polyline, useMapEvents } from 'react-leaflet'
import L, { LatLngExpression } from 'leaflet'
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

export type MapStyle = 'satellite' | 'dark' | 'streets'

const MAP_STYLES: Record<MapStyle, { label: string, url: string, attribution: string }> = {
  satellite: {
    label: 'Satellite',
    url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attribution: 'Tiles &copy; Esri &mdash; Source: Esri, GeoEye, Earthstar Geographics, CNES/Airbus DS',
  },
  dark: {
    label: 'Dark',
    url: 'https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png',
    attribution: '&copy; OpenStreetMap &copy; CARTO',
  },
  streets: {
    label: 'Streets',
    url: 'https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png',
    attribution: '&copy; OpenStreetMap &copy; CARTO',
  }
}

type Props = {
  defaultCenter: [number, number]
  defaultZoom: number
  guess: { lat: number, lon: number } | null
  setGuess: (g: { lat: number, lon: number } | null) => void
  locked: boolean
  answer: { lat: number, lon: number } | null
  mapStyle: MapStyle
  onStyleChange: (style: MapStyle) => void
}

function ClickHandler({ onClick, locked }: { onClick: (lat: number, lon: number) => void; locked: boolean }) {
  useMapEvents({
    click(e) {
      if (locked) return
      onClick(e.latlng.lat, e.latlng.lng)
    }
  })
  return null
}

export default function MapGuess({ defaultCenter, defaultZoom, guess, setGuess, locked, answer, mapStyle, onStyleChange }: Props) {
  const center = useMemo<LatLngExpression>(() => defaultCenter, [defaultCenter])
  const activeStyle = MAP_STYLES[mapStyle]

  const linePositions = useMemo(() => {
    if (!answer || !guess) return null
    return [
      [guess.lat, guess.lon] as [number, number],
      [answer.lat, answer.lon] as [number, number]
    ]
  }, [answer, guess])

  return (
    <div className="map-wrap">
      <div className="map-style-toggle" role="radiogroup" aria-label="Map style">
        {Object.entries(MAP_STYLES).map(([styleKey, data]) => {
          const style = styleKey as MapStyle
          const isActive = style === mapStyle
          return (
            <button
              key={style}
              type="button"
              className={`map-style-pill ${isActive ? 'active' : ''}`}
              aria-pressed={isActive}
              onClick={() => onStyleChange(style)}
            >
              {data.label}
            </button>
          )
        })}
      </div>

      <MapContainer center={center} zoom={defaultZoom} scrollWheelZoom className={`map ${locked ? 'is-locked' : ''}`}>
        <TileLayer
          key={mapStyle}
          attribution={activeStyle.attribution}
          url={activeStyle.url}
        />
        <ClickHandler onClick={(lat, lon) => setGuess({ lat, lon })} locked={locked} />
        {guess && (
          <Marker
            position={[guess.lat, guess.lon]}
            icon={defaultIcon}
            draggable={!locked}                         // <— freeze dragging when locked
            eventHandlers={
              !locked
                ? {
                  dragend: (e) => {
                    const m = e.target as L.Marker
                    const p = m.getLatLng()
                    setGuess({ lat: p.lat, lon: p.lng })
                  },
                }
                : undefined
            }
          />
        )}
        {locked && answer && (
          <Marker position={[answer.lat, answer.lon]} icon={defaultIcon} />
        )}

        {locked && answer && guess && linePositions && (
          <Polyline positions={linePositions} />
        )}
      </MapContainer>
    </div>
  )
}
