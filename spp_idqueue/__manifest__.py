# Part of OpenSPP. See LICENSE file for full copyright and licensing details.


{
    "name": "OpenSPP ID Printing Queue",
    "category": "OpenSPP",
    "version": "17.0.1.0.0",
    "sequence": 1,
    "author": "OpenSPP.org",
    "website": "https://github.com/OpenSPP/openspp-modules",
    "license": "LGPL-3",
    "development_status": "Beta",
    "maintainers": ["jeremi", "gonzalesedwin1123"],
    "depends": [
        "base",
        "g2p_registry_base",
        "spp_idpass",
        "queue_job",
        "spp_area",
    ],
    "data": [
        "data/id_pass.xml",
        "data/queue_data.xml",
        "security/g2p_security.xml",
        "security/ir.model.access.csv",
        "views/id_queue_view.xml",
        "views/id_batch_view.xml",
        "wizard/request_id_wizard.xml",
        "wizard/batch_create_wizard.xml",
        "wizard/multi_id_request_wizard.xml",
        "views/registrant.xml",
        "views/res_config_settings.xml",
    ],
    "assets": {
        "web.assets_backend": [
            # web.FormController is already obsolete in odoo 17
            "spp_idqueue/static/src/js/form_controller.js",
        ],
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
}
