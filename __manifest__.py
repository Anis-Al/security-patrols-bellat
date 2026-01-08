{
    "name": "Security Patrol",
    "version": "17.0.0.1",
    "category": "Services",
    "summary": "Security Patrol",
    "description": """
    Security Patrol
    """,
    "author": "Alim Anis",
    "website": "www.bellat.dz",
    "license": "LGPL-3",
    'external_dependencies': {
        'python': ['segno'],
    },
    "depends": ["base","mail","hr","web","dh_map_widget"],
    "data": [
        "security/ir.model.access.csv",
        "views/agent_views.xml",
        "views/site_views.xml",
        "views/checkpoint_views.xml",
        "views/res_config_settings_views.xml",
        "views/tour_template_views.xml",
        "views/tour_views.xml",
        "views/tour_log_views.xml",
        "views/incident_views.xml",
        "views/menus.xml",
        "report/checkpoint_qr_code_report.xml",
        "data/ir_sequence_data.xml"
    ],
    "images" : ['static/description/icon.png'],
    "installable":True,
    "application": True,
    "auto_install" : False
}