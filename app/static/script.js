let map, tileLayer;
let markers = {};
let soundEnabled = true;
const audioCtx = new (window.AudioContext || window.webkitAudioContext)();

document.addEventListener('DOMContentLoaded', () => {
  map = L.map('map').setView([23.5859, 58.4059], 12);

  tileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors',
    maxZoom: 18,
  }).addTo(map);

  L.control.scale({ position: 'bottomright' }).addTo(map);
  fetchData();
});

function playAlertSound() {
  if (!soundEnabled) return;
  const oscillator = audioCtx.createOscillator();
  oscillator.type = 'sine';
  oscillator.frequency.setValueAtTime(800, audioCtx.currentTime);
  oscillator.connect(audioCtx.destination);
  oscillator.start();
  oscillator.stop(audioCtx.currentTime + 0.2);
}

function toggleSound() {
  soundEnabled = !soundEnabled;
  document.getElementById('sound-toggle').textContent = soundEnabled ? 'Mute Alerts' : 'Unmute Alerts';
}

async function fetchData() {
  document.getElementById('map-loading').classList.remove('hidden');
  document.getElementById('map-error').classList.add('hidden');

  try {
    const res = await fetch('/dashboard-data');
    const data = await res.json();

    const bounds = [];
    data.vehicles.forEach(truck => {
      const id = truck.truck_id;
      const lat = truck.latitude;
      const lon = truck.longitude;
      const fuel = truck.fuel_level;

      bounds.push([lat, lon]);
      const popupContent = `
        <div class="p-2">
          <h3 class="font-bold">Truck ${id}</h3>
          <p>Fuel: ${fuel} liters</p>
          <p>Lat: ${lat.toFixed(4)}</p>
          <p>Lon: ${lon.toFixed(4)}</p>
        </div>
      `;
      const truckIcon = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/1432/1432636.png',
        iconSize: [32, 32],
        iconAnchor: [16, 16],
        popupAnchor: [0, -16]
      });

      if (markers[id]) {
        markers[id].setLatLng([lat, lon]).setPopupContent(popupContent);
      } else {
        markers[id] = L.marker([lat, lon], { icon: truckIcon }).addTo(map).bindPopup(popupContent);
      }
    });

    if (bounds.length > 0) {
      map.fitBounds(bounds, { padding: [50, 50], maxZoom: 14 });
    }

    const alertsList = document.getElementById('alerts-list');
    alertsList.innerHTML = '';
    data.alerts.forEach(alert => {
      const li = document.createElement('li');
      li.className = 'alert-enter p-4 rounded-md bg-red-100';
      li.innerHTML = `<span class="block text-sm font-bold">[${alert.timestamp}]</span><span class="block text-sm">Truck ${alert.truck_id}: ${alert.message}</span>`;
      alertsList.appendChild(li);
      playAlertSound();
      setTimeout(() => li.className = 'alert-enter-active p-4 rounded-md bg-red-100', 10);
    });

    const fleetSummary = document.getElementById('fleet-summary');
    fleetSummary.innerHTML = data.vehicles.map(truck => `
      <div class="flex items-center gap-4">
        <div class="gauge">
          <div class="gauge-needle" style="transform: rotate(${(truck.fuel_level / 100) * 180 - 90}deg)"></div>
          <div class="gauge-label">Truck ${truck.truck_id}</div>
        </div>
        <p class="text-sm">Truck ${truck.truck_id}: ${truck.fuel_level} liters</p>
      </div>
    `).join('');

    map.invalidateSize();
    document.getElementById('map-loading').classList.add('hidden');

  } catch (error) {
    console.error('Error fetching data:', error);
    document.getElementById('map-error').classList.remove('hidden');
    document.getElementById('map-loading').classList.add('hidden');
  }
}

setInterval(fetchData, 5000);
