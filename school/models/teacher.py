from odoo import fields,models

class Teacher(models.Model):
    _name = "teacher"
    _description = "Teacher"

    name = fields.Char(required=True)
    age = fields.Integer()
    city = fields.Char()
    grade_id = fields.One2many("grade", "teacher_assigned_id", string="Assigned grade")

