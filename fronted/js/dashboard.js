import { API_BASE } from "./config.js";

async function loadSummary() {
    const res = await fetch(`${API_BASE}/stats/summary`);
    const data = await res.json();
    console.log(data);
}
