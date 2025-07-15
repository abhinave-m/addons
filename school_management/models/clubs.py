#-*- coding: utf-8 -*-
from odoo import fields, models


class Clubs(models.Model):
    """Clubs model field declaration"""
    _name = "clubs"
    _description = "Clubs"
    _inherit = ['mail.thread']

    name = fields.Char()
    student_ids = fields.Many2many('registration','registration_clubs_rel','club_id', 'registration_id',string="Students")
    event_ids = fields.One2many('events.club','club_id')
    event_count = fields.Integer(compute='_compute_event_count')

    def action_view_events(self):
        """Adds action to the Events smart button"""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Events',
            'res_model': 'events.club',
            'domain': [('club_id', '=', self.id)],
            'context': {'default_club_id' : self.id},
            'view_mode': 'list,form'
        }

    def _compute_event_count(self):
        """Computes the number of Events associated with the specific Club"""
        for rec in self:
            rec.event_count = self.env['events.club'].search_count([('club_id', '=', rec.id)])


