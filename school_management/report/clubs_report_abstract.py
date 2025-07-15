# -*- coding: utf-8 -*-
from odoo import models


class ClubsReportAbstract(models.AbstractModel):
    """Defines the Abstract model and SQL logic"""
    _name = 'report.school_management.clubs_report'
    _description = 'Clubs Report Abstract'

    def _get_report_values(self, docids, data=None):
        """Retrieves the data from the wizard"""
        student_id = data.get('student_id')
        club_id = data.get('club_id')
        query = """
            SELECT
                r.first_name AS student_name,r.admission_number as admission_number,
                c.name AS club_name
            FROM
                registration r
            JOIN
                registration_clubs_rel rel ON rel.registration_id = r.id
            JOIN
                clubs c ON c.id = rel.club_id
            WHERE 1=1
        """
        if student_id:
            query += f" AND r.id = {student_id}"
        if club_id:
            query += f" AND c.id = {club_id}"

        self.env.cr.execute(query)
        clubs = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'clubs.report.wizard',
            'clubs': clubs,
            'club_id' : club_id,
            'student_id': student_id,
        }
