#-*- coding: utf-8 -*-
from odoo import fields, models


class ExamPapers(models.Model):
    """Exam paper fields declaration"""
    _name = "exam.papers"
    _description = "Exam Papers"

    exam_id = fields.Many2one('exam',"Exam")
    subject_id = fields.Many2one('manage.subject','Subject')
    max_mark = fields.Integer(string="Maximum Marks")
    pass_mark = fields.Integer(string="Pass Mark")