{
    'name': 'Example',
    'version': '18.0.1.0.0',
    'summary': 'Odoo Example Module',
    'category': 'Test',
    'author': 'Cybrosys',
    'depends': ['base', 'product'],
    'sequence':3,
    'data': [
        'security/ir.model.access.csv',
        'data/example_tag_data.xml',
        'views/example_view.xml',
        'views/example_lines_views.xml',
        'views/example_tags_views.xml',
        'views/example_menus.xml',
    ],
    'web_icon': 'static/description/icon.png',
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

