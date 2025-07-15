# -*- coding: utf-8 -*-
from odoo import models, api


class StockValuationLayer(models.Model):
    """Handles the data related to average expense and valuation of products"""
    _inherit = 'stock.valuation.layer'

    @api.model
    def get_avg_expense(self):
        """Returns the average expense of products"""
        valuation = self.env['stock.valuation.layer'].read_group(
            [('product_id', '!=', False)],
            ['product_id', 'value:sum', 'quantity:sum'],
            ['product_id']
        )
        result = []
        for line in valuation:
            total_value = line.get('value', 0.0)
            total_qty = line.get('quantity', 0.0)
            avg_expense = total_value / total_qty if total_qty else 0.0
            product_name = line['product_id'][1] if isinstance(line['product_id'], tuple) else ''
            result.append({
                'product': product_name,
                'avg_expense': avg_expense,
            })
        return result

    @api.model
    def get_inventory_valuation(self):
        """Returns the valuation of products"""
        groups = self.read_group(
            [('value', '>', 0)],
            ['product_id', 'value:sum'],
            ['product_id']
        )
        results = []
        for group in groups:
            product = self.env['product.product'].browse(group['product_id'][0])
            total_value = group['value']
            results.append({
                'product_name': product.display_name,
                'total_value': total_value
            })
        return results
