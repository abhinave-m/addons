# -*- coding: utf-8 -*-
import json
import base64
from odoo import http, fields
from odoo.http import content_disposition, request, Response
from odoo.http import serialize_exception as _serialize_exception
from odoo.tools import html_escape
from odoo.exceptions import ValidationError
from datetime import date,datetime


class XLSXReportController(http.Controller):
    """XlsxReport generating controller"""
    @http.route('/xlsx_reports', type='http', auth='user', methods=['POST'], csrf=False)
    def get_report_xlsx(self, model, options, output_format, **kw):
        uid = request.session.uid
        report_obj = request.env[model].with_user(uid)
        options = json.loads(options)
        token = 'dummy-because-api-expects-one'
        try:
            if output_format == 'xlsx':
                report_name = options.get('report_name', 'Report')
                response = request.make_response(
                    None,
                    headers=[
                        ('Content-Type', 'application/vnd.ms-excel'),
                        ('Content-Disposition', content_disposition(f"{report_name}.xlsx"))
                    ]
                )
                report_obj.get_xlsx_report(options, response)
                response.set_cookie('fileToken', token)
                return response
        except Exception as e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
        return request.make_response(html_escape(json.dumps(error)))


def encode_image(image_data):
    """Convert binary image data to a base64-encoded UTF-8 string."""
    if image_data and isinstance(image_data, bytes):
        return base64.b64encode(image_data).decode('utf-8')
    return False

