// js/main.js

// URL base del backend Flask
const API_BASE = "http://127.0.0.1:8080/siem/api";

async function loadSummary() {
  try {
    const res = await fetch(`${API_BASE}/stats/summary`);
    if (!res.ok) {
      console.error("Respuesta no OK del backend:", res.status, res.statusText);
      return;
    }

    const data = await res.json();

    // OJO: nombres de las keys según tu backend (app.py)
    // app.py devuelve: total_events, unique_ips, events_today, by_label
    const totalEvents = data.total_events ?? 0;
    const byLabel = data.by_label || {};

    const sospechosos =
      byLabel["sospechoso"] ||
      byLabel["suspicious"] ||
      byLabel["SUSPICIOUS"] ||
      0;

    const exploits =
      byLabel["exploit"] ||
      byLabel["EXPLOIT"] ||
      0;

    document.getElementById("metric-total").textContent = totalEvents;
    document.getElementById("metric-suspicious").textContent = sospechosos;
    document.getElementById("metric-exploit").textContent = exploits;
  } catch (err) {
    console.error("Error cargando summary:", err);
  }
}

// Cuando el DOM está listo, cargamos métricas y actualizamos cada 10s
document.addEventListener("DOMContentLoaded", () => {
  loadSummary();
  setInterval(loadSummary, 10000);
});
