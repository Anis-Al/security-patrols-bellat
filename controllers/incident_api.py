from odoo import http
from odoo.http import request

from ._common import _parse_int


class SecurityIncidentApi(http.Controller):
    @http.route("/api/security/incident", type="json", auth="user", methods=["POST"])
    def create_incident(self, **payload):
        payload = payload or {}
        log_id = _parse_int(payload.get("log_id"))
        if not log_id:
            return {"error": "log_required"}
        vals = {
            "log_id": log_id,
            "title": payload.get("title"),
            "description": payload.get("description"),
            "severity": payload.get("severity", "medium"),
            "category": payload.get("category", "other"),
        }
        incident = request.env["security.incident"].sudo().create(vals)
        photos = payload.get("photos") or []
        attachment_ids = []
        for idx, photo in enumerate(photos):
            if not photo:
                continue
            attachment = request.env["ir.attachment"].sudo().create(
                {
                    "name": f"incident_photo_{incident.id}_{idx + 1}.png",
                    "datas": photo,
                    "res_model": "security.incident",
                    "res_id": incident.id,
                    "mimetype": "image/png",
                }
            )
            attachment_ids.append(attachment.id)
        if attachment_ids:
            incident.photo_ids = [(6, 0, attachment_ids)]
        return {"id": incident.id, "status": incident.status}

    @http.route("/api/security/incidents", type="json", auth="user", methods=["GET"])
    def list_incidents(self, **kwargs):
        params = request.params
        tour_id = _parse_int(params.get("tour_id"))
        log_id = _parse_int(params.get("log_id"))
        domain = []
        if tour_id:
            domain.append(("tour_id", "=", tour_id))
        if log_id:
            domain.append(("log_id", "=", log_id))

        incidents = request.env["security.incident"].sudo().search(domain, order="create_date desc")
        return [
            {
                "id": inc.id,
                "tour_id": inc.tour_id.id,
                "log_id": inc.log_id.id,
                "checkpoint_id": inc.checkpoint_id.id if inc.checkpoint_id else None,
                "title": inc.title,
                "description": inc.description,
                "severity": inc.severity,
                "category": inc.category,
                "status": inc.status,
                "reported_by": inc.reported_by.id if inc.reported_by else None,
                "reported_date": inc.reported_date,
                "assigned_to": inc.assigned_to.id if inc.assigned_to else None,
                "resolved_date": inc.resolved_date,
            }
            for inc in incidents
        ]



