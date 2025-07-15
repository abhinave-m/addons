# -*- coding: utf-8 -*-
from odoo import fields, models


class SurveySurvey(models.Model):
    """Adding relation to survey contact from model survey"""
    _inherit = 'survey.survey'

    survey_contact_ids = fields.One2many('survey.contact', 'survey_id')
