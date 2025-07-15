from odoo import fields,models

class Student(models.Model):
    _name = "student"
    _description = "Student"

    name = fields.Char(required=True)
    age = fields.Integer()
    city = fields.Char()
    date_of_birth = fields.Date()
    grade_id = fields.Many2one("grade",string="Grade")
    subject_id = fields.Many2many("subject",string="Subject")
    teacher_assigned = fields.Many2one("teacher",related="grade_id.teacher_assigned_id",store=True)