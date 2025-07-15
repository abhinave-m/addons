# -*- coding: utf-8 -*-
from odoo import fields, models, api
from datetime import timedelta


class StockMove(models.Model):
    """Handles the records related to incoming,outgoing,internal and picking type moves"""
    _inherit = 'stock.move'

    @api.model
    def get_incoming_stock(self):
        """Returns the incoming stock moves """
        filter_value = self.env.context.get("filter")
        domain = [
            ('picking_id.picking_type_id.code', '=', 'incoming'),
            ('state', '=', 'done')
        ]
        if filter_value == 'yearly':
            first_month = fields.Date.today().replace(day=1,month=1)
            domain.append(('date', '>=', first_month))
        elif filter_value == 'monthly':
            first_day = fields.Date.today().replace(day=1)
            domain.append(('date', '>=', first_day))
        elif filter_value == 'weekly':
            today = fields.Date.today()
            start_week = today - timedelta(days=today.weekday())
            domain.append(('date', '>=', start_week))

        if not self.env.user.has_group('stock.group_stock_manager'):
            domain.append(('picking_id.user_id', '=', self.env.user.id))
        moves = self.env['stock.move'].read_group(
            domain=domain,
            fields=['product_uom_qty:sum'],
            groupby=['product_id']
        )
        data = []
        for rec in moves:
            product_name = ''
            if rec.get('product_id'):
                product_name = self.env['product.product'].browse(rec['product_id'][0]).name
            data.append({
                'product_id': rec['product_id'],
                'product_name': product_name,
                'product_uom_qty': rec.get('product_uom_qty', 0),
            })
        return data

    @api.model
    def get_outgoing_stock(self):
        """Returns the outgoing stock moves """
        filter_value = self.env.context.get("filter")
        domain = [
            ('picking_id.picking_type_id.code', '=', 'outgoing'),
            ('state', '=', 'done')
        ]
        if filter_value == 'yearly':
            first_month = fields.Date.today().replace(day=1,month=1)
            domain.append(('date', '>=', first_month))
        elif filter_value == 'monthly':
            first_day = fields.Date.today().replace(day=1)
            domain.append(('date', '>=', first_day))
        elif filter_value == 'weekly':
            today = fields.Date.today()
            start_week = today - timedelta(days=today.weekday())
            domain.append(('date', '>=', start_week))

        if not self.env.user.has_group('stock.group_stock_manager'):
            domain.append(('picking_id.user_id', '=', self.env.user.id))
        moves = self.env['stock.move'].read_group(
            domain=domain,
            fields=['product_uom_qty:sum'],
            groupby=['product_id']
        )
        data = []
        for rec in moves:
            product_name = ''
            if rec.get('product_id'):
                product_name = self.env['product.product'].browse(rec['product_id'][0]).name
            data.append({
                'product_id': rec['product_id'],
                'product_name': product_name,
                'product_uom_qty': rec.get('product_uom_qty', 0),
            })
        return data

    @api.model
    def get_internal_stock_move(self):
        """Returns the internal stock moves """
        filter_value = self.env.context.get("filter")
        domain = [
            ('picking_id.picking_type_id.code', '=', 'internal'),
            ('state', '=', 'done')
        ]
        if filter_value == 'yearly':
            first_month = fields.Date.today().replace(day=1,month=1)
            domain.append(('date', '>=', first_month))
        elif filter_value == 'monthly':
            first_day = fields.Date.today().replace(day=1)
            domain.append(('date', '>=', first_day))
        elif filter_value == 'weekly':
            today = fields.Date.today()
            start_week = today - timedelta(days=today.weekday())
            domain.append(('date', '>=', start_week))

        if not self.env.user.has_group('stock.group_stock_manager'):
            domain.append(('picking_id.user_id', '=', self.env.user.id))
        moves = self.env['stock.move'].read_group(
            domain=domain,
            fields=['product_uom_qty:sum'],
            groupby=['product_id']
        )
        data = []
        for rec in moves:
            product_name = ''
            if rec.get('product_id'):
                product_name = self.env['product.product'].browse(rec['product_id'][0]).name
            data.append({
                'product_id': rec['product_id'],
                'product_name': product_name,
                'product_uom_qty': rec.get('product_uom_qty', 0),
            })
        return data

    @api.model
    def get_group_based_on_picking_type(self):
        """Returns the moves based on picking type """
        moves = self.env['stock.move'].read_group(
            domain=[('state', '=', 'done')],
            fields=['product_uom_qty:sum'],
            groupby=['picking_type_id']
        )
        data = []
        for rec in moves:
            if rec.get('picking_type_id'):
                picking_type_name = rec['picking_type_id'][1]
            else:
                continue
            data.append({
                'picking_type': picking_type_name,
                'total_quantity': rec.get('product_uom_qty', 0),
            })
        return data



