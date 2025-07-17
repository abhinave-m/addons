{
    "name": "Live Weather",
    "summary": "An icon that shows live weather",
    "version": "18.0.1.0.0",
    "category": "Category",
    "depends": ['base','base_setup'],
    "data":{
        'views/res_config_settings_views.xml'
    },
    'assets': {
       'web.assets_backend': [
           'weather/static/src/js/weather.js',
           'weather/static/src/xml/weather.xml',
       ],
    },
    "installable": True,
    "application": False,
}