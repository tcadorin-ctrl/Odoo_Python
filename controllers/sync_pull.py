from odoo import http
from odoo.http import request

class FitDataPullController(http.Controller):

    @http.route('/fitdata/sync/pull', type='json', auth='user', csrf=False)
    def pull_data(self):
        """Devuelve res.partner y res.users en formato JSON"""

        partners = request.env['res.partner'].sudo().search([])

        users = request.env['res.users'].sudo().search([])

        data = {
            "partners": [
                {
                    "id": p.id,
                    "name": p.name,
                    "email": p.email,
                    "phone": p.phone,
                    "street": p.street,
                    "city": p.city,
                    "zip": p.zip,
                    "country": p.country_id.name if p.country_id else None,
                }
                for p in partners
            ],
            "users": [
                {
                    "id": u.id,
                    "name": u.name,
                    "login": u.login,
                    "active": u.active,
                    "email": u.email,
                }
                for u in users
            ]
        }

        return data
