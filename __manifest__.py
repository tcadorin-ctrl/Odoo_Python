# -*- coding: utf-8 -*-
{
    "name": "GenteFit Integration",
    "version": "0.1",
    "summary": "Import/export XML between GenteFit and Odoo",
    "author": "TuNombre",
    "category": "Tools",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/gentefit_views.xml",
        # si quieres que schema esté disponible como dato:
        "data/genteFit_schema.xsd",
    ],
    "installable": True,
    "application": False,
}
