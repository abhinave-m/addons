{
    "name": "QR code generator",
    "summary": "An icon that generates QR code",
    "version": "18.0.1.0.0",
    "category": "Category",
    "depends": ['base'],
    'assets': {
       'web.assets_backend': [
           'qr_code/static/src/js/systray_icon.js',
           'qr_code/static/src/xml/systray_icon.xml',
       ],
    },
    "installable": True,
    "application": False,
}