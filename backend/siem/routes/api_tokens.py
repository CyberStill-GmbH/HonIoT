from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from ..models import SessionLocal, ApiToken

# Blueprint para gestion de tokens API
api_tokens = Blueprint("api_tokens", __name__, url_prefix="/siem/api/tokens")


# =========================
#   LISTAR TOKENS
# =========================

@api_tokens.route("/", methods=["GET"])
def list_tokens():
    """
    Lista todos los tokens API.
    """
    db = SessionLocal()
    try:
        tokens = db.query(ApiToken).order_by(ApiToken.id.asc()).all()
        result = []
        for t in tokens:
            result.append(
                {
                    "id": t.id,
                    "token": t.token,
                    "owner": getattr(t, "owner", None),
                    "active": getattr(t, "active", None),
                    "created_at": t.created_at.isoformat() if t.created_at else None,
                }
            )
        return jsonify(result)
    finally:
        db.close()


# =========================
#   CREAR TOKEN
# =========================

@api_tokens.route("/", methods=["POST"])
def create_token():
    """
    Crea un nuevo token API.

    Body JSON:
    {
        "owner": "nombre_opcional",
        "active": true
    }
    """
    from secrets import token_hex

    db = SessionLocal()
    try:
        data = request.get_json(silent=True) or {}
        owner = data.get("owner", None)
        active = data.get("active", True)

        raw_token = token_hex(32)

        t = ApiToken(
            token=raw_token,
            owner=owner,
            active=bool(active),
        )
        db.add(t)
        db.commit()
        db.refresh(t)

        return (
            jsonify(
                {
                    "id": t.id,
                    "token": t.token,  # importante: mostrar solo una vez aqui
                    "owner": t.owner,
                    "active": t.active,
                    "created_at": t.created_at.isoformat()
                    if t.created_at
                    else None,
                }
            ),
            201,
        )

    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "db error", "detail": str(e)}), 500
    finally:
        db.close()


# =========================
#   PARCIAL UPDATE (PATCH)
# =========================

@api_tokens.route("/<int:token_id>", methods=["PATCH"])
def patch_token(token_id: int):
    """
    Actualiza parcialmente un token API (por ejemplo, activar/desactivar).

    Body JSON:
    {
        "active": false
    }
    """
    db = SessionLocal()
    try:
        t = db.query(ApiToken).filter(ApiToken.id == token_id).first()
        if not t:
            return jsonify({"error": "token not found"}), 404

        data = request.get_json(silent=True) or {}
        if "active" in data:
            t.active = bool(data["active"])

        if "owner" in data:
            t.owner = data["owner"]

        db.commit()
        db.refresh(t)

        return jsonify(
            {
                "id": t.id,
                "token": t.token,
                "owner": t.owner,
                "active": t.active,
                "created_at": t.created_at.isoformat()
                if t.created_at
                else None,
            }
        )

    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "db error", "detail": str(e)}), 500
    finally:
        db.close()


# =========================
#   DELETE TOKEN
# =========================

@api_tokens.route("/<int:token_id>", methods=["DELETE"])
def delete_token(token_id: int):
    """
    Elimina un token API por id.
    """
    db = SessionLocal()
    try:
        t = db.query(ApiToken).filter(ApiToken.id == token_id).first()
        if not t:
            return jsonify({"error": "token not found"}), 404

        db.delete(t)
        db.commit()
        return jsonify({"status": "deleted", "id": token_id})

    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "db error", "detail": str(e)}), 500
    finally:
        db.close()
