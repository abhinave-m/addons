# -*- coding: utf-8 -*-
from odoo import fields,models


class SaleOrder(models.Model):
    """Inherits the Sale Order Model and adds new state"""
    _inherit = "sale.order"

    state = fields.Selection(selection_add=[('admitted','Admitted')])


