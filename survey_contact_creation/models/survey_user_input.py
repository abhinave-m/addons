#-*- coding: utf-8 -*-
from odoo import models, fields


class SurveyUserInput(models.Model):
    """Extends survey input to link or create a contact."""
    _inherit = 'survey.user_input'

    contact_creation_id = fields.Many2one('res.partner', string="Created Contact")

    def _mark_done(self):
        """Process survey answers to create or link a partner contact."""
        for user_input in self:
            survey = user_input.survey_id
            if not survey.contact_mapping_ids:
                continue

            data = {}
            for line in user_input.user_input_line_ids:
                answer_type = line.answer_type
                answer_field = f'value_{answer_type}' if answer_type else None
                answer = getattr(line, answer_field, None) if answer_field else None

                for mapping in survey.contact_mapping_ids:
                    if mapping.question_id == line.question_id and answer:
                        data[mapping.contact_field_id.name] = answer

            if not data:
                continue

            email_value = data.get('email')
            if email_value:
                existing_contact = self.env['res.partner'].search([('email', '=', email_value)], limit=1)
                if existing_contact:
                    user_input.contact_creation_id = existing_contact.id
                    continue

            contact = self.env['res.partner'].create({
                **data,
                'name': data.get('name', 'Survey User'),
            })
            user_input.contact_creation_id = contact.id
        return super(SurveyUserInput, self)._mark_done()