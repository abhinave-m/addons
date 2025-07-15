# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import date, timedelta


class EventReportWizard(models.TransientModel):
    """Event Report Wizard field declaration"""
    _name = 'event.report.wizard'
    _description = 'Event Report Filter Wizard'

    date_filter = fields.Selection([
        ('today', 'Today'),
        ('this_week', 'This Week'),
        ('this_month', 'This Month'),
        ('custom', 'Custom Range')
    ], string="Date Filter", default='this_month')

    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    club_id = fields.Many2one("clubs","Club Name")

    @api.onchange('date_filter')
    def _onchange_date_filter(self):
        """Auto-fill start/end date based on selected range."""
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

    def action_generate_pdf_report(self):
        """Trigger the report using SQL logic in the Abstract model"""
        data = {
            'start_date': self.start_date,
            'end_date': self.end_date,
            'club_id': self.club_id.id if self.club_id else False,
        }
        return self.env.ref('school_management.action_event_report_pdf').report_action(self, data=data)

