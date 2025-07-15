# -*- coding: utf-8 -*-
from odoo import models


class AutomatedProduct(models.Model):
    """Inherits the product.product model"""
    _inherit = 'product.product'

    def add_to_quotation(self):
        """Returns a Wizard when Add to Quotation button is clicked"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Create Quotation',
            'res_model': 'automated.so.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_product_id': self.id,
                'default_price': self.lst_price
            },
        }

