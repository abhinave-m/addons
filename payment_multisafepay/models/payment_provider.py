# -*- coding: utf-8 -*-
import requests
from odoo import models, fields
from odoo.http import request


class PaymentProvider(models.Model):
    """Extends payment provider to support MultiSafepay integration."""
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('multisafepay', "MultiSafepay")],
        ondelete={'multisafepay': 'set default'}
    )
    multisafepay_api_key = fields.Char("MultiSafepay API Key")
    multisafepay_test_mode = fields.Boolean("Use Test Mode", default=True)

    def multisafepay_create_order(self, tx):
        """Creates a payment order on MultiSafepay and returns redirect URL."""
        self.ensure_one()
        api_key = self.multisafepay_api_key
        if not api_key:
            raise ValueError("MultiSafepay API Key is missing!")
        base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')

        payload = {
            "type": "redirect",
            "order_id": tx.reference,
            "currency": tx.currency_id.name,
            "amount": int(tx.amount * 100),
            "description": f"Order {tx.reference}",
            "customer": {
            "locale": "en_US",
            },
            "payment_options": {
                "redirect_url": f"{base_url}/payment/multisafepay/return",
                "cancel_url": f"{base_url}/payment/multisafepay/cancel"
            }
        }

        headers = {
            'api_key': api_key,
            'Content-Type': 'application/json'
        }
        resp = requests.post(
            "https://testapi.multisafepay.com/v1/json/orders",
            headers=headers,
            json=payload
        )

        result = resp.json().get('data') or {}
        return result.get('payment_url')
