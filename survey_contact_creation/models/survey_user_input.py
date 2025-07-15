from odoo import api, models, fields
import logging
_logger = logging.getLogger(__name__)



class SurveyUserInput(models.Model):
    _inherit = 'survey.user_input'

    contact_creation_id = fields.Many2one('res.partner', string="Created Contact")


class SurveyUserInputLine(models.Model):
    _inherit = 'survey.user_input.line'

    @api.model_create_multi
    def create(self, vals_list):
        """Creating a contact from input lines"""
        for vals in vals_list:
            _logger.info("Creating input line with vals: %s", vals)
            user_input = self.env['survey.user_input'].browse(vals.get('user_input_id'))
            survey = user_input.survey_id
            contact = user_input.contact_creation_id
            question_id = vals.get('question_id')
            answer_type = vals.get('answer_type')
            answer_field = f'value_{answer_type}'
            answer = vals.get(answer_field)

            if not survey or not survey.contact_mapping_ids:
                continue

            for mapping in survey.contact_mapping_ids:
                if mapping.question_id.id == question_id:
                    field_name = mapping.contact_field
                    _logger.info("Mapping question %s to partner field %s with value %s",
                                 question_id, field_name, answer)

                    if not contact:
                        contact = self.env['res.partner'].create({
                            field_name: answer,
                            'name': answer if field_name == 'name' else 'Survey User'
                        })
                        user_input.contact_creation_id = contact.id
                    else:
                        contact.write({field_name: answer})

        return super(SurveyUserInputLine, self).create(vals_list)