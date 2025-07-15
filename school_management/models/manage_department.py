#-*- coding: utf-8 -*-
from odoo import fields, models


class ManageDepartment(models.Model):
    """Department model fields declaration"""
    _name = "manage.department"
    _description = "Manage Department"
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    head_of_the_department_id = fields.Many2one('res.partner','HOD')

