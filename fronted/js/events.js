// js/events.js
import { API_BASE } from "./config.js";

const tbody = document.getElementById("events-body");
const countLabel = document.getElementById("events-count");
const form = document.getElementById("filters-form");
const ipInput = document.getElementById("filter-ip");
const labelInput = document.getElementById("filter-label");
const limitInput = document.getElementById("filter-limit");

async function loadEvents() {
  try {
    const limit = parseInt(limitInput.value || "50", 10);

    // Construimos la URL con parámetros básicos (limit / offset)
    const url = new URL(`${API_BASE}/events`);
    url.searchParams.set("limit", isNaN(limit) ? 50 : limit);
    url.searchParams.set("offset", 0);

    const res = await fetch(url);
    if (!res.ok) {
      console.error("Error al obtener eventos:", res.status, res.statusText);
      return;
    }

    const data = await res.json();
    const events = data.events || [];

    // Aplico filtros simples en el cliente
    const ipFilter = ipInput.value.trim().toLowerCase();
    const labelFilter = labelInput.value.trim().toLowerCase();

    const filtered = events.filter((ev) => {
      const ipOk = ipFilter
        ? (ev.source_ip || "").toLowerCase().includes(ipFilter)
        : true;
      const labelOk = labelFilter
        ? (ev.label || "").toLowerCase().includes(labelFilter)
        : true;
      return ipOk && labelOk;
    });

    renderEvents(filtered);
    countLabel.textContent = `Mostrando ${filtered.length} de ${data.count ?? events.length} eventos.`;
  } catch (err) {
    console.error("Error cargando eventos:", err);
  }
}

function renderEvents(events) {
  tbody.innerHTML = "";

  if (!events.length) {
    const tr = document.createElement("tr");
    const td = document.createElement("td");
    td.colSpan = 7;
    td.className = "text-center text-muted";
    td.textContent = "No hay eventos para los filtros actuales.";
    tr.appendChild(td);
    tbody.appendChild(tr);
    return;
  }

  for (const ev of events) {
    const tr = document.createElement("tr");

    const tdId = document.createElement("td");
    tdId.textContent = ev.id;
    tr.appendChild(tdId);

    const tdTs = document.createElement("td");
    tdTs.textContent = ev.timestamp || "";
    tr.appendChild(tdTs);

    const tdIp = document.createElement("td");
    tdIp.textContent = ev.source_ip || "";
    tr.appendChild(tdIp);

    const tdLabel = document.createElement("td");
    tdLabel.textContent = ev.label || "";
    tr.appendChild(tdLabel);

    const tdScore = document.createElement("td");
    tdScore.textContent = ev.score != null ? ev.score.toFixed(2) : "";
    tr.appendChild(tdScore);

    const tdCmd = document.createElement("td");
    tdCmd.textContent = ev.raw_cmd || "";
    tr.appendChild(tdCmd);

    const tdReason = document.createElement("td");
    tdReason.textContent = ev.reason || "";
    tr.appendChild(tdReason);

    tbody.appendChild(tr);
  }
}

// Manejar envío del formulario de filtros
form.addEventListener("submit", (e) => {
  e.preventDefault();
  loadEvents();
});

// Cargar al inicio
document.addEventListener("DOMContentLoaded", () => {
  loadEvents();
});
