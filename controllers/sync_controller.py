# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class GenteFitSyncController(http.Controller):

    def _auth(self):
        """Autentica mediante API KEY en header: X-Api-Key"""
        api_key = request.httprequest.headers.get("X-Api-Key")

        if not api_key:
            return None

        user = request.env["res.users"].sudo().search([
            ("api_key", "=", api_key)
        ], limit=1)

        if not user:
            return None

        # Hacer que el entorno use este usuario
        request.env = request.env(user=user)
        return user

    # ----------------------------------------------------------
    # GET USERS
    # ----------------------------------------------------------
    @http.route("/gentefit/users", type="http", auth="public", methods=["GET"], csrf=False)
    def get_users(self, **kwargs):
        user = self._auth()
        if not user:
            return request.make_json_response({"error": "Invalid API KEY"}, status=401)

        users = request.env["res.users"].sudo().search([])

        data = [{
            "id": u.id,
            "name": u.name,
            "email": u.login,
            "active": u.active,
        } for u in users]

        return request.make_json_response({"users": data}, status=200)

    # ----------------------------------------------------------
    # GET PARTNERS
    # ----------------------------------------------------------
    @http.route("/gentefit/partners", type="http", auth="public", methods=["GET"], csrf=False)
    def get_partners(self, **kwargs):
        user = self._auth()
        if not user:
            return request.make_json_response({"error": "Invalid API KEY"}, status=401)

        partners = request.env["res.partner"].sudo().search([])

        data = [{
            "id": p.id,
            "name": p.name,
            "email": p.email,
            "phone": p.phone,
            "customer_rank": p.customer_rank,
            "is_company": p.is_company,
        } for p in partners]

        return request.make_json_response({"partners": data}, status=200)
