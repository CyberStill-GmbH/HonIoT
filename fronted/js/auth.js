// js/auth.js
import { API_BASE } from "./config.js";

// --- helpers de token (localStorage) ---
export function getToken() {
  return localStorage.getItem("siem_jwt");
}

export function setToken(token) {
  localStorage.setItem("siem_jwt", token);
}

export function clearToken() {
  localStorage.removeItem("siem_jwt");
}

// Forzar que la página esté logueada (lo usarás en index/events/tokens)
export function requireAuth() {
  const token = getToken();
  if (!token) {
    window.location.href = "login.html";
  }
}

// --- llamada al backend /auth/login ---
export async function loginRequest(username, password) {
  const res = await fetch(`${API_BASE}/auth/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    username: document.getElementById("user").value,
    password: document.getElementById("pass").value
  })
});


  if (!res.ok) {
    const errData = await res.json().catch(() => ({}));
    const msg = errData.error || "Credenciales inválidas";
    throw new Error(msg);
  }

  return res.json(); // { jwt: "..." }
}

// --- wiring del formulario de login (solo en login.html) ---
document.addEventListener("DOMContentLoaded", () => {
  console.log("auth.js cargado, DOM listo");

  const form = document.getElementById("login-form");
  if (!form) {
    console.log("No hay #login-form en esta página, salgo.");
    return;
  }

  const userInput = document.getElementById("user");
  const passInput = document.getElementById("pass");
  const errorBox = document.getElementById("login-error");

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    if (errorBox) errorBox.textContent = "";

    try {
      const data = await loginRequest(userInput.value, passInput.value);
      console.log("Respuesta login:", data);

      if (!data.jwt) {
        throw new Error("Respuesta del servidor sin JWT");
      }

      setToken(data.jwt);

      // redirigimos al dashboard
      window.location.href = "index.html";
    } catch (err) {
      console.error("Error en login:", err);
      if (errorBox) {
        errorBox.textContent = err.message || "Error al iniciar sesión";
      } else {
        alert(err.message || "Error al iniciar sesión");
      }
    }
  });
});
