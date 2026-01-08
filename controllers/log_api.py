from odoo import http
from odoo.http import request

from ._common import _parse_int, _parse_float, _calculate_distance


class SecurityLogApi(http.Controller):
    @http.route("/api/security/log", type="json", auth="user", methods=["POST"])
    def create_log(self, **payload):
        payload = payload or {}
        checkpoint_id = _parse_int(payload.get("checkpoint_id"))
        checkpoint_identifier = payload.get("checkpoint_identifier")

        if not checkpoint_id and checkpoint_identifier:
            checkpoint = (
                request.env["security.checkpoint"]
                .sudo()
                .search([("identifier", "=", checkpoint_identifier)], limit=1)
            )
            if not checkpoint:
                return {"error": "checkpoint_not_found"}
            checkpoint_id = checkpoint.id

        if not checkpoint_id:
            return {"error": "checkpoint_required"}

        tour_id = _parse_int(payload.get("tour_id"))
        if not tour_id:
            return {"error": "tour_required"}

        tour = request.env["security.tour"].sudo().browse(tour_id)
        if not tour.exists():
            return {"error": "tour_not_found"}

        checkpoint = request.env["security.checkpoint"].sudo().browse(checkpoint_id)
        if not checkpoint.exists():
            return {"error": "checkpoint_not_found"}

        current_user = request.env.user
        employee = request.env["hr.employee"].sudo().search(
            [("user_id", "=", current_user.id)], limit=1
        )
        if not employee:
            return {"error": "agent_not_found", "message": "Current user has no associated employee record"}
        
        if tour.agent_id and tour.agent_id.id != employee.id:
            return {
                "error": "agent_not_assigned",
                "message": f"Tour is assigned to agent {tour.agent_id.name}, not the current user"
            }

        tour_checkpoint_ids = tour.checkpoint_ids.mapped("checkpoint_id").ids
        if checkpoint_id not in tour_checkpoint_ids:
            return {
                "error": "checkpoint_not_in_tour",
                "message": f"Checkpoint {checkpoint.name} is not part of tour {tour.name}"
            }

        if tour.strict_ordering:
            tour_lines = tour.checkpoint_ids.sorted("sequence")
            logged_checkpoint_ids = tour.log_ids.mapped("checkpoint_id").ids
            
            next_checkpoint_id = None
            for line in tour_lines:
                if line.checkpoint_id.id not in logged_checkpoint_ids:
                    next_checkpoint_id = line.checkpoint_id.id
                    break
            
            if next_checkpoint_id is None:
                pass
            elif checkpoint_id != next_checkpoint_id:
                next_checkpoint = request.env["security.checkpoint"].sudo().browse(next_checkpoint_id)
                return {
                    "error": "wrong_sequence",
                    "message": f"Checkpoints must be scanned in order. Next checkpoint is: {next_checkpoint.name}",
                    "next_checkpoint_id": next_checkpoint_id,
                    "next_checkpoint_name": next_checkpoint.name,
                }

        agent_lat = _parse_float(payload.get("latitude"))
        agent_lon = _parse_float(payload.get("longitude"))
        checkpoint_lat = checkpoint.latitude
        checkpoint_lon = checkpoint.longitude

        if agent_lat is not None and agent_lon is not None and \
           checkpoint_lat is not None and checkpoint_lon is not None:
            distance = _calculate_distance(agent_lat, agent_lon, checkpoint_lat, checkpoint_lon)
            if distance is not None:
                max_distance = tour.max_checkpoint_distance or int(request.env['ir.config_parameter'].sudo().get_param(
                    'security_patrol.max_checkpoint_distance', 50
                ))
                if distance > max_distance:
                    return {
                        "error": "distance_exceeded",
                        "message": f"Agent is {distance:.1f}m away from checkpoint (max: {max_distance}m)",
                        "distance": round(distance, 1),
                        "max_distance": max_distance,
                    }

        photo_selfie = payload.get("photo_selfie")
        photo_place = payload.get("photo_place")
        
        if tour.require_selfie and not photo_selfie:
            return {
                "error": "photo_selfie_required",
                "message": "Selfie photo is required for this tour"
            }
        
        if tour.require_photo_place and not photo_place:
            return {
                "error": "photo_place_required",
                "message": "Photo of place is required for this tour"
            }

        vals = {
            "tour_id": tour_id,
            "checkpoint_id": checkpoint_id,
            "latitude": agent_lat,
            "longitude": agent_lon,
            "status": payload.get("status", "ok"),
            "comment": payload.get("comment"),
        }
        if photo_selfie:
            vals["photo_selfie"] = photo_selfie
        if photo_place:
            vals["photo_place"] = photo_place

        log = request.env["security.tour.log"].sudo().create(vals)
        return {
            "id": log.id,
            "tour_id": log.tour_id.id,
            "tour_state": log.tour_id.state,
            "completed": log.tour_id.state == "finished",
        }

    @http.route("/api/security/logs", type="json", auth="user", methods=["GET"])
    def list_logs(self, **kwargs):
        tour_id = _parse_int(request.params.get("tour_id"))
        domain = []
        if tour_id:
            domain.append(("tour_id", "=", tour_id))
        logs = request.env["security.tour.log"].sudo().search(domain, order="time desc")
        return [
            {
                "id": log.id,
                "tour_id": log.tour_id.id,
                "checkpoint_id": log.checkpoint_id.id,
                "time": log.time,
                "latitude": log.latitude,
                "longitude": log.longitude,
                "status": log.status,
                "comment": log.comment,
                "require_selfie": log.require_selfie,
                "require_photo_place": log.require_photo_place,
                "has_selfie": bool(log.photo_selfie),
                "has_photo_place": bool(log.photo_place),
            }
            for log in logs
        ]



