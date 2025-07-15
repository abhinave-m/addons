#-*- coding: utf-8 -*-
from odoo import api, fields, models, Command
from odoo.exceptions import UserError


class ResPartner(models.Model):
    """Extends the fields of res.partner"""
    _name = "res.partner"
    _inherit = "res.partner"

    partner_type = fields.Selection([('teacher','Teacher'),('staff','Office Staff'),('student','Student')])
    partner_id = fields.Many2one('res.partner','Partner')
    is_partner = fields.Boolean()
    # user_id = fields.Many2one('res.users', string='User')

    @api.model
    def create(self, vals):
        """Creates user from res.partner model and assigns it to the corresponding group"""
        record = super().create(vals)
        if vals.get('is_partner'):
            if not record.email:
                raise UserError("Email is mandatory to create a user.")
            user_vals = {
                'name': record.name,
                'login': record.email,
                'email': record.email,
            }
            user = self.env['res.users'].create(user_vals)

            if record.partner_type == 'teacher':
                group = self.env.ref('school_management.group_school_management_teachers')
                user.groups_id = [Command.link(group.id)]
            elif record.partner_type == 'staff':
                group = self.env.ref('school_management.group_school_management_office_staffs')
                user.groups_id = [Command.link(group.id)]
            record.user_id = user.id
        return record

