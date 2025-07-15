# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter
from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools import json_default
from datetime import date, timedelta, datetime


class LeaveReportWizard(models.TransientModel):
    """Leave Report Wizard field declaration"""
    _name = 'leave.report.wizard'
    _description = 'Leave Report Filter Wizard'

    date_filter = fields.Selection([
        ('today', 'Today'),
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
        ('custom', 'Custom Range')
    ], string="Date Filter", default='this_month')

    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    class_id = fields.Many2one('manage.class', string="Class")
    student_ids = fields.Many2many('registration', string="Student")
    possible_student_ids = fields.Many2many('registration', compute='_compute_possible_student_ids', string="Possible Student")

    @api.depends('class_id')
    def _compute_possible_student_ids(self):
        """Filters students based on the selected class"""
        for rec in self:
            if rec.class_id:
                rec.possible_student_ids = self.env['registration'].search([
                    ('current_class_id', '=', rec.class_id.id)
                ])
            else:
                rec.possible_student_ids = self.env['registration'].search([])

    @api.onchange('date_filter')
    def _onchange_date_filter(self):
        """Autofill start/end date based on selected range."""
        today = date.today()
        if self.date_filter == 'today':
            self.start_date = today
            self.end_date = today
        elif self.date_filter == 'this_week':
            start = today - timedelta(days=today.weekday())
            end = start + timedelta(days=6)
            self.start_date = start
            self.end_date = end
        elif self.date_filter == 'this_month':
            self.start_date = today.replace(day=1)
            next_month = self.start_date.replace(day=28) + timedelta(days=4)
            self.end_date = next_month - timedelta(days=next_month.day)
        else:
            self.start_date = False
            self.end_date = False

    @api.onchange('start_date', 'end_date')
    def _onchange_date_custom(self):
        """Manages the change in date fields to set it as Custom"""
        today = date.today()
        expected_start = expected_end = None
        if self.date_filter == 'today':
            expected_start = expected_end = today
        elif self.date_filter == 'this_week':
            expected_start = today - timedelta(days=today.weekday())
            expected_end = expected_start + timedelta(days=6)
        elif self.date_filter == 'this_month':
            expected_start = today.replace(day=1)
            next_month = expected_start.replace(day=28) + timedelta(days=4)
            expected_end = next_month - timedelta(days=next_month.day)
        if expected_start and expected_end:
            if self.start_date != expected_start or self.end_date != expected_end:
                self.date_filter = 'custom'

    def action_generate_pdf_report(self):
        """Trigger the report using SQL logic in the Abstract model"""
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'class_id': self.class_id.id if self.class_id else False,
            'student_ids': self.student_ids.ids if self.student_ids else False,
        }
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise UserError("End Date cannot be earlier than Start Date.")
        return self.env.ref('school_management.action_leave_report_pdf').report_action(self, data=data)

    def action_generate_xlsx_report(self):
        """Trigger the xlsx report"""
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'class_id': self.class_id.id if self.class_id else False,
            'student_ids': self.student_ids.ids if self.student_ids else False,
        }
        if self.start_date and self.end_date and self.end_date < self.start_date:
            raise UserError("End Date cannot be earlier than Start Date.")
        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data': {
                'model': 'leave.report.wizard',
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Leave Report',
            },
        }

    def get_xlsx_report(self, data, response):
        """Defines the xlsx report headers, columns and values using raw SQL"""
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Leave Report")

        title_format = workbook.add_format({
            'align': 'center',
            'bold': True,
            'font_size': 14
        })
        header_format = workbook.add_format({
            'align': 'center',
            'bold': True,
            'font_size': 10
        })
        cell_format = workbook.add_format({
            'font_size': 10,
            'align': 'center',
            'valign': 'vcenter'
        })
        date_format = workbook.add_format({
            'font_size': 10,
            'num_format': 'yyyy-mm-dd',
            'align': 'center',
            'valign': 'vcenter'
        })

        sheet.merge_range('B2:I2', 'Leave Report', title_format)

        company = self.env.company
        sheet.write('A3', 'Company :', header_format)
        sheet.write('B3', company.name, cell_format)
        sheet.write('A4', 'Email :', header_format)
        sheet.write('B4', company.email, cell_format)
        sheet.write('A5', 'Phone :', header_format)
        sheet.write('B5', company.phone, cell_format)

        rows = 6
        printed_date = datetime.today().strftime('%Y-%m-%d')
        sheet.write(f'A{rows}', 'Printed Date:', header_format)
        sheet.write(f'B{rows}', printed_date, date_format)
        rows += 1

        if data.get('start_date') and data.get('end_date'):
            sheet.write(f'A{rows}', 'Start Date:', header_format)
            sheet.write(f'B{rows}', data.get('start_date'), date_format)
            rows += 1
            sheet.write(f'A{rows}', 'End Date:', header_format)
            sheet.write(f'B{rows}', data.get('end_date'), date_format)
            rows += 1

        if data.get('class_id'):
            class_name = self.env['manage.class'].browse(data['class_id']).name
            sheet.write(f'A{rows}', 'Class:', header_format)
            sheet.write(f'B{rows}', class_name or '', cell_format)
            rows += 1

        student_ids = data.get('student_ids') or []
        if student_ids and len(student_ids) == 1:
            student = self.env['registration'].browse(student_ids[0])
            sheet.write(f'A{rows}', 'Student:', header_format)
            sheet.write(f'B{rows}', student.first_name or '', cell_format)
            rows += 1
            sheet.write(f'A{rows}', 'Admission No:', header_format)
            sheet.write(f'B{rows}', student.admission_number or '', cell_format)
            rows += 1
            sheet.write(f'A{rows}', 'Class:', header_format)
            sheet.write(f'B{rows}', student.current_class_id.name or '', cell_format)
            rows += 1
            sheet.write(f'A{rows}', 'Email:', header_format)
            sheet.write(f'B{rows}', student.email or '', cell_format)
            rows += 1
            sheet.write(f'A{rows}', 'Phone:', header_format)
            sheet.write(f'B{rows}', student.phone_num or '', cell_format)
            rows += 1

        all_headers = [
            ('sl_no', 'SL No'),
            ('student_name', 'Student'),
            ('admission_number', 'Admission No'),
            ('class_name', 'Class'),
            ('start_date', 'Start Date'),
            ('end_date', 'End Date'),
            ('total_days', 'Total Days'),
            ('reason', 'Reason'),
            ('email', 'Email'),
            ('phone', 'Phone')
        ]

        filtered_headers = []
        for key, label in all_headers:
            if len(student_ids) == 1:
                if key in ['student_name','admission_number','class_name','email','phone'] and data.get('student_ids'):
                    continue
            if key == 'class_name' and data.get('class_id'):
                continue
            filtered_headers.append((key, label))

        table_start_row = rows + 1
        for col, (key, label) in enumerate(filtered_headers):
            sheet.write(table_start_row, col, label, header_format)

        report = self.env['report.school_management.leave_report']
        report_data = report._get_report_values([], data)
        leaves = report_data.get('leaves', [])

        row = table_start_row
        for index, student in enumerate(leaves, start=1):
            row += 1
            col = 0
            for key, label in filtered_headers:
                if key == 'sl_no':
                    sheet.write(row, col, index, cell_format)
                else:
                    val = student.get(key)
                    if isinstance(val, date):
                        sheet.write(row, col, val, date_format)
                    else:
                        sheet.write(row, col, val or '', cell_format)
                col += 1

        for col in range(len(filtered_headers)):
            sheet.set_column(col, col, 20)

        workbook.close()
        output.seek(0)
        response.stream.write(output.read())
        output.close()

