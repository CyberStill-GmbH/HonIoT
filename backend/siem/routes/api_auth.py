from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
import jwt
from datetime import datetime, timedelta

from ..config_siem import SECRET_KEY
from ..models import SessionLocal, AdminUser

# Blueprint para endpoints de autenticacion admin
api_auth = Blueprint("api_auth", __name__, url_prefix="/siem/api/auth")


# =========================
#   Helpers JWT
# =========================

def create_jwt(admin_id: int) -> str:
    """
    Genera un JWT valido por 24 horas.
    """
    payload = {
        "admin_id": admin_id,
        "exp": datetime.utcnow() + timedelta(hours=24),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


def decode_jwt(token: str):
    """
    Decodifica y valida un JWT. Devuelve el payload o None.
    """
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except Exception:
        return None


def require_admin_auth(f):
    """
    Decorador para proteger endpoints admin con JWT.

    Espera header:
        Authorization: Bearer <token>
    """
    from functools import wraps

    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid JWT"}), 401

        token = auth.split(" ", 1)[1].strip()
        payload = decode_jwt(token)
        if not payload:
            return jsonify({"error": "Invalid or expired JWT"}), 401

        # Adjuntamos admin_id al request para uso interno
        request.admin_id = payload.get("admin_id")
        return f(*args, **kwargs)

    return wrapper


# =========================
#   LOGIN ADMIN
# =========================

@api_auth.route("/login", methods=["POST"])
def siem_auth_login():
    """
    Login de administrador.

    Body JSON:
    {
        "username": "...",
        "password": "..."
    }

    Respuesta:
    {
        "jwt": "<token>"
    }
    """
    db = SessionLocal()
    try:
        data = request.get_json() or {}
        username = data.get("username", "").strip()
        password = data.get("password", "")

        if not username or not password:
            return jsonify({"error": "username y password requeridos"}), 400

        user = db.query(AdminUser).filter_by(username=username).first()
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401

        if not check_password_hash(user.password_hash, password):
            return jsonify({"error": "Invalid credentials"}), 401

        jwt_token = create_jwt(user.id)
        return jsonify({"jwt": jwt_token})

    finally:
        db.close()
