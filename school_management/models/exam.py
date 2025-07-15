#-*- coding: utf-8 -*-
from odoo import fields, models, Command


class Exam(models.Model):
    """Exam fields declaration"""
    _name = "exam"
    _description = "Exam"
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    class_id = fields.Many2one('manage.class','Class')
    paper_ids = fields.One2many('exam.papers','exam_id','Papers')
    status = fields.Selection([('new','New'),('ongoing','Ongoing'),('completed','Completed')], default='new')

    def add_exam(self):
        """Adds exam to the students of corresponding class"""
        for exam in self:
            registrations = self.env['registration'].search([('current_class_id', '=', exam.class_id.id)])
            for reg in registrations:
                reg.exam_ids = [(Command.link(exam.id))]