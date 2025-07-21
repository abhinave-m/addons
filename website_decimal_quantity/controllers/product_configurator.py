import json
from odoo import http
from odoo.http import request,route
from odoo.addons.website_sale.controllers.product_configurator import WebsiteSaleProductConfiguratorController

class WebsiteSaleDecimal(WebsiteSaleProductConfiguratorController):
    """Extends the ProductConfigurator controller to handle decimal quantities"""

    @route()
    def website_sale_product_configurator_update_cart(
            self, main_product, optional_products, **kwargs):
        """Handles float quantity and optional products from the configurator modal."""
        order = request.website.sale_get_order(force_create=True)
        if order.state != 'draft':
            request.website.sale_reset()
            order = request.website.sale_get_order(force_create=True)

        main_product_qty = float(main_product.get('quantity', 1.0))
        main_product_id = int(main_product['product_id'])

        main_line = order._cart_update(
            product_id=main_product_id,
            add_qty=main_product_qty,
            **kwargs
        )
        parent_line_id = main_line.get('line_id')

        optional_product_lines = []
        response_lines = []

        for option in optional_products:
            option_qty = float(option.get('quantity', 0.0))
            if not option_qty:
                continue

            product_id = option['product_id']
            product = request.env['product.product'].browse(product_id)

            option_values = order._cart_update(
                product_id=product_id,
                add_qty=option_qty,
                linked_line_id=parent_line_id,
                **kwargs
            )

            optional_product_lines.append(option_values.get('line_id'))

            response_lines.append({
                'product_id': product.id,
                'quantity': option_qty,
                'display_name': product.display_name,
                'product_template_id': product.product_tmpl_id.id,
                'is_optional': True,
            })

        qty = sum(order.mapped('website_order_line.product_uom_qty'))
        request.session['website_sale_cart_quantity'] = round(qty, 1)

        line_ids = [parent_line_id] if parent_line_id else []
        notification_info = self._get_cart_notification_information(order, line_ids)

        return {
            'main_line_id': parent_line_id,
            'optional_product_line_ids': optional_product_lines,
            'cart_quantity': round(qty, 1),
            'notification_info': notification_info,
            'lines': response_lines or [],
        }
