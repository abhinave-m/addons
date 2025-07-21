# -*- coding: utf-8 -*-
from odoo import api, models


class SaleOrder(models.Model):
    """Inherits sale.order to customize cart quantity handling and allow decimal quantity support."""
    _inherit = 'sale.order'

    @api.depends('order_line.product_uom_qty', 'order_line.product_id')
    def _compute_cart_info(self):
        """Compute the total quantity in the cart and determine if all products are services."""
        for order in self:
            order.cart_quantity = sum(order.mapped('website_order_line.product_uom_qty'))
            order.only_services = all(line.product_id.type == 'service' for line in order.website_order_line)

    def _cart_update(self, product_id, line_id=None, add_qty=0, set_qty=0, **kwargs):
        """Updates the cart: add, set, or remove product quantity (supports decimals)."""
        self.ensure_one()

        order_line = self.env['sale.order.line']
        if line_id is not False:
            order_line = self._cart_find_product_line(product_id, line_id, **kwargs)[:1]

        quantity = 0
        if set_qty:
            quantity = set_qty
        elif add_qty is not None:
            if order_line:
                quantity = float(order_line.product_uom_qty) + float(add_qty or 0)
            else:
                quantity = add_qty or 0

        if float(quantity) > 0:
            quantity, warning = self._verify_updated_quantity(order_line, product_id, float(quantity), **kwargs)
        else:
            warning = ''

        if order_line and int(quantity) <= 0:
            order_line.unlink()
            order_line = self.env['sale.order.line']
        elif order_line:
            update_values = self._prepare_order_line_update_values(order_line, quantity, **kwargs)
            if update_values:
                self._update_cart_line_values(order_line, update_values)
        elif int(quantity) >= 0:
            order_line_values = self._prepare_order_line_values(product_id, quantity, **kwargs)
            order_line = self.env['sale.order.line'].sudo().create(order_line_values)

        return {
            'line_id': order_line.id,
            'quantity': quantity,
            'option_ids': list(
                set(order_line.linked_line_ids.filtered(lambda sol: sol.order_id == order_line.order_id).ids)),
            'warning': warning,
        }
