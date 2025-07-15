{
    'name': 'Dashboard',
    'version': '18.0.1.0.0',
    'category': 'Category',
    'summary': 'Dasboard view of inventory',
    'author': 'AMR',
    'depends': ['stock','stock_account'],
    'data': [
        'views/inventory_dashboard_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'inventory_dashboard/static/lib/chart.min.js',
            'inventory_dashboard/static/src/js/dashboard.js',
            'inventory_dashboard/static/src/xml/dashboard.xml',
        ],
    },
    'installable': True,
    'application': False,
}
