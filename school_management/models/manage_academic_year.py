#-*- coding: utf-8 -*-
from odoo import fields, models


class ManageAcademicYear(models.Model):
    """Academic Year model fields declaration"""
    _name = "manage.academic.year"
    _description = "Manage Academic Year"

    name = fields.Char(required=True)

