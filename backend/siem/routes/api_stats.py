from flask import Blueprint, request, jsonify
from sqlalchemy import func, extract
from datetime import date

from ..models import SessionLocal, Event


api_stats = Blueprint("api_stats", __name__, url_prefix="/siem/api")


# ---------------------------
#      LIST EVENTS
# ---------------------------
@api_stats.route("/events", methods=["GET"])
def events_list():
    db = SessionLocal()
    try:
        limit = int(request.args.get("limit", 50))
        offset = int(request.args.get("offset", 0))

        rows = (
            db.query(Event)
            .order_by(Event.timestamp.desc())
            .offset(offset)
            .limit(limit)
            .all()
        )

        return jsonify({
            "count": len(rows),
            "events": [e.to_dict() for e in rows],
        })

    finally:
        db.close()


# ---------------------------
#      SUMMARY STATS
# ---------------------------
@api_stats.route("/stats/summary", methods=["GET"])
def stats_summary():
    db = SessionLocal()
    try:
        total = db.query(func.count(Event.id)).scalar()
        unique_ips = db.query(func.count(func.distinct(Event.source_ip))).scalar()

        today = date.today()
        today_count = (
            db.query(func.count(Event.id))
            .filter(func.date(Event.timestamp) == today)
            .scalar()
        )

        by_label = (
            db.query(Event.label, func.count(Event.id))
            .group_by(Event.label)
            .all()
        )

        return jsonify({
            "total_events": total,
            "unique_ips": unique_ips,
            "events_today": today_count,
            "by_label": {lbl: cnt for lbl, cnt in by_label}
        })

    finally:
        db.close()


# ---------------------------
#    HOURLY STATS
# ---------------------------
@api_stats.route("/stats/hourly")
def stats_hourly():
    db = SessionLocal()
    try:
        rows = (
            db.query(
                extract("hour", Event.timestamp).label("hour"),
                func.count(Event.id)
            )
            .group_by("hour")
            .order_by("hour")
            .all()
        )

        return jsonify([
            {"hour": int(h), "events": total}
            for h, total in rows
        ])

    finally:
        db.close()


# ---------------------------
#    HEATMAP STATS
# ---------------------------
@api_stats.route("/stats/heatmap")
def stats_heatmap():
    db = SessionLocal()
    try:
        rows = (
            db.query(
                extract("dow", Event.timestamp).label("dow"),
                func.count(Event.id)
            )
            .group_by("dow")
            .order_by("dow")
            .all()
        )

        return jsonify([
            {"weekday": int(dow), "events": total}
            for dow, total in rows
        ])

    finally:
        db.close()
