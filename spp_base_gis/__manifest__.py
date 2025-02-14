# Part of OpenSPP. See LICENSE file for full copyright and licensing details.
{
    "name": "OpenSPP Base GIS",
    "category": "OpenSPP",
    "version": "17.0.1.0.0",
    "sequence": 1,
    "author": "OpenSPP.org",
    "website": "https://github.com/OpenSPP/openspp-modules",
    "license": "LGPL-3",
    "development_status": "Beta",
    "maintainers": ["jeremi", "gonzalesedwin1123", "reichie020212"],
    "depends": ["base", "web", "contacts"],
    "external_dependencies": {"python": ["shapely", "pyproj", "geojson"]},
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/ir_model_view.xml",
        "views/ir_view_view.xml",
        "views/raster_layer_view.xml",
        "views/data_layer_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "spp_base_gis/static/src/js/**/*",
            "spp_base_gis/static/src/css/style.css",
            "web/static/src/libs/fontawesome/css/font-awesome.css",
            ("include", "web._assets_helpers"),
            "web/static/src/scss/pre_variables.scss",
            "web/static/lib/bootstrap/scss/_variables.scss",
            ("include", "web._assets_bootstrap"),
        ]
    },
    "demo": [],
    "images": [],
    "application": True,
    "installable": True,
    "auto_install": False,
    "pre_init_hook": "init_postgis",
}
