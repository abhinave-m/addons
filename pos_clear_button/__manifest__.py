{
    'name': "POS Clear Button",
    'version': '18.0.1.0.0',
    'depends': ['base','point_of_sale'],
    'author': "AMR",
    'category': 'Category',
    'description': """
    Adds a Clear Button in POS orders to clear order lines
    """,
    'assets': {
        'point_of_sale._assets_pos': [
        'pos_clear_button/static/src/js/clear_button.js',
        'pos_clear_button/static/src/xml/clear_button.xml',
    ],
    },
    'installable': True,
    'application': False,
}




