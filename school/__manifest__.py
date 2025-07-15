{
    'name': "School",
    'version': '18.0.1.0.0',
    'depends': ['base'],
    'author': "AMR",
    'category': 'Category',
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'views/student_views.xml',
        'views/teacher_views.xml',
        'views/grade_views.xml',
        'views/subject_views.xml',
        'views/school_menu.xml'

    ],
    'installable': True,
    'application': True,
}
