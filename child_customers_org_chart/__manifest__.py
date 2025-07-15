{
    'name': "Child Customers Org Chart",
    'version': '18.0.1.0.0',
    'depends': ['base','hr_org_chart'],
    'author': "AMR",
    'category': 'Category',
    'description': """
    Helps in adding parents to customers
    """,
    # data files always loaded at installation
    'data': [
        'views/res_partner_views.xml',
        'views/customer_hierarchy_views.xml',
        'views/res_partner_search_filter.xml'
    ],
    'assets': {
        'web.assets_backend': [
            'child_customers_org_chart/static/src/css/customer_org_chart.scss',
            'child_customers_org_chart/static/src/fields/customer_org_chart.js',
            'child_customers_org_chart/static/src/xml/customer_org_chart.xml',
        ],
    },
    'installable': True,
    'application': False,
}
