{
    'name': "Survey contact creation",
    'version': '18.0.1.0.0',
    'depends': ['base','survey', 'contacts'],
    'author': "AMRan",
    'category': 'Category',
    'description': """
    Helps in creation of contacts from surveys
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        
        'views/survey_form_views.xml',
    ],
    'installable': True,
    'application': False,
}
