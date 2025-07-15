# -*- coding: utf-8 -*-
import json
from odoo import http
from odoo.http import request


class WebsiteSale(http.Controller):
    """Handles the clear cart action from button->JS"""
    @http.route(['/shop/clear_cart'], type='http', auth="public", csrf=False, website=True)
    def clear_cart(self, **kw):
        """Clears the cart"""
        order = request.website.sale_get_order()
        if order:
            order.website_order_line.unlink()
        return request.make_response(json.dumps({'success': True}), headers=[('Content-Type', 'application/json')])

