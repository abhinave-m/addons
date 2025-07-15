# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class CustomerOrgChartController(http.Controller):
    """Handles the RPC call from the customer_org_chart.js and returns the tree created"""
    @http.route('/customer/get_org_chart', type='json', auth='user')
    def get_customer_org_chart(self, partner_id):
        partner = request.env['res.partner'].browse(partner_id).exists()
        return partner.get_customer_org_chart_data() if partner else {}
