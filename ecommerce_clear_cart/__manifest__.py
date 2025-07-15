{
    'name': "Ecommerce Clear Cart",
    'version': '18.0.1.0.0',
    'depends': ['base','web','website'],
    'author': "AMR",
    'category': 'Category',
    'description': """
    Clears the cart in Ecommerce site
    """,
    # data files always loaded at installation
    'data': [
        'views/cart_views.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'ecommerce_clear_cart/static/src/js/clear_cart.js',
    ],
    },
    'installable': True,
    'application': False,
}


