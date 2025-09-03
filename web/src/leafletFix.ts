import L from 'leaflet'
// Vite bundling can break Leaflet's default icon paths.
// This patch points them to the imported assets.
import markerRetina from 'leaflet/dist/images/marker-icon-2x.png'
import marker from 'leaflet/dist/images/marker-icon.png'
import shadow from 'leaflet/dist/images/marker-shadow.png'

L.Icon.Default.mergeOptions({
  iconRetinaUrl: markerRetina,
  iconUrl: marker,
  shadowUrl: shadow,
})
