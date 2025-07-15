from odoo import models, fields

class SurveyContactMapping(models.Model):
    _name = 'survey.contact.mapping'
    _description = 'Survey Contact Mapping'

    survey_id = fields.Many2one('survey.survey', required=True, ondelete='cascade')
    question_id = fields.Many2one('survey.question', string='Question', required=True, domain="[('survey_id', '=', parent.id)]")
    contact_field = fields.Selection(
        [
            ('name', 'Name'),
            ('email', 'Email'),
            ('phone', 'Phone'),
            ('mobile', 'Mobile'),
            ('street', 'Street'),
            ('city', 'City'),
            ('zip', 'Zip'),
            ('country_id', 'Country'),
        ],
        string='Contact Field',
        required=True
    )

class SurveySurvey(models.Model):
    _inherit = 'survey.survey'

    contact_mapping_ids = fields.One2many(
        'survey.contact.mapping',
        'survey_id',
        string='Contact Mappings'
    )
