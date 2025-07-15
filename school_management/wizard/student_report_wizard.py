# -*- coding: utf-8 -*-
import io
import json
import xlsxwriter
from odoo import api, fields, models
from odoo.tools import json_default
from datetime import date,datetime
from odoo.exceptions import UserError


class StudentReportWizard(models.TransientModel):
    """Student Report Wizard field declaration"""
    _name = 'student.report.wizard'
    _description = 'Student Report Wizard'

    department_id = fields.Many2one('manage.department', string='Department')
    class_id = fields.Many2one('manage.class', string='Class')
    possible_class_ids = fields.Many2many('manage.class',compute='_compute_possible_class_ids',string='Possible Classes')

    @api.depends('department_id')
    def _compute_possible_class_ids(self):
        """Filters class based on the selected department"""
        for rec in self:
            if rec.department_id:
                rec.possible_class_ids = self.env['manage.class'].search([
                    ('department_id', '=', rec.department_id.id)
                ])
            else:
                rec.possible_class_ids = self.env['manage.class'].search([])

    def action_generate_pdf_report(self):
        """Trigger the report using SQL logic in the Abstract model"""
        data = {
            'department_id': self.department_id.id if self.department_id else False,
            'class_id': self.class_id.id if self.class_id else False,
        }
        return self.env.ref('school_management.action_student_report_pdf').report_action(self, data=data)

    def action_generate_xlsx_report(self):
        data = {
            'department_id': self.department_id.id if self.department_id else False,
            'class_id': self.class_id.id if self.class_id else False,
        }
        return {
            'type': 'ir.actions.report',
            'report_type': 'xlsx',
            'data': {
                'model': 'student.report.wizard',
                'options': json.dumps(data, default=json_default),
                'output_format': 'xlsx',
                'report_name': 'Student Report',
            },
        }

    def get_xlsx_report(self, data, response):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet("Student Report")

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
        company = self.env.company
        sheet.write('A1', 'Company:', header_format)
        sheet.write('B1', company.name or '', cell_format)
        sheet.write('A2', 'Email:', header_format)
        sheet.write('B2', company.email or '', cell_format)
        sheet.write('A3', 'Phone:', header_format)
        sheet.write('B3', company.phone or '', cell_format)

        sheet.merge_range('A4:D4', 'Student Report', title_format)
        rows = 3

        printed_date = datetime.today().strftime('%Y-%m-%d')
        sheet.write(f'A{rows}', 'Printed Date:', header_format)
        sheet.write(f'B{rows}', printed_date, date_format)
        rows += 1

        if data.get('department_id') or data.get('class_id'):
            if data.get('department_id'):
                department = self.env['manage.department'].browse(data['department_id']).name
                sheet.write(f'A{rows}', 'Department:', header_format)
                sheet.write(f'B{rows}', department or '', cell_format)
                rows += 1
            else:
                department = self.env['manage.class'].browse(data['class_id']).department_id.name
                sheet.write(f'A{rows}', 'Department:', header_format)
                sheet.write(f'B{rows}', department or '', cell_format)
                rows += 1


        if data.get('class_id'):
            class_name = self.env['manage.class'].browse(data['class_id']).name
            sheet.write(f'A{rows}', 'Class:', header_format)
            sheet.write(f'B{rows}', class_name or '', cell_format)
            rows += 1

        all_headers = [
            ('sl_no', 'SL No'),
            ('student_name', 'Student'),
            ('admission_number', 'Admission No'),
            ('class_name', 'Class'),
            ('department_name', 'Department'),
            ('email', 'Email'),
            ('phone', 'Phone')
        ]

        filtered_headers = []
        for key, label in all_headers:
            if key == 'department_name' and (data.get('department_id') or data.get('class_id')):
                continue
            if key == 'class_name' and data.get('class_id') :
                continue
            filtered_headers.append((key, label))

        table_start_row = rows + 1
        for col, (key, label) in enumerate(filtered_headers):
            sheet.write(table_start_row, col, label, header_format)

        report = self.env['report.school_management.student_report']
        report_data = report._get_report_values([], data)
        students = report_data.get('students', [])

        row = table_start_row
        for index, student in enumerate(students, start=1):
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
