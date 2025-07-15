# -*- coding: utf-8 -*-
from odoo import fields, models


class AutomatedSOWizard(models.TransientModel):
    """Declares fields and actions for the wizard"""
    _name = 'automated.so.wizard'
    _description = 'Wizard for Creating Quotation and SO'

    product_id = fields.Many2one('product.product', string="Product", readonly=True)
    customer_id = fields.Many2one('res.partner', string="Customer", required=True)
    quantity = fields.Float(string="Quantity", required=True, default=1.0)
    price = fields.Float(string="Price", required=True)

    def confirm_so(self):
        """Contains the logic for creation of New Sale order or to add to existing Sale order when the confirm button is clicked"""
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']

        order = SaleOrder.search([
            ('partner_id', '=', self.customer_id.id),
            ('state', '=', 'draft')
        ])

        if not order:
            order = SaleOrder.create({'partner_id': self.customer_id.id})

        matched_line = False
        for line in order.order_line:
            if line.product_id == self.product_id and line.price_unit == self.price:
                line.product_uom_qty += self.quantity
                matched_line = True
                break

        if not matched_line:
            SaleOrderLine.create({
                'order_id': order.id,
                'product_id': self.product_id.id,
                'product_uom_qty': self.quantity,
                'price_unit': self.price,
                'name': self.product_id.name,
            })

        order.action_confirm()
        return {'type': 'ir.actions.act_window_close'}
