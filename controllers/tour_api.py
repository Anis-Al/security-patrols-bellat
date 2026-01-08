from odoo import http
from odoo.http import request

from ._common import _parse_int, _serialize_tour, _get_param


class SecurityTourApi(http.Controller):
    @http.route("/api/security/tours", type="json", auth="user", methods=["GET"])
    def list_tours(self, **kwargs):
        agent_id = _parse_int(_get_param("agent_id"))
        states = _get_param("states")
        states_list = []
        if states:
            if isinstance(states, list):
                states_list = states
            elif isinstance(states, str):
                states_list = [s.strip() for s in states.split(",") if s.strip()]

        domain = []
        # Auto-filter by current agent if no agent_id provided
        if not agent_id:
            current_user = request.env.user
            employee = request.env["hr.employee"].sudo().search(
                [("user_id", "=", current_user.id)], limit=1
            )
            if employee:
                agent_id = employee.id
        
        if agent_id:
            domain.append(("agent_id", "=", agent_id))
        if states_list:
            domain.append(("state", "in", states_list))
        else:
            domain.append(("state", "in", ["planned", "in_progress"]))

        tours = request.env["security.tour"].sudo().search(domain)
        return [_serialize_tour(t) for t in tours]

    @http.route("/api/security/tour/<int:tour_id>", type="json", auth="user", methods=["GET"])
    def get_tour(self, tour_id, **kwargs):
        agent_id = _parse_int(_get_param("agent_id"))
        domain = [("id", "=", tour_id)]
        if agent_id:
            domain.append(("agent_id", "=", agent_id))
        tour = request.env["security.tour"].sudo().search(domain, limit=1)
        if not tour:
            return {"error": "not_found"}
        return _serialize_tour(tour)

    @http.route(
        "/api/security/tour/<int:tour_id>/progress", type="json", auth="user", methods=["GET"]
    )
    def tour_progress(self, tour_id, **kwargs):
        agent_id = _parse_int(_get_param("agent_id"))
        domain = [("id", "=", tour_id)]
        if agent_id:
            domain.append(("agent_id", "=", agent_id))
        tour = request.env["security.tour"].sudo().search(domain, limit=1)
        if not tour:
            return {"error": "not_found"}
        required = len(tour.checkpoint_ids)
        logged = len(tour.log_ids)
        return {
            "tour_id": tour.id,
            "state": tour.state,
            "required_checkpoints": required,
            "logged_checkpoints": logged,
            "completed": tour.state == "finished" or (required > 0 and logged >= required),
        }

    @http.route("/api/security/agent/current", type="json", auth="user", methods=["GET"])
    def get_current_agent(self, **kwargs):
        """Get the current user's employee/agent record"""
        current_user = request.env.user
        employee = request.env["hr.employee"].sudo().search(
            [("user_id", "=", current_user.id)], limit=1
        )
        if not employee:
            return {"error": "agent_not_found", "message": "Current user has no associated employee record"}
        
        return {
            "id": employee.id,
            "name": employee.name,
            "is_agent": employee.is_agent if hasattr(employee, "is_agent") else False,
            "status": employee.status if hasattr(employee, "status") else None,
        }



