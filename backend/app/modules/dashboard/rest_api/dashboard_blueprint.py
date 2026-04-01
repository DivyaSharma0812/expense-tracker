from flask import Blueprint, jsonify, request
from ..dashboard_service import DashboardService

blueprint = Blueprint("dashboard", __name__)

_service = DashboardService()


@blueprint.get("/summary")
def get_summary():
    year = request.args.get("year", type=int)
    month = request.args.get("month", type=int)
    summary = _service.get_summary(year=year, month=month)
    return jsonify({"data": summary})


@blueprint.get("/trends")
def get_trends():
    months = request.args.get("months", 6, type=int)
    trends = _service.get_trends(months=months)
    return jsonify({"data": trends})
