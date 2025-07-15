#-*- coding: utf-8 -*-
from odoo import fields, models


class ManageSubject(models.Model):
    """Subject model fields declaration"""
    _name = "manage.subject"
    _description = "Manage Subject"
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    department_id = fields.Many2one('manage.department','Department')
