# -*- coding: utf-8 -*-
from odoo import models, api


class StockLocation(models.Model):
    """Handles the data of locations specific to warehouses"""
    _inherit = 'stock.location'

    @api.model
    def get_warehouse_locations(self):
        """Returns the locations related to each warehouse"""
        locations = self.search([('usage', '=', 'internal')])
        data = []
        for loc in locations:
            warehouse_name = loc.warehouse_id.name or 'No Warehouse'
            data.append({
                'warehouse': warehouse_name,
                'location': loc.complete_name,
            })
        return data


