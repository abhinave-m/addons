from odoo import fields,models

class Grade(models.Model):
    _name = "grade"
    _description = "Grade"

    name = fields.Char(required=True)
    teacher_assigned_id = fields.Many2one("teacher",string="Teacher Assigned")