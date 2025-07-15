# -*- coding: utf-8 -*-
from odoo import models
from datetime import date
from odoo.exceptions import UserError


class StudentReportAbstract(models.AbstractModel):
    """Defines the Abstract model and SQL logic"""
    _name = 'report.school_management.student_report'
    _description = 'Student Report Abstract'

    def _get_report_values(self, docids, data=None):

        """Retrieves the data from the wizard"""
        wizard = self.env['student.report.wizard'].browse(docids)
        class_id = data.get('class_id')
        department_id = data.get('department_id')

        query = """
            SELECT
            r.first_name as student_name,r.admission_number as admission_number,r.email as email, r.phone_num as phone,
            c.name AS class_name,
			d.name AS department_name
            FROM
                registration r
            JOIN
                manage_class c ON r.current_class_id  = c.id 
			JOIN 
				manage_department d on d.id = r.current_department_id
            WHERE 1=1

        """

        if department_id:
            query += f" AND r.current_department_id = {department_id}"
        if class_id:
            query += f" AND r.current_class_id = {class_id}"


        self.env.cr.execute(query)
        students = self.env.cr.dictfetchall()
        if not students:
            raise UserError("No Records Found")

        return {
            'doc_ids': docids,
            'doc_model': 'student.report.wizard',
            'docs': wizard,
            'students': students,
        }
