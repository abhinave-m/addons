{
    'name': "Estate",
    'version': '18.0.1.0.0',
    'depends': ['base'],
    'author': "AMR",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offers_views.xml',
        'views/estate_menu.xml'
    ],
    'installable': True,
    'application': True,
}
