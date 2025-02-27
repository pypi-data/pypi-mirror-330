class GPSDisplayMap extends WhiteboxExtensionAPI.MapExtension {
  constructor() {
    super('gps_display')
    this.map = null
    this.markers = {
      whitebox: null,
    }

    Whitebox.sockets.addEventListener('flight', 'message', (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "location_update") {
        this.setWhiteboxLocation({
          lat: data.latitude,
          lon: data.longitude,
        })
      }
    })
  }

  render({ mapContainer }) {
    this.map = L.map(mapContainer).setView([0, 0], 2);

    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: "© OpenStreetMap contributors",
    }).addTo(this.map);

    // Render the marker in the initial position (nowhere)
    this.setWhiteboxLocation({
      lat: 0,
      lon: 0,
    })
  }

  _getOrCreateWhiteboxMarker() {
    if (!this.markers.whitebox) {
      this.markers.whitebox = L.marker([0, 0]).addTo(this.map);
    }
    return this.markers.whitebox
  }

  _calculateBearing(prevLocation, currLocation) {
    const lat1 = prevLocation.lat * Math.PI / 180;
    const lat2 = currLocation.lat * Math.PI / 180;
    const lng1 = prevLocation.lng * Math.PI / 180;
    const lng2 = currLocation.lng * Math.PI / 180;

    const dLng = lng2 - lng1;
    const y = Math.sin(dLng) * Math.cos(lat2);
    const x = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLng);

    // Calculate the angle in radians
    let bearing = Math.atan2(y, x);

    // Convert to degrees and normalize to [0, 360]
    bearing = (bearing * 180 / Math.PI + 360) % 360;

    return bearing;
  }

  _setMarkerLocation(marker, { lat, lon }) {
    marker.setLatLng([lat, lon])
    this.map.setView([lat, lon], 10)

    if (marker.options.isRotating) {
      // If the marker is rotating, we need to set the rotation angle
      // to the current bearing between the current and new location
      const oldLatLng = marker.getLatLng()
      const newLatLng = L.latLng(lat, lon)

      const bearing = this._calculateBearing(oldLatLng, newLatLng)
      const adjustedBearing = bearing + marker.options.initialRotation

      marker.setRotationAngle(adjustedBearing)
    }
  }

  _setMarkerIcon(marker, iconURL, { isRotating = false, initialRotation = 0 }) {
    const icon = L.icon({
      iconUrl: iconURL,
      iconSize: [32, 32],
      iconAnchor: [16, 16],
    })

    marker.setIcon(icon)

    // When a new icon is set, we need to reset the rotation angle and make
    // it centered
    marker.setRotationAngle(0)
    marker.setRotationOrigin('center center')

    // Default `rotationAngle` is 0, which we can't reliably use to determine if
    // the marker should be rotating or not, so we'll set our own value
    marker.options.isRotating = isRotating
    marker.options.initialRotation = initialRotation
  }

  setWhiteboxMarkerIcon({ iconURL, isRotating = false, initialRotation = 0 }) {
    const marker = this._getOrCreateWhiteboxMarker()
    this._setMarkerIcon(marker, iconURL, { isRotating, initialRotation })
  }

  setWhiteboxLocation({ lat, lon }) {
    const marker = this._getOrCreateWhiteboxMarker()
    this._setMarkerLocation(marker, { lat, lon })
  }
}

const init = () => {
  const mapContainer = document.getElementById('slot-map')
  if (!mapContainer) {
    return
  }

  const gpsDisplayMap = new GPSDisplayMap()
  Whitebox.extensions.register(gpsDisplayMap)

  gpsDisplayMap.render({ mapContainer })
}

const module = {
  name: 'gps_display',

  providesCapabilities: ['map'],
  requiresSockets: ['flight'],

  init: init,
}

Whitebox.plugins.registerPlugin(module)

export default module
