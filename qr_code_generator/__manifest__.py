{
    "name": "QR code generator(JS)",
    "summary": "An icon that generates QR code",
    "version": "18.0.1.0.0",
    "category": "Category",
    "depends": ['base'],
    'assets': {
       'web.assets_backend': [
           'qr_code_generator/static/lib/qrcodejs/qrcode.min.js',
           'qr_code_generator/static/src/js/qr_code_generator.js',
           'qr_code_generator/static/src/xml/qr_code_generator.xml',
       ],
    },
    "installable": True,
    "application": False,
}