class WebsiteSchoolManagementController(http.Controller):
    """Handles the data related to Student registration, Leaves and Events"""
    @http.route(['/school_management/register', '/school_management/register/page/<int:page>'], type='http',
                auth='public', website=True)
    def student_registration_list(self, search=None, search_in='all', page=1, **kwargs):
        """Defines the list view of registrations"""
        domain = []
        searchbar_inputs = {
            'all': {'label': 'All', 'domain': ['|',
                                               ('first_name', 'ilike', search or ''),
                                               ('registration_number', 'ilike', search or '')]},
            'first_name': {'label': 'First Name', 'domain': [('first_name', 'ilike', search)]},
            'registration_number': {'label': 'Registration No', 'domain': [('registration_number', 'ilike', search)]}
        }

        if search and search_in in searchbar_inputs:
            domain += searchbar_inputs[search_in]['domain']

        students_per_page = 5

        total_students = request.env['registration'].sudo().search_count(domain)

        pager_values = request.website.pager(
            url="/school_management/register",
            total=total_students,
            page=page,
            step=students_per_page,
            url_args={'search': search, 'search_in': search_in}
        )

        students = request.env['registration'].sudo().search(
            domain,
            offset=(page - 1) * students_per_page,
            limit=students_per_page
        )

        return request.render('school_management.registration_list_template', {
            'students': students,
            'search': search,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
            'pager': pager_values,
            'no_results': not students,
        })

    @http.route('/school_management/register/new', type='http', auth='public', website=True)
    def new_registration_form(self, **kwargs):
        """Defines the new registration form"""
        departments = request.env['manage.department'].sudo().search([])
        classes = request.env['manage.class'].sudo().search([])
        return request.render('school_management.registration_form_template', {
            'departments': departments,
            'classes': classes
        })

    @http.route('/school_management/register/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_registration_form(self, **post):
        """Handles the submission of registration"""
        image_data = False
        image_file = request.httprequest.files.get('student_image')
        if image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')

        dob_str = post.get('dob')
        if not dob_str:
            return request.render('school_management.registration_form_template', {
                'error': 'Date of Birth is required.',
                'departments': request.env['manage.department'].sudo().search([]),
                'classes': request.env['manage.class'].sudo().search([]),
            })

        dob = fields.Date.from_string(dob_str)
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))

        if age < 5 or age > 15:
            return request.render('school_management.registration_form_template', {
                'error': 'Age must be between 5 and 15.',
                'departments': request.env['manage.department'].sudo().search([]),
                'classes': request.env['manage.class'].sudo().search([]),
                'form_data': post,
            })

        request.env['registration'].sudo().create({
            'first_name': post.get('first_name'),
            'last_name': post.get('last_name'),
            'dob': dob,
            'age':post.get('age'),
            'email': post.get('email'),
            'gender': post.get('gender'),
            'current_department_id': int(post.get('current_department')),
            'current_class_id': int(post.get('current_class')),
            'student_image': image_data
        })
        return request.redirect('/school_management/thanks')


    @http.route('/school_management/register/<int:student_id>', type='http', auth='public', website=True)
    def view_registration(self, student_id, **kwargs):
        """Views the existing registrations"""
        student = request.env['registration'].sudo().browse(student_id)
        departments = request.env['manage.department'].sudo().search([])
        classes = request.env['manage.class'].sudo().search([])
        student_image = encode_image(student.student_image)
        return request.render('school_management.registration_view_template', {
            'student': student,
            'departments': departments,
            'classes': classes,
            'student_image':student_image
        })

    @http.route('/school_management/register/<int:student_id>/edit', type='http', auth='public', website=True,
                methods=['POST'])
    def edit_registration(self, student_id, **post):
        """Handles the modification of existing registrations"""
        student = request.env['registration'].sudo().browse(student_id)
        departments = request.env['manage.department'].sudo().search([])
        classes = request.env['manage.class'].sudo().search([])
        student_image = student.student_image
        image_data = False
        image_file = request.httprequest.files.get('student_image')
        if image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')


        try:
            dob_str = post.get('dob')
            if dob_str:
                dob = fields.Date.from_string(dob_str)
            else:
                dob = False
            if dob:
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
                if age < 5 or age > 15:
                    raise ValidationError('Age must be between 5 and 15.')

            vals = {
                'first_name': post.get('first_name'),
                'last_name': post.get('last_name'),
                'dob': dob,
                'age':post.get('age'),
                'email': post.get('email'),
                'gender': post.get('gender'),
                'current_department_id': int(post.get('current_department')),
                'current_class_id': int(post.get('current_class')),
            }
            if image_data:
                vals['student_image'] = image_data
            student.write(vals)

            return request.redirect('/school_management/register')

        except ValidationError as e:
            if student_image and isinstance(student_image, bytes):
                student_image = base64.b64encode(student_image).decode('utf-8')
            return (request.render('school_management.registration_view_template', {
                'student': student,
                'departments': departments,
                'classes': classes,
                'error': str(e),
                'form_data': post,
                'student_image': student_image

            }))

    @http.route('/getclasses/<int:department_id>', type='http', auth='public', methods=['GET'])
    def get_classes(self, department_id):
        """Retrieves the classes based on the department chosen"""
        classes = request.env['manage.class'].sudo().search([('department_id', '=', department_id)])
        result = [{'id': c.id, 'name': c.name} for c in classes]
        return Response(json.dumps({'classes': result}), content_type='application/json;charset=utf-8')

    @http.route(['/school_management/leave','/school_management/leave/page/<int:page>'], type='http', auth='public', website=True)
    def leave_list(self, search=None, search_in='all', page=1, **kwargs):
        """Defines the list view of leaves"""
        domain = []
        searchbar_inputs = {
            'all': {
                'label': 'All',
                'domain': ['|', ('student_id.first_name', 'ilike', search or ''), ('reason', 'ilike', search or '')]
            },
            'student_id': {'label': 'Student Name', 'domain': [('student_id.first_name', 'ilike', search)]},
            'reason': {'label': 'Reason', 'domain': [('reason', 'ilike', search)]},
        }

        if search and search_in in searchbar_inputs:
            domain += searchbar_inputs[search_in]['domain']
            
        leaves_per_page = 3
        total_leaves = request.env['leave'].sudo().search_count(domain)
        pager_values = request.website.pager(
            url="/school_management/leave",
            total=total_leaves,
            page=page,
            step=leaves_per_page,
            url_args={'search': search, 'search_in': search_in}
        )
        leaves = request.env['leave'].sudo().search(
            domain,
            offset=(page - 1) * leaves_per_page,
            limit=leaves_per_page
        )

        return request.render('school_management.leave_list_template', {
            'leaves': leaves,
            'search': search,
            'search_in': search_in,
            'searchbar_inputs': searchbar_inputs,
            'pager': pager_values,
            'no_results': not leaves,
        })
    

    @http.route('/school_management/leave/new', type='http', auth='public', website=True)
    def new_leave_form(self, **kwargs):
        """Handles the creation of new leaves"""
        students = request.env['registration'].sudo().search([])
        return request.render('school_management.leave_form_template', {
            'students': students,
        })

    @http.route('/school_management/leave/submit', type='http', auth='public', website=True, methods=['POST'])
    def submit_leave_form(self, **post):
        """Handles the submission of leaves"""
        start_date = fields.Date.from_string(post.get('start_date'))
        end_date = fields.Date.from_string(post.get('end_date'))
        if start_date > end_date:
            return request.render('school_management.leave_form_template', {
                'error': 'End date must be after start date.',
                'students': request.env['registration'].sudo().search([]),
                'classes': request.env['manage.class'].sudo().search([]),
                'form_data': post,
            })

        request.env['leave'].sudo().create({
            'student_id': int(post.get('student_id')),
            'class_id': post.get('class_id'),
            'start_date': start_date,
            'end_date': end_date,
            'reason': post.get('reason'),
        })

        return request.redirect('/school_management/thanks')

    @http.route('/school_management/leave/<int:leave_id>', type='http', auth='public', website=True)
    def view_leave(self, leave_id, **kwargs):
        """Views the existing leaves"""
        leave = request.env['leave'].sudo().browse(leave_id)
        return request.render('school_management.leave_view_template', {
            'leave': leave,
        })

    @http.route('/school_management/leave/<int:leave_id>/edit', type='http', auth='public', website=True,
                methods=['POST'])
    def edit_leave(self, leave_id, **post):
        """Handles the modification of existing leaves"""
        leave = request.env['leave'].sudo().browse(leave_id)
        students = request.env['registration'].sudo().search([])

        try:
            start_date = fields.Date.from_string(post.get('start_date'))
            end_date = fields.Date.from_string(post.get('end_date'))

            if start_date > end_date:
                raise ValidationError("End date must be after start date.")

            leave.write({
                'start_date': post.get('start_date'),
                'end_date': post.get('end_date'),
                'reason': post.get('reason'),
            })
            return request.redirect('/school_management/leave')

        except ValidationError as e:
            return request.render('school_management.leave_view_template', {
                'leave': leave,
                'students': students,
                'error': str(e),
                'form_data': post,
            })

    @http.route('/school_management/get_class', type='json', auth='public', methods=['POST'])
    def get_class(self, student_id=None, **kwargs):
        """Retrieves the classes based on the student chosen"""
        student_id = int(student_id) if student_id else 0
        student = request.env['registration'].sudo().browse(student_id)
        if student.exists() and student.current_class_id:
            return {'class_name': student.current_class_id.name}
        else:
            return {'class_name': ''}

    @http.route(['/school_management/events','/school_management/events/page/<int:page>'], type='http', auth='public', website=True)
    def list_events(self, page=1, **kwargs):
        """Defines the list view of events"""
        search = kwargs.get('search')
        search_in = kwargs.get('search_in', 'name')
        domain = []

        searchbar_inputs = {
            'name': {'label': 'Event Name'},
            'club': {'label': 'Club Name'},
            'status': {'label': 'Status'},
        }

        if search:
            if search_in == 'name':
                domain += [('name', 'ilike', search)]
            elif search_in == 'club':
                domain += [('club_id.name', 'ilike', search)]
            elif search_in == 'status':
                domain += [('status', 'ilike', search)]
                
        events_per_page = 3
        total_events = request.env['events.club'].sudo().search_count(domain)
        pager_values = request.website.pager(
            url="/school_management/events",
            total=total_events,
            page=page,
            step=events_per_page,
            url_args={'search': search, 'search_in': search_in}
        )
        events = request.env['events.club'].sudo().search(
            domain,
            offset=(page - 1) * events_per_page,
            limit=events_per_page
        )
        return request.render('school_management.event_list_template', {
            'events': events,
            'search': search,
            'search_in': search_in,
            'pager':pager_values,
            'searchbar_inputs': searchbar_inputs,
        })

    @http.route(['/school_management/events/<int:event_id>', '/school_management/events/new'], type='http',
                    auth='public', website=True)
    def view_event(self, event_id=None, **kwargs):
        """Views the existing events"""
        event = None
        if event_id:
            event = request.env['events.club'].sudo().browse(event_id)
            if not event.exists():
                return request.not_found()
        return request.render('school_management.event_form_template', {'event': event})

    @http.route('/school_management/events/submit', type='http', auth='public', methods=['POST'], website=True)
    def submit_event(self, **post):
        """Handles the submission of events"""
        def convert_html_datetime(dt_str):
            """Converts an HTML datetime-local string to a standard datetime format."""
            if dt_str:
              return datetime.strptime(dt_str, '%Y-%m-%dT%H:%M').strftime('%Y-%m-%d %H:%M:%S')
            return None

        event_id = post.get('event_id', 0)
        start_date = convert_html_datetime(post.get('start_date'))
        end_date = convert_html_datetime(post.get('end_date'))
        values = {
                  'name': post.get('name'),
                    'club_id': int(post.get('club_id') or 0),
                    'start_date': start_date,
                    'end_date': end_date,
                    'desc': post.get('desc'),
                }

        event = request.env['events.club'].sudo()
        if event_id:
            event.browse(event_id).write(values)
        else:
            event.create(values)

        return request.redirect('/school_management/events')

    @http.route('/school_management/thanks', type='http', auth='public', website=True)
    def school_thank_you(self, **kwargs):
        """Returns a ThankYou page after submitting forms"""
        return request.render('school_management.thank_you_template')






