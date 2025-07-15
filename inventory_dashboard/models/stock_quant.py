# -*- coding: utf-8 -*-
from odoo import models, api


class StockQuant(models.Model):
    """Returns the Location specific stock quantities data"""
    _inherit = 'stock.quant'

    @api.model
    def get_location_stock(self):
        """Returns the stock quantities at their respective locations"""
        quants = self.env['stock.quant'].read_group(
            domain=[],
            fields=['quantity:sum'],
            groupby=['location_id']
        )
        data = []
        for q in quants:
            loc_name = 'Unknown'
            if q.get('location_id'):
                loc_name = self.env['stock.location'].browse(q['location_id'][0]).display_name
            data.append({
                'location_name': loc_name,
                'quantity': q.get('quantity', 0),
            })
        return data

