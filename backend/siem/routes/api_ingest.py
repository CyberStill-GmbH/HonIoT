from flask import Blueprint, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

from ..models import SessionLocal, ApiToken, Event


# Blueprint para ingest de eventos desde honeypot / gateway
api_ingest = Blueprint("api_ingest", __name__, url_prefix="/siem/api")


def _extract_api_key(req):
    """
    Extrae api_key desde:
    - Header: X-API-KEY
    - Header: Authorization: Bearer <token>
    - JSON body: {"api_key": "..."}
    - Query string: ?api_key=...
    """
    hdr = req.headers.get("X-API-KEY")
    if hdr:
        return hdr.strip()

    auth = req.headers.get("Authorization")
    if auth and auth.lower().startswith("bearer "):
        return auth.split(" ", 1)[1].strip()

    if req.is_json:
        data = req.get_json(silent=True) or {}
        if "api_key" in data:
            return str(data["api_key"]).strip()

    api_key_qs = req.args.get("api_key")
    if api_key_qs:
        return api_key_qs.strip()

    return None


@api_ingest.route("/ingest", methods=["POST"])
def ingest_event():
    """
    Endpoint para recibir eventos desde otros componentes (UDP server, ESP32 gateway, etc.)

    Espera JSON con:
    {
        "api_key": "...",        # opcional si viene en header
        "source_ip": "192.168.18.41",
        "raw_cmd": "rm -rf /",
        "label": "sospechoso",
        "score": 0.98,
        "reason": "pattern match ..."
    }
    """
    db = SessionLocal()
    try:
        api_key = _extract_api_key(request)
        if not api_key:
            return jsonify({"error": "missing api key"}), 400

        # Validar token
        token_obj = (
            db.query(ApiToken)
            .filter(ApiToken.token == api_key, ApiToken.active == True)
            .first()
        )
        if not token_obj:
            return jsonify({"error": "invalid or inactive api key"}), 403

        data = request.get_json(silent=True) or {}

        source_ip = data.get("source_ip") or request.remote_addr
        raw_cmd = data.get("raw_cmd", "")
        label = data.get("label", "desconocido")
        reason = data.get("reason", "")

        try:
            score = float(data.get("score", 0.0))
        except Exception:
            return jsonify({"error": "score debe ser numerico"}), 400

        if not raw_cmd:
            return jsonify({"error": "raw_cmd required"}), 400

        ev = Event(
            source_ip=source_ip,
            raw_cmd=raw_cmd,
            label=label,
            score=score,
            reason=reason,
        )
        db.add(ev)
        db.commit()
        db.refresh(ev)

        return jsonify(
            {
                "status": "ok",
                "message": "evento registrado",
                "event_id": ev.id,
            }
        ), 201

    except SQLAlchemyError as e:
        db.rollback()
        return jsonify({"error": "db error", "detail": str(e)}), 500
    except Exception as e:
        db.rollback()
        return jsonify({"error": "internal error", "detail": str(e)}), 500
    finally:
        db.close()
