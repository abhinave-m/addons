# -*- coding: utf-8 -*-
from odoo import api, models, fields


class ResPartner(models.Model):
    """Inherits res.partner and adds a field to store parent customer"""
    _inherit = 'res.partner'

    customer_parent_id = fields.Many2one('res.partner',string="Parent Customer", domain="[('id', 'not in', customer_hierarchy_ids)]")
    customer_child_ids = fields.One2many('res.partner', 'customer_parent_id', string="Child Customers")
    # is_in_hierarchy = fields.Boolean(compute='_compute_is_in_hierarchy', store=True)
    # has_customer_children = fields.Boolean(compute="_compute_has_customer_children")
    customer_hierarchy_ids = fields.Many2many('res.partner',string="Related Customers",compute='_compute_customer_hierarchy_ids',store=False)

    @api.depends('customer_parent_id', 'customer_child_ids')
    def _compute_customer_hierarchy_ids(self):
        """Checks whether the record has a child in hierarchy to remove it from the available parents"""
        for partner in self:
            related = partner._get_all_children() | partner
            partner.customer_hierarchy_ids = related

    # @api.depends('customer_child_ids')
    # def _compute_has_customer_children(self):
    #     """Checks if the record has a children or not for making the parent field invisible"""
    #     for rec in self:
    #         rec.has_customer_children = bool(rec.customer_child_ids)

    # @api.depends('customer_parent_id', 'customer_child_ids')
    # def _compute_is_in_hierarchy(self):
    #     """Checks whether the record is a parent or child to remove it from the available parents"""
    #     for partner in self:
    #         partner.is_in_hierarchy = bool(partner.customer_parent_id or partner.customer_child_ids)

    def get_customer_org_chart_data(self):
        """Return JSON-like org chart data for this partner if part of hierarchy."""
        has_parent = bool(self.customer_parent_id)
        has_children = bool(self.customer_child_ids)
        if not (has_parent or has_children):
            return None
        top = self
        while top.customer_parent_id:
            top = top.customer_parent_id
        data = top._get_customer_node()
        return {"root": data}


    def _get_customer_node(self):
        """Build and return a node dict with id, name, function, image, and children."""
        return {
            "id": self.id,
            "display_name": self.display_name,
            "image_128": self.image_128.decode() if self.image_128 else "",
            "function" : self.function,
            "children": [c._get_customer_node() for c in self.customer_child_ids],
        }

    # def _get_all_parents(self):
    #     """Returns a recordset of all parents up to the top ancestor."""
    #     parents = self.env['res.partner']
    #     current = self.customer_parent_id
    #     while current:
    #         parents |= current
    #         current = current.customer_parent_id
    #     return parents

    def _get_all_children(self):
        """Returns a recordset of all descendants (children, grandchildren, etc)."""
        all_children = self.env['res.partner']
        to_process = self.customer_child_ids
        while to_process:
            all_children |= to_process
            to_process = to_process.mapped('customer_child_ids')
        return all_children


