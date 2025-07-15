# -*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import datetime, timedelta


class EventsClub(models.Model):
    """Events model field declaration"""
    _name = 'events.club'
    _description = 'Events Club'
    _inherit = ['mail.thread']

    name = fields.Char(required=True)
    event_image = fields.Image()
    club_id = fields.Many2one('clubs',string="Club Name")
    start_date = fields.Datetime(string="Start date")
    end_date = fields.Datetime(string="End date")
    status = fields.Selection([('new','New'),('ongoing','Ongoing'),('completed','Completed')], default='new', tracking=True)
    desc = fields.Text()
    poster = fields.Binary(string='Poster')
    active = fields.Boolean(readonly=False, default=True)
    reminder_date = fields.Datetime(compute='compute_reminder_date',readonly=False,store=True)

    @api.model
    def create(self, vals):
        """Overrides the original creation of records to check the status and active field"""
        record = super().create(vals)
        if record.end_date:
            record._check_event_status_on_save()
            return record

    def write(self, vals):
        """Overrides the original updation of records to check the status and active field"""
        res = super().write(vals)
        if self.end_date:
            self._check_event_status_on_save()
            return res

    def _check_event_status_on_save(self):
        """Change status to 'completed' and archives if end_date is today or earlier"""
        today = datetime.now()
        for rec in self:
            if rec.end_date and rec.end_date <= today and rec.status != 'completed':
                super(EventsClub, rec).write({
                    'status': 'completed',
                    'active': False
                })
            elif rec.end_date > today and rec.status == 'completed':
                super(EventsClub, rec).write({
                    'status': 'new',
                    'active': True
                })

    @api.onchange('status')
    def archive_event(self):
        """Archive events based on the change in status (manual)"""
        for rec in self:
            if rec.status == 'completed':
                rec.active = False
            else:
                rec.active = True

    @api.depends('start_date')
    def compute_reminder_date(self):
        """Calculates the reminder date"""
        for rec in self:
            if rec.start_date:
                current_date = rec.start_date
                current_date += timedelta(days=-2)
                rec.reminder_date = current_date
            else:
                rec.reminder_date = False

    def cron_send_event_reminders(self):
        """Send reminder emails to teachers and staffs on reminder date"""
        today = datetime.now().date()
        events = self.search([('reminder_date', '!=', False)])
        for event in events:
            if event.reminder_date.date() == today:
                template = self.env.ref('school_management.email_event_reminder_template')
                staff_partners = self.env['res.partner'].search([('is_partner', '=', True), ('email', '!=', False),])
                for partner in staff_partners:
                    template.send_mail(event.id, force_send=True, email_values={
                        'email_to': partner.email
                    })




