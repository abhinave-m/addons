# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ExamReportWizard(models.TransientModel):
    """Exam Report Wizard field declaration"""
    _name = 'exam.report.wizard'
    _description = 'Exam Report Filter Wizard'

    student_id = fields.Many2one("registration","Student")
    class_id = fields.Many2one("manage.class","Class")
    exam_id = fields.Many2one('exam','Exam')
    possible_student_ids = fields.Many2many('registration', compute='_compute_possible_student_ids',string="Possible Student")
    possible_exam_ids = fields.Many2many('exam', compute='_compute_possible_exam_ids',string="Possible Exam")

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

    @api.depends('class_id')
    def _compute_possible_exam_ids(self):
        """Filters exam based on the selected class"""
        for rec in self:
            if rec.class_id:
                rec.possible_exam_ids = self.env['exam'].search([
                    ('class_id', '=', rec.class_id.id)
                ])
            else:
                rec.possible_exam_ids = self.env['exam'].search([])

    def action_generate_pdf_report(self):
        """Trigger the report using SQL logic in the Abstract model"""
        data = {
            'class_id': self.class_id.id if self.class_id else False,
            'student_id': self.student_id.id if self.student_id else False,
            'exam_id' : self.exam_id.id if self.exam_id else False
        }
        return self.env.ref('school_management.action_exam_report_pdf').report_action(self, data=data)

