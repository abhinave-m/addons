{
    "name": "MultiSafepay Payment Acquirer",
    "summary": "Integrate MultiSafepay with Odoo Website Checkout",
    "version": "18.0.1.0.0",
    "category": "Category",
    "depends": ['base', 'payment', 'account'],
    'imagess': [
        'static/description/multi.png'
    ],
    "data": [
        "data/payment_provider_data.xml",
        "views/payment_provider_views.xml",
        "views/payment_templates.xml",
    ],
    "installable": True,
    "application": False,
}