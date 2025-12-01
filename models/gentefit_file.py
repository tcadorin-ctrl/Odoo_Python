# -*- coding: utf-8 -*-
from odoo import models, fields, api
import base64
from datetime import datetime

class GenteFitFile(models.Model):
    _name = 'gentefit.file'
    _description = 'GenteFit imported/exported file'

    name = fields.Char(string='Name', required=True)
    filename = fields.Char(string='File name')
    raw_xml = fields.Text(string='Raw XML (base64)', help='Raw XML content encoded as base64')
    batch_id = fields.Char(string='BatchId')
    import_date = fields.Datetime(string='Import Date', default=lambda self: fields.Datetime.now())
    state = fields.Selection([('draft','Draft'), ('imported','Imported')], default='draft')

