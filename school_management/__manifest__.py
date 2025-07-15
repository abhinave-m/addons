{
    'name': "School Management",
    'version': '18.0.10.0.0',
    'depends': ['base','mail','hr','base_automation','web','website'],
    'author': "AMR",
    'category': 'Category',
    'description': """
    A module to manage School
    """,
    # data files always loaded at installation
    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'security/ir_rules.xml',

        'report/report_template.xml',
        'report/report_action.xml',

        'data/ir_sequence_data.xml',
        'data/manage_department_data.xml',
        'data/manage_class_data.xml',
        'data/manage_subject_data.xml',
        'data/email_template_data.xml',
        'data/email_reminder_data.xml',
        'data/update_attendance_data.xml',
        'data/automated_user_creation.xml',

        'wizard/leave_report_wizard_views.xml',
        'wizard/event_report_wizard_views.xml',
        'wizard/student_report_wizard_views.xml',
        'wizard/clubs_report_wizard_views.xml',
        'wizard/exam_report_wizard_views.xml',

        'views/manage_department_views.xml',
        'views/manage_class_views.xml',
        'views/manage_subject_views.xml',
        'views/manage_academic_year_views.xml',
        'views/registration_views.xml',
        'views/clubs_views.xml',
        'views/events_club_views.xml',
        'views/res_partner_views.xml',
        'views/leave_views.xml',
        'views/exam_views.xml',
        'views/students_views.xml',
        'views/student_class.xml',
        'views/school_management_template.xml',
        'views/school_management_menu.xml',
        'views/website_menu.xml',
        'views/snippets/event_snippet_template.xml',


    ],
    'assets': {
    'web.assets_frontend': [
        'school_management/static/src/img/default_avatar.png',
        'school_management/static/src/js/student_class_autofill.js',
        'school_management/static/src/js/department_class_filter.js',
        'school_management/static/src/js/age_calculation.js',
        'school_management/static/src/js/image_preview.js',
        'school_management/static/src/xml/event_content.xml',
        'school_management/static/src/js/latest_events.js',

    ],
    'web.assets_backend': [
        'school_management/static/src/js/action_manager.js',
    ],
},
    'installable': True,
    'application': True,
}
