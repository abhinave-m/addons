{
    "name": "Website Decimal Quantity",
    "summary": "Adds decimal quantity in shop",
    "version": "18.0.1.0.0",
    "category": "Category",
    "depends": ['website_sale'],
    "data":{

    },
    'assets': {
       'web.assets_frontend': [
            'website_decimal_quantity/static/src/js/decimal.js',
       ],
    },
    "installable": True,
    "application": False,
}