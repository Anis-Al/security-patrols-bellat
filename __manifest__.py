{
    "name": "Security Patrol",

    "summary": "Security Patrol",

    "description": """
    Security Patrol
    """,

    "version": "1.0",

    "category": "Services",

    "license": "LGPL-3",

    "depends": ["base","mail","hr","web","dh_map_widget"],
    
    'external_dependencies': {
        'python': ['segno'],
    },
    
    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/agent_views.xml",
        "views/site_views.xml",
        "views/checkpoint_views.xml",
        "views/res_config_settings_views.xml",
        "views/tour_template_views.xml",
        "views/tour_views.xml",
        "views/tour_log_views.xml",
        "views/incident_views.xml",
        "views/menus.xml",
        "report/checkpoint_qr_code_report.xml"
    ],

    "author": "Alim Anis",

    "website": "www.bellat.dz",

    "application": True,

}