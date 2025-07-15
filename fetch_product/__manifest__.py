{
    'name': 'Fetch products from Odoo 17',
    'version': '18.0.1.0.0',
    'category': 'Category',
    'summary': 'Fetch products from Odoo 17 to Odoo 18 ',
    'author': 'AMR',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',

        'views/fetch_product_views.xml',

        'wizard/fetch_product_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
}
