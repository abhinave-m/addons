# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SurveyContactMapping(models.Model):
    """Maps survey questions to partner contact fields."""
    _name = 'survey.contact.mapping'
    _description = 'Survey Contact Mapping'

    survey_id = fields.Many2one('survey.survey', required=True, ondelete='cascade')
    question_id = fields.Many2one('survey.question',string='Question',required=True,domain="[('survey_id', '=', survey_id), ('id', 'not in', used_question_ids)]")
    contact_field_id = fields.Many2one(
        'ir.model.fields',
        string='Contact Field',
        domain="[('model', '=', 'res.partner'), ('id', 'not in', used_contact_field_ids), ('name', 'in', ('name', 'email', 'mobile', 'street', 'city', 'zip', 'country_id'))]",
        required=True,
        ondelete='cascade'
    )
    used_question_ids = fields.Many2many('survey.question',compute='_compute_used_question_ids',string='Used Questions')
    used_contact_field_ids = fields.Many2many('ir.model.fields',compute='_compute_used_contact_field_ids',string='Used Contact Fields')

    @api.depends('survey_id', 'survey_id.contact_mapping_ids')
    def _compute_used_question_ids(self):
        """Checks whether the question has been already used or not."""
        for rec in self:
            if rec.survey_id:
                rec.used_question_ids = rec.survey_id.contact_mapping_ids.filtered(lambda r: r.id != rec.id).mapped('question_id')
            else:
                rec.used_question_ids = []

    @api.depends('survey_id', 'survey_id.contact_mapping_ids')
    def _compute_used_contact_field_ids(self):
        """Checks whether the field has been already used or not."""
        for rec in self:
            if rec.survey_id:
                rec.used_contact_field_ids = rec.survey_id.contact_mapping_ids.filtered(lambda r: r.id != rec.id).mapped('contact_field_id')
            else:
                rec.used_contact_field_ids = []


class SurveySurvey(models.Model):
    """Extends survey to hold partner field mappings for contact creation."""
    _inherit = 'survey.survey'

    contact_mapping_ids = fields.One2many(
        'survey.contact.mapping',
        'survey_id',
        string='Contact Mappings'
    )
