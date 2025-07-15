from odoo import fields,models

class Subject(models.Model):
    _name = "subject"
    _description = "Subject"

    name = fields.Char(required=True)


