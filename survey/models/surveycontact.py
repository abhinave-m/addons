# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SurveyContact(models.Model):
    """Mapping survey questions with res.partner fields"""
    _name = 'survey.contact'
    _parent_name = 'survey_id'
    _description = 'Survey Contact'


    question_id = fields.Many2one('survey.question',
                                  'Question',
                                  domain="[('survey_id', '=', survey_id), ('id', 'not in', used_question_ids)]",
                                  required=True)
    partner_field_id = fields.Many2one('ir.model.fields',
                                       'Contact',
                                       domain="[('model', '=', 'res.partner'), "
                                              "('id', 'not in', used_partner_field_ids)]",
                                       required=True, ondelete='cascade')
    survey_id = fields.Many2one('survey.survey')
    parent_path = fields.Char(index=True)
    used_question_ids = fields.Many2many('survey.question', compute='_compute_used_question_ids')
    used_partner_field_ids = fields.Many2many('ir.model.fields',
                                              compute='_compute_used_partner_field_ids', ondelete='cascade')

    @api.depends('survey_id')
    def _compute_used_question_ids(self):
        """To compute previously used questions"""
        for rec in self:
            if rec.survey_id:
                used_question_ids = (rec.survey_id.survey_contact_ids.filtered(lambda r: r.id != rec.id)
                                     .mapped('question_id.id'))
                rec.used_question_ids = used_question_ids

    @api.depends('survey_id')
    def _compute_used_partner_field_ids(self):
        """To compute previously used fields"""
        for rec in self:
            if rec.survey_id:
                used_partner_field_ids = (rec.survey_id.survey_contact_ids.filtered(lambda r: r.id != rec.id)
                                          .mapped('partner_field_id.id'))
                rec.used_partner_field_ids = used_partner_field_ids