# -*- coding: utf-8 -*-
import json
from odoo import fields, http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale


class WebsiteSaleDecimal(WebsiteSale):
    """Extends WebsiteSale to support decimal quantities in the cart."""
    @http.route()
    def shop(self, page=0, category=None, search='', **post):
        response = super().shop(page=page, category=category, search=search, **post)
        order = request.website.sale_get_order()
        if order:
            qty = sum(order.mapped('website_order_line.product_uom_qty'))
            request.session['website_sale_cart_quantity'] = round(qty, 1)
        return response

    @http.route()
    def cart(self, **post):
        """Renders the cart page with decimal quantity support and cleans inactive lines."""
        order = request.website.sale_get_order()
        if order and order.carrier_id:
            order._remove_delivery_line()

        if order and order.state != 'draft':
            request.session['sale_order_id'] = None
            order = request.website.sale_get_order()

        if order:
            qty = sum(order.mapped('website_order_line.product_uom_qty'))
            request.session['website_sale_cart_quantity'] = round(qty, 1)

        values = {
            'website_sale_order': order,
            'date': fields.Date.today(),
            'suggested_products': [],
        }

        if order:
            order.order_line.filtered(lambda l: not l.product_id.active).unlink()
            values['suggested_products'] = order._cart_accessories()
            values.update(self._get_express_shop_payment_values(order))

        values.update(self._cart_values(**post))
        return request.render("website_sale.cart", values)

    @http.route()
    def cart_update_json(self, product_id, line_id=None, add_qty=None, set_qty=None,product_custom_attribute_values=None,no_variant_attribute_values=None, **kw):
        """Updates the cart (add/set quantity) via JSON route with decimal support."""
        order = request.website.sale_get_order(force_create=True)

        if order.state != 'draft':
            request.website.sale_reset()
            if kw.get('force_create'):
                order = request.website.sale_get_order(force_create=True)
            else:
                return {}

        if product_custom_attribute_values:
            product_custom_attribute_values = json.loads(product_custom_attribute_values)
        if no_variant_attribute_values:
            no_variant_attribute_values = json.loads(no_variant_attribute_values)

        values = order._cart_update(
            product_id=product_id,
            line_id=line_id,
            add_qty=add_qty,
            set_qty=set_qty,
            product_custom_attribute_values=product_custom_attribute_values,
            no_variant_attribute_values=no_variant_attribute_values,
            **kw
        )

        line_ids = [values['line_id']]
        values['notification_info'] = self._get_cart_notification_information(order, line_ids)

        qty = sum(order.mapped('website_order_line.product_uom_qty'))
        request.session['website_sale_cart_quantity'] = round(qty, 1)

        if not order.cart_quantity:
            request.website.sale_reset()
            return values

        values.update({
            'cart_quantity': round(qty, 1),
            'amount': order.amount_total,
            'cart_ready': order._is_cart_ready(),
            'website_sale.cart_lines': request.env['ir.ui.view']._render_template(
                "website_sale.cart_lines", {
                    'website_sale_order': order,
                    'date': fields.Date.today(),
                    'suggested_products': order._cart_accessories()
                }),
            'website_sale.total': request.env['ir.ui.view']._render_template(
                "website_sale.total", {
                    'website_sale_order': order,
                }),
        })
        return values
    

