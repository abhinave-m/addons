# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ClubsReportWizard(models.TransientModel):
    """Clubs Report Wizard field declaration"""
    _name = 'clubs.report.wizard'
    _description = 'Clubs Report Filter Wizard'

    student_id = fields.Many2one("registration","Student")
    club_id = fields.Many2one("clubs","Club")
    possible_student_ids = fields.Many2many('registration', compute='_compute_possible_student_ids',string="Possible Student")

    @api.depends('club_id')
    def _compute_possible_student_ids(self):
        """Filters students based on the selected club"""
        for rec in self:
            if rec.club_id:
                rec.possible_student_ids = self.env['registration'].search([
                    ('club_ids', '=', rec.club_id.id)
                ])
            else:
                rec.possible_student_ids = self.env['registration'].search([])

    def action_generate_pdf_report(self):
        """Trigger the report using SQL logic in the Abstract model"""
        data = {
            'club_id': self.club_id.id if self.club_id else False,
            'student_id': self.student_id.id if self.student_id else False,
        }

        return self.env.ref('school_management.action_clubs_report_pdf').report_action(self, data=data)

