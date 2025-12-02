//--------------------------------------------------------
// TOKENS.JS
//--------------------------------------------------------

requireAuth();

const jwtHeaders = {
    "Content-Type": "application/json",
    "Authorization": "Bearer " + getToken()
};

//---------------------------------------------
// Cargar todos los tokens
//---------------------------------------------
async function loadTokens() {
    const res = await fetch(`${API_BASE}/siem/api/tokens`, {
        headers: jwtHeaders
    });

    const data = await res.json();

    const table = document.getElementById("tokensTable");
    table.innerHTML = "";

    data.tokens.forEach(t => {
        table.innerHTML += `
            <tr>
                <td>${t.id}</td>
                <td><code>${t.token}</code></td>
                <td>${t.owner}</td>
                <td>${t.active ? "Activo" : "Inactivo"}</td>
                <td>
                    <button class="btn btn-warning btn-sm" onclick="toggleToken(${t.id}, ${t.active})">
                        ${t.active ? "Desactivar" : "Activar"}
                    </button>
                    <button class="btn btn-danger btn-sm" onclick="deleteToken(${t.id})">Eliminar</button>
                </td>
            </tr>
        `;
    });
}

//---------------------------------------------
// Crear nuevo token
//---------------------------------------------
async function createToken() {
    const owner = prompt("Nombre del dueño del token:");
    if (!owner) return;

    const res = await fetch(`${API_BASE}/siem/api/tokens`, {
        method: "POST",
        headers: jwtHeaders,
        body: JSON.stringify({ owner })
    });

    const data = await res.json();
    alert("Nuevo token creado:\n" + data.token);

    loadTokens();
}

//---------------------------------------------
// Activar/desactivar token
//---------------------------------------------
async function toggleToken(id, active) {
    const res = await fetch(`${API_BASE}/siem/api/tokens/${id}`, {
        method: "PATCH",
        headers: jwtHeaders,
        body: JSON.stringify({ active: !active })
    });

    loadTokens();
}

//---------------------------------------------
// Eliminar token
//---------------------------------------------
async function deleteToken(id) {
    if (!confirm("¿Eliminar token permanentemente?")) return;

    await fetch(`${API_BASE}/siem/api/tokens/${id}`, {
        method: "DELETE",
        headers: jwtHeaders
    });

    loadTokens();
}

loadTokens();
