# -*- coding: utf-8 -*-
from odoo import models


class ProductProduct(models.Model):
    """Inherit product.product to include custom fields in POS"""
    _inherit = 'product.product'

    def _load_pos_data_fields(self, config_id):
        """To load the field product_grade to POS"""
        result = super()._load_pos_data_fields(config_id)
        result.append('product_grade')
        return result

    def _pos_ui_product_fields(self):
        """ Adds 'product_grade' to the list of product fields sent to the frontend"""
        return super()._pos_ui_product_fields() + ['product_grade']