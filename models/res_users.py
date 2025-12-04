from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    api_key = fields.Char(
        string="API Key",
        help="Clave para permitir acceso desde la aplicación FitData."
    )
