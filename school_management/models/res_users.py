#-*- coding: utf-8 -*-
from odoo import fields,models


class ResUsers(models.Model):
    """Create a field registration_id to link the Registration model to other sub models for rule creation"""
    _inherit = 'res.users'

    registration_id = fields.Many2one('registration',"Student Registration")