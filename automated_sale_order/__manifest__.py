{
    'name': "Automated SO",
    'version': '18.0.1.0.0',
    'depends': ['base', 'product', 'sale'],
    'author': "AMR",
    'category': 'Category',
    'description': """
    A model to automate SO from product section
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/automated_product_views.xml',
        'wizard/automated_so_wizard.xml'
    ],
    'installable': True,
    'application': True,
}
