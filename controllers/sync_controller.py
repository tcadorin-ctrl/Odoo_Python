# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class GenteFitSyncController(http.Controller):

    def _auth(self):
        """Autentica usando API KEY en header: X-Api-Key"""
        api_key = request.httprequest.headers.get("X-Api-Key")

        if not api_key:
            return None

        user = request.env["res.users"].sudo().search([("api_key", "=", api_key)], limit=1)

        if not user:
            return None

        # activar entorno con permisos de ese usuario
        request.update_env(user=user)

        return user


    @http.route("/gentefit/users", type="json", auth="none", methods=["GET"])
    def get_users(self):
        user = self._auth()
        if not user:
            return {"error": "Invalid API KEY"}

        users = request.env["res.users"].sudo().search([])

        data = []
        for u in users:
            data.append({
                "id": u.id,
                "name": u.name,
                "email": u.login,
                "active": u.active,
            })

        return {"users": data}


    @http.route("/gentefit/partners", type="json", auth="none", methods=["GET"])
    def get_partners(self):
        user = self._auth()
        if not user:
            return {"error": "Invalid API KEY"}

        partners = request.env["res.partner"].sudo().search([])

        data = []
        for p in partners:
            data.append({
                "id": p.id,
                "name": p.name,
                "email": p.email,
                "phone": p.phone,
                "customer_rank": p.customer_rank,
                "is_company": p.is_company,
            })

        return {"partners": data}
