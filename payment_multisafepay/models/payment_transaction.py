# -*- coding: utf-8 -*-
from odoo import models


class PaymentTransaction(models.Model):
    """Inherits payment.transaction model to inject redirect URL"""
    _inherit = 'payment.transaction'

    def _get_specific_rendering_values(self, processing_values):
        """Inject redirect URL for MultiSafepay payment"""
        if self.provider_code == 'multisafepay':
            redirect_url = f"/payment/multisafepay/redirect/{self.id}"
            return {'api_url': redirect_url}
        return super()._get_specific_rendering_values(processing_values)

