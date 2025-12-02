from flask import Blueprint, jsonify
from sqlalchemy import func
from backend.siem.models import SessionLocal, Event

bp_events = Blueprint("bp_events", __name__)

@bp_events.get("/siem/api/events")
def list_events():
    db = SessionLocal()
    try:
        rows = db.query(Event).order_by(Event.id.desc()).limit(200).all()
        return jsonify([
            {
                "id": e.id,
                "source_ip": e.source_ip,
                "raw_cmd": e.raw_cmd,
                "label": e.label,
                "score": e.score,
                "reason": e.reason,
                "created_at": e.created_at.isoformat(),
            }
            for e in rows
        ])
    finally:
        db.close()


@bp_events.get("/siem/api/stats/summary")
def stats_summary():
    db = SessionLocal()
    try:
        total = db.query(Event).count()
        benign = db.query(Event).filter(Event.label == "benigno").count()
        mal = db.query(Event).filter(Event.label == "maligno").count()

        return jsonify({
            "total": total,
            "benignos": benign,
            "malignos": mal
        })
    finally:
        db.close()


@bp_events.get("/siem/api/stats/top-sources")
def top_sources():
    db = SessionLocal()
    try:
        rows = (
            db.query(Event.source_ip, func.count(Event.id).label("n"))
            .group_by(Event.source_ip)
            .order_by(func.count(Event.id).desc())
            .limit(10)
            .all()
        )
        return jsonify([
            {"source_ip": ip, "count": n} for ip, n in rows
        ])
    finally:
        db.close()
