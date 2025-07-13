const apiUrl = "http://localhost:8000/dashboard-data";

async function fetchData() {
  const res = await fetch(apiUrl);
  const data = await res.json();
  console.log(data);
  updateMap(data.vehicles);
  updateTable(data.vehicles, data.alerts);
}

// Setup map
const map = L.map('map').setView([23.5859, 58.4059], 13);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

// Draw geofence circle
const geofenceCenter = [23.5859, 58.4059];
const geofenceRadius = 5000; // 5 km in meters
L.circle(geofenceCenter, { radius: geofenceRadius, color: 'blue' }).addTo(map);

function updateMap(vehicles) {
  vehicles.forEach(truck => {
    const marker = L.marker([truck.latitude, truck.longitude]).addTo(map);
    marker.bindPopup(`<b>${truck.truck_id}</b><br>Fuel: ${truck.fuel_level} L`);
  });
}

function updateTable(vehicles, alerts) {
  const tbody = document.querySelector("#alerts-table tbody");
  tbody.innerHTML = "";

  vehicles.forEach(truck => {
    const truckAlerts = alerts
      .filter(a => a.truck_id === truck.truck_id)
      .map(a => a.message)
      .join("; ");

    const row = `
      <tr>
        <td>${truck.truck_id}</td>
        <td>${truck.fuel_level}</td>
        <td>${truck.latitude.toFixed(5)}</td>
        <td>${truck.longitude.toFixed(5)}</td>
        <td>${truckAlerts}</td>
      </tr>
    `;
    tbody.innerHTML += row;
  });
}

fetchData();
setInterval(fetchData, 5000); // Refresh every 5 sec
