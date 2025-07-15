# -*- coding: utf-8 -*-
import xmlrpc.client
from odoo import models, fields
from odoo.exceptions import UserError
from odoo.tools import config
import logging

_logger = logging.getLogger(__name__)

class FetchProductWizard(models.TransientModel):
    """Handles the wizard and XML-RPC"""
    _name = 'fetch.product.wizard'
    _description = 'Fetch All Products from Odoo 17'

    odoo18_db = fields.Char(string="Odoo 18 DB", readonly=True, default=lambda self: self.env.cr.dbname)
    odoo18_user = fields.Char(string="Odoo 18 User", readonly=True, default=lambda self: config["db_user"])
    odoo17_url = fields.Char(string="Odoo 17 URL", required=True, default="http://localhost:8017")
    odoo17_db = fields.Char(string="Database Name", required=True)
    odoo17_username = fields.Char(string="Username", required=True)
    odoo17_password = fields.Char(string="Password", required=True)

    def get_existing_default_codes(self):
        """Finds the existing products in Odoo18 based on internal reference"""
        products = self.env['product.product'].search_read([('default_code', '!=', False)],['default_code'])
        return [p['default_code'] for p in products]

    def action_fetch_all_products(self):
        """Handles the XML-RPC and creation of fetched products"""
        self.ensure_one()
        try:
            common = xmlrpc.client.ServerProxy(f"{self.odoo17_url}/xmlrpc/2/common")
            uid = common.authenticate(self.odoo17_db, self.odoo17_username, self.odoo17_password, {})
            models = xmlrpc.client.ServerProxy(f"{self.odoo17_url}/xmlrpc/2/object")
        except:
            raise UserError("Invalid details provided")

        existing_codes = self.get_existing_default_codes()
        domain = [('default_code', '!=', False)]
        if existing_codes:
            domain.append(('default_code', 'not in', existing_codes))

        fetched_products = models.execute_kw(
                self.odoo17_db, uid, self.odoo17_password,
                'product.product', 'search_read',
                [domain],
                {'fields': ['name', 'default_code', 'list_price', 'standard_price', 'type',
                            'uom_id', 'categ_id', 'barcode', 'active']}
            )
        existing_products = self.env['product.product'].search_read([('default_code', 'in', existing_codes)],['name','default_code'])
        print(existing_products)
        existing_count = len(existing_products)
        print(existing_count)
        existing_products_info = [f"{p['name']} ({p['default_code']})" for p in existing_products]

        created_count=0
        for prod in fetched_products:
            self.env['product.product'].create({
                'name': prod['name'],
                'default_code': prod['default_code'],
                'list_price': prod['list_price'],
                'standard_price': prod['standard_price'],
                'type': prod['type'],
                'barcode': prod['barcode'],
                'active': prod['active'],
                'uom_id': prod['uom_id'][0] if prod['uom_id'] else False,
                'categ_id': prod['categ_id'][0] if prod['categ_id'] else False,
            })
            created_count+=1

        return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': f"{created_count} product(s) imported. {existing_count} product(s) already exists",
                    'type': 'success',
                    'sticky': False,
                },
                'effect': {
                    'fadeout': 'slow',
                    'message': f"{created_count} Product(s) Fetched. {existing_count} product(s) already exists {existing_products_info}",
                    'type': 'rainbow_man'
                },
        }
