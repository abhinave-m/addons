#-*- coding: utf-8 -*-
from odoo import api, fields, models
from datetime import timedelta


class Leave(models.Model):
    """Leave fields declaration"""
    _name = "leave"
    _description = "Leave"
    _inherit = ['mail.thread']
    _rec_name = "student_id"

    student_id = fields.Many2one("registration","Student",required=True,domain="[('status','=','enroled')]")
    class_id = fields.Many2one("manage.class","Class",related='student_id.current_class_id',store=True)
    start_date = fields.Date()
    end_date = fields.Date()
    half_day = fields.Boolean()
    reason = fields.Text()
    total_days = fields.Float(compute='_compute_total_days',store=True)
    _sql_constraints = [
        ('check_date','CHECK(start_date<=end_date)','End date should be greater/equal to Start date')
    ]

    @api.depends('start_date','end_date','half_day')
    def _compute_total_days(self):
        """Calculates the total days excluding Saturdays and Sundays"""
        for record in self:
            if record.start_date and record.end_date:
                day_count = 0
                current_day = record.start_date
                while current_day <= record.end_date:
                    if current_day.isoweekday() not in (6,7):
                        day_count += 1
                    current_day += timedelta(days=1)
                    if record.half_day and day_count == 1:
                        record.total_days = 0.5
                    elif record.half_day and day_count > 1:
                        record.total_days = day_count + 0.5
                    else:
                        record.total_days = day_count
            else:
                record.total_days = 0