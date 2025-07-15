# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError


class LeaveReportAbstract(models.AbstractModel):
    """Defines the Abstract model and SQL logic"""
    _name = 'report.school_management.leave_report'
    _description = 'Leave Report Abstract'

    def _get_report_values(self, docids, data=None):
        """Retrieves the data from the wizard"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        class_id = data.get('class_id')
        student_ids = data.get('student_ids')  # Corrected key here

        query = """
            SELECT
                l.id, l.reason, l.start_date, l.end_date,
                l.total_days AS total_days,
                r.first_name AS student_name, r.admission_number, r.email, r.phone_num AS phone,
                c.name AS class_name
            FROM leave l
            JOIN registration r ON r.id = l.student_id
            LEFT JOIN manage_class c ON c.id = l.class_id
            WHERE 1=1
        """

        params = []

        if start_date:
            query += " AND l.start_date >= %s"
            params.append(start_date)
        if end_date:
            query += " AND l.end_date <= %s"
            params.append(end_date)
        if class_id:
            query += " AND l.class_id = %s"
            params.append(class_id)
        if student_ids:
            if len(student_ids) == 1:
                query += " AND l.student_id = %s"
                params.append(student_ids[0])
            else:
                query += " AND l.student_id = ANY(%s)"
                params.append(student_ids)

        self.env.cr.execute(query, tuple(params))
        leaves = self.env.cr.dictfetchall()
        if not leaves:
            raise UserError("No Records Found")

        return {
            'doc_model': 'leave.report.wizard',
            'leaves': leaves,
        }
