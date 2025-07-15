# -*- coding: utf-8 -*-
from odoo import models
from datetime import date


class EventReportAbstract(models.AbstractModel):
    """Defines the Abstract model and SQL logic"""
    _name = 'report.school_management.event_report'
    _description = 'Event Report Abstract'

    def _get_report_values(self, docids, data=None):
        """Retrieves the data from the wizard"""
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        club_id = data.get('club_id')

        query = """
            SELECT
            e.name as event_name, e.start_date, e.end_date,
            c.name AS club_name
            FROM
                events_club e
            JOIN
                clubs c ON c.id = e.club_id
            WHERE 1=1
        """

        if start_date:
            query += f" AND e.start_date >= '{start_date}'"
        if end_date:
            query += f" AND e.end_date <= '{end_date}'"
        if club_id:
            query += f" AND e.club_id = {club_id}"

        self.env.cr.execute(query)
        events = self.env.cr.dictfetchall()

        return {
            'doc_ids': docids,
            'doc_model': 'event.report.wizard',
            'events': events,
        }
