# -*- coding: utf-8 -*-
from odoo import fields,models


class ProductGrade(models.Model):
    """Inherits the product.product model to add product_grade field"""
    _inherit = 'product.product'

    product_grade = fields.Char("Product Grade")