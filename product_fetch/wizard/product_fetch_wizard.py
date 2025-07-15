#-*- coding: utf-8 -*-
import requests
from odoo import models, fields
from odoo.exceptions import UserError
from odoo.tools import config
import logging
_logger = logging.getLogger(__name__)


class ProductFetchWizard(models.TransientModel):
    """Handles the wizard and POST to the controller"""
    _name = 'product.fetch.wizard'
    _description = 'Fetch All Products from Odoo 17'

    odoo18_db = fields.Char(string="Odoo 18 DB", readonly=True, default=lambda self: self.env.cr.dbname,)
    odoo18_user = fields.Char(string="Odoo 18 User", readonly=True, default=lambda self: config["db_user"])

    odoo17_url = fields.Char(string="Odoo 17 URL", required=True, default="http://localhost:8017")
    odoo17_db = fields.Char(string="Database Name", required=True)
    odoo17_username = fields.Char(string="Odoo 17 Username", required=True)
    api_key = fields.Char(string="API", required=True)

    def get_existing_default_codes(self):
        """Takes all the existing default_codes(Internal Reference)"""
        products = self.env['product.product'].search_read([('default_code', '!=', False)],['default_code'])
        return [p['default_code'] for p in products]

    def action_fetch_all_products(self):
        """Performs the fetching of products from Odoo17 by posting the controller"""
        self.ensure_one()
        existing_codes = self.get_existing_default_codes()
        url = self.odoo17_url.rstrip('/') + "/product_transfer/fetch"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }
        _logger.warning("Existing default codes sent: %s", existing_codes)
        payload = {
            "params": {
                "existing_default_codes": existing_codes
            }
        }

        try:
            response = requests.post(url, json=payload, headers=headers)
            data = response.json()
            _logger.info("Odoo 17 API response: %s", data)
        except Exception as e:
            raise UserError(f"Failed to fetch products from Odoo 17. Reason: {e}")

        result = data.get('result', {})
        count = result.get('count')
        print(result)
        if count==0:
            raise UserError("No products to fetch")
        if not result.get('success') or not result:
            error_msg = result.get('error', 'Unknown error from Odoo 17')
            raise UserError("Odoo 17 API Error: %s" % error_msg)

        _logger.warning("Fetched products: %s", result.get('products'))

        for product in result.get('products', []):
            self.env['product.product'].create({
                'name': product['name'],
                'default_code': product['default_code'],
                'list_price': product['list_price'],
                'standard_price': product['standard_price'],
                'type': product['type'],
                'uom_id': self.env['uom.uom'].search([('name', '=', product['uom_id'])], limit=1).id,
                'categ_id': self.env['product.category'].search([('name', '=', product['categ_id'])], limit=1).id,
                'barcode': product['barcode'],
                'active': product['active'],
            })

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': "Product Transfer Complete",
                'message': "Products imported successfully from Odoo 17.",
                'type': 'success',
                'sticky': False,
            }
        }
