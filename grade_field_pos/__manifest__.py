{
    'name': "Grade Field",
    'version': '18.0.1.0.0',
    'depends': ['base','point_of_sale','product'],
    'author': "AMR",
    'category': 'Category',
    'description': """
    Adds a Grade field on Product form and shows it in POS 
    """,
    # data files always loaded at installation
    'data': [
        'views/grade_field_products.xml'
    ],
    'assets': {
        'point_of_sale._assets_pos': [
        'grade_field_pos/static/src/js/product_grade.js',
        'grade_field_pos/static/src/xml/product_grade_pos_card.xml',
        'grade_field_pos/static/src/xml/product_grade_receipt.xml',
    ],
    },
    'installable': True,
    'application': False,
}




