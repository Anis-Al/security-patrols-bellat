from odoo import http
from odoo.http import request

from ._common import _parse_int, _serialize_checkpoint, _get_param


class SecurityCheckpointApi(http.Controller):
    @http.route(
        "/api/security/checkpoint/<string:identifier>", type="json", auth="user", methods=["GET"]
    )
    def get_checkpoint(self, identifier, **kwargs):
        checkpoint = (
            request.env["security.checkpoint"]
            .sudo()
            .search([("identifier", "=", identifier)], limit=1)
        )
        if not checkpoint:
            return {"error": "not_found"}
        return _serialize_checkpoint(checkpoint)

    @http.route("/api/security/checkpoints", type="json", auth="user", methods=["GET"])
    def list_checkpoints(self, **kwargs):
        site_id = _parse_int(_get_param("site_id"))
        domain = []
        if site_id:
            domain.append(("site_id", "=", site_id))
        checkpoints = request.env["security.checkpoint"].sudo().search(domain)
        return [_serialize_checkpoint(cp) for cp in checkpoints]



