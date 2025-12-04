# -*- coding: utf-8 -*-
{
    "name": "GenteFit Sync API",
    "version": "1.0",
    "summary": "API para sincronizar con FitData (.NET)",
    "author": "FitData",
    "category": "Tools",
    "license": "LGPL-3",
    "depends": ["base"],
    "data": [
        "security/ir.model.access.csv",
        "views/res_users_views.xml",   # 👈 IMPORTANTE
    ],
    "installable": True,
    "application": False,
}
