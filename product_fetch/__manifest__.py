{
    'name': 'Product fetch from Odoo 17',
    'version': '18.0.1.0.0',
    'category': 'Category',
    'summary': 'Fetch products from Odoo 17 to Odoo 18 ',
    'author': 'AMR',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',

        'views/product_fetch_views.xml',

        'wizard/product_fetch_wizard_views.xml',
    ],
    'installable': True,
    'application': False,
}
