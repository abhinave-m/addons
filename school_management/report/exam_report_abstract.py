# -*- coding: utf-8 -*-
from odoo import models


class ExamReportAbstract(models.AbstractModel):
    """Defines the Abstract model and SQL logic"""
    _name = 'report.school_management.exam_report'
    _description = 'Exam Report Abstract'

    def _get_report_values(self, docids, data=None):
        """Retrieves the data from the wizard"""
        student_id = data.get('student_id')
        class_id = data.get('class_id')
        exam_id = data.get('exam_id')

        query = """
            SELECT
                r.first_name AS student_name,r.admission_number as admission_number,
                c.name AS class_name,
				e.name AS exam_name
            FROM
                registration r
            JOIN
                manage_class c ON c.id = r.current_class_id
            JOIN
                exam e ON c.id = e.class_id
            WHERE 1=1
        """
        if student_id:
            query += f" AND r.id = {student_id}"
        if class_id:
            query += f" AND c.id = {class_id}"
        if exam_id:
            query += f" AND e.id = {exam_id}"

        self.env.cr.execute(query)
        exams = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'exam.report.wizard',
            'exams': exams,

        }
