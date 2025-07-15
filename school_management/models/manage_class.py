#-*- coding: utf-8 -*-
from odoo import fields, models


class ManageClass(models.Model):
    """Class model fields declaration"""
    _name = "manage.class"
    _description = "Manage Class"
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    department_id = fields.Many2one('manage.department','Department')
    hod_id = fields.Many2one('res.partner', string='HOD', related='department_id.head_of_the_department_id', store=True, readonly=True)


