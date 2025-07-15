#-*- coding: utf-8 -*-
from odoo import api, fields, models, Command
from datetime import date
from odoo.exceptions import UserError, ValidationError


class Registration(models.Model):
    """Student Registration fields declaration"""
    _name = "registration"
    _description = "Registration"
    _inherit = ['mail.thread']
    _rec_name = 'first_name'

    registration_number = fields.Char(string="Registration Number", readonly=True, default='New')

    student_image = fields.Binary("Profile Photo")

    first_name = fields.Char(required=True)
    last_name = fields.Char()
    father = fields.Char()
    mother = fields.Char()
    school_id = fields.Many2one('res.company','School', default=lambda self: self.env.company.id)
    admission_number = fields.Char(string="Admission Number", readonly=True, default='nil')
    club_ids = fields.Many2many('clubs', 'registration_clubs_rel', 'registration_id', 'club_id', string="Clubs")
    partner_id = fields.Many2one('res.partner','Partner')

    previous_academic_department = fields.Many2one('manage.department',string='Previous Academic Department')
    previous_class = fields.Many2one('manage.class',string='Previous Class')
    permanent_street = fields.Char()
    permanent_street2 = fields.Char()
    permanent_zip = fields.Char()
    permanent_city = fields.Char()
    permanent_state_id = fields.Many2one('res.country.state',string='State')
    permanent_country_id = fields.Many2one('res.country',string='Country')

    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char()
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State')
    country_id = fields.Many2one('res.country', string='Country')

    same = fields.Boolean("Same as Permanent Address")
    email = fields.Char()
    phone_num = fields.Char()
    dob = fields.Date(string="DOB")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)
    gender = fields.Selection(string="Gender", selection = [('male','Male'),('female','Female'),('others','Others')])
    registration_date = fields.Date()
    tc = fields.Char(string="TC")
    aadhar_number = fields.Char()
    status = fields.Selection([('draft','Draft'),('enroled','Enroled')],default='draft')

    exam_ids = fields.Many2many('exam', string="Exams")
    current_class_id = fields.Many2one('manage.class', string="Current Class")
    current_department_id = fields.Many2one('manage.department',string="Current Department")
    user_id = fields.Many2one('res.users', string='User')
    attendance = fields.Selection([('absent', 'Absent'), ('present', 'Present')], default='present')

    def action_draft(self):
        """Action for set to draft button"""
        registration = self.filtered(lambda s: s.status in ['enroled'])
        return registration.write({
            'status': 'draft'
             })

    @api.depends('dob')
    def _compute_age(self):
        """Calculation of age from DOB """
        for rec in self:
            if rec.dob:
                today = date.today()
                birth_date = fields.Date.from_string(rec.dob)
                rec.age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            else:
                rec.age = 0

    @api.onchange('same')
    def _onchange_same(self):
        """Copies Permanent Address to Communication Address when same as permanent is checked"""

        if self.same:
            self.street = self.permanent_street
            self.street2 = self.permanent_street2
            self.zip = self.permanent_zip
            self.city = self.permanent_city
            self.state_id = self.permanent_state_id
            self.country_id = self.permanent_country_id
        else:
            self.street = ''
            self.street2 = ''
            self.zip = ''
            self.city = ''
            self.state_id = False
            self.country_id = False


    @api.constrains('age')
    def _check_age(self):
        for rec in self:
            if not (5 <= rec.age <= 15):
                raise ValidationError("Age should be in between 5 and 15")

    def enrol(self):
        """Changes the status to Registered and creates user and partner"""
        for record in self:
            if record.admission_number == 'nil':
                record.admission_number = self.env['ir.sequence'].next_by_code('admission')
                record.status = "enroled"

    @api.model_create_multi
    def create(self, vals_list):
        """Creates Sequence number when saved"""
        for vals in vals_list:
            if vals.get("registration_number","New") == 'New':
                vals['registration_number'] = self.env['ir.sequence'].next_by_code('registration')
        return super(Registration,self).create(vals_list)

    @api.model
    def _update_daily_attendance(self):
        """Checks if leave is added for a student daily and marks their attendance"""
        today = date.today()
        students = self.search([('status','=','enroled')])

        for student in students:
            leave_exists = self.env['leave'].search_count([('student_id', '=', student.id),('start_date', '<=', today),('end_date', '>=', today)]) > 0
            student.attendance = 'absent' if leave_exists else 'present'

    def create_user(self):
        """Function to create user from students"""
        for record in self:
            if not record.email:
                raise UserError("Email is mandatory")
            else:
                group = self.env.ref('school_management.group_school_management_students')
                user_vals = {
                    'name': f"{record.first_name} {record.last_name or ''}".strip(),
                    'login': record.email,
                    'email': record.email,
                    'company_id': record.school_id.id,
                    'registration_id' : record.id,
                    'groups_id' : [Command.link(group.id)]
                }
                user = self.env['res.users'].create(user_vals)
                record.user_id = user.id




