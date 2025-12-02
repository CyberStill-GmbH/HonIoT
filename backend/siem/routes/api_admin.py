from flask import Blueprint, request, jsonify, Response
from functools import wraps
import jwt
import csv

from ..config_siem import SECRET_KEY
from ..models import SessionLocal, Event


api_admin = Blueprint("api_admin", __name__, url_prefix="/siem/api/admin")


# ---------------------------
#   JWT AUTH MIDDLEWARE
# ---------------------------
def decode_jwt(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except:
        return None


def require_admin_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")
        if not auth.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid JWT"}), 401

        token = auth.split(" ", 1)[1]
        payload = decode_jwt(token)
        if not payload:
            return jsonify({"error": "Invalid or expired JWT"}), 401

        request.admin_id = payload["admin_id"]
        return f(*args, **kwargs)
    return wrapper


# ---------------------------
#     DELETE EVENT
# ---------------------------
@api_admin.route("/delete-event/<int:event_id>", methods=["DELETE"])
@require_admin_auth
def delete_event(event_id):
    db = SessionLocal()
    try:
        ev = db.query(Event).filter_by(id=event_id).first()
        if not ev:
            return jsonify({"error": "event not found"}), 404

        db.delete(ev)
        db.commit()
        return jsonify({"status": "deleted", "id": event_id})

    finally:
        db.close()


# ---------------------------
#      EXPORT CSV
# ---------------------------
@api_admin.route("/export", methods=["GET"])
@require_admin_auth
def export_events():
    db = SessionLocal()
    try:
        events = db.query(Event).order_by(Event.timestamp.desc()).all()

        def generate():
            yield "id,timestamp,source_ip,label,score,reason\n"
            for e in events:
                yield f"{e.id},{e.timestamp},{e.source_ip},{e.label},{e.score},{e.reason}\n"

        return Response(generate(), mimetype="text/csv")

    finally:
        db.close()
