# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError
from odoo.http import request


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.depends('order_line.product_uom_qty', 'order_line.product_id')
    def _compute_cart_info(self):
        for order in self:
            order.cart_quantity = sum(order.mapped('website_order_line.product_uom_qty'))
            order.only_services = all(line.product_id.type == 'service' for line in order.website_order_line)

    def _cart_update(self, product_id, line_id=None, add_qty=0, set_qty=0, **kwargs):
        self.ensure_one()

        if self.state != 'draft':
            request.session.pop('sale_order_id', None)
            request.session.pop('website_sale_cart_quantity', None)
            raise UserError(_('It is forbidden to modify a sales order which is not in draft status.'))

        product = self.env['product.product'].browse(product_id).exists()
        if not product or not product._is_add_to_cart_allowed():
            raise UserError(_("The given product does not exist therefore it cannot be added to cart."))

        if product.lst_price == 0 and product.website_id.prevent_zero_price_sale:
            raise UserError(_("The given product does not have a price therefore it cannot be added to cart."))

        order_line = self._cart_find_product_line(product_id, line_id, **kwargs)[:1] if line_id is not False else self.env['sale.order.line']

        quantity = float(set_qty) if set_qty else (
            int(order_line.product_uom_qty) + int(add_qty or 0) if order_line else float(add_qty or 0)
        )

        warning = ''
        if float(quantity) > 0:
            quantity, warning = self._verify_updated_quantity(order_line, product_id, float(quantity), **kwargs)
        if order_line and int(quantity) <= 0:
            order_line.unlink()
            order_line = self.env['sale.order.line']
        elif order_line:
            update_values = self._prepare_order_line_update_values(order_line, quantity, **kwargs)
            if update_values:
                self._update_cart_line_values(order_line, update_values)
        elif int(quantity) > 0:
            order_line_values = self._prepare_order_line_values(product_id, quantity, **kwargs)
            order_line = self.env['sale.order.line'].sudo().create(order_line_values)

        return {
            'line_id': order_line.id,
            'quantity': quantity,
            'option_ids': list(set(order_line.linked_line_ids.filtered(
                lambda sol: sol.order_id == order_line.order_id).ids)),
            'warning': warning,
        }
