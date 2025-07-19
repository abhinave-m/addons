# -*- coding: utf-8 -*-
import ast
from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    hr_hiring_reviewer_ids = fields.Many2many(comodel_name='res.users',
                                              related='company_id.hr_hiring_reviewer_ids', readonly=False)

    @api.model
    def get_values(self):
        res = super().get_values()
        config = self.env['ir.config_parameter'].sudo()
        user_ids_str = config.get_param('hr_hub.hr_hiring_reviewer_ids', '[]')

        try:
            user_ids = ast.literal_eval(user_ids_str) if user_ids_str else []
        except (ValueError, SyntaxError):
            user_ids = []

        res.update({
            'hr_hiring_reviewer_ids': [(6, 0, user_ids)],
        })
        return res

    def set_values(self):
        super().set_values()
        config = self.env['ir.config_parameter'].sudo()
        user_ids = self.hr_hiring_reviewer_ids.ids
        config.set_param('hr_hub.hr_hiring_reviewer_ids', str(user_ids))