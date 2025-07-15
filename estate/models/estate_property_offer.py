from odoo import api,fields,models
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"
    price = fields.Float()
    status = fields.Selection(selection=[('accepted','Accepted'),('refused','Refused')])
    buyer_id = fields.Many2one("res.partner", string="Buyer", required=True)
    property_id= fields.Many2one("estate.property",string="Property",required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_date_deadline", inverse="_inverse_date_deadline")

    @api.depends('validity', 'create_date')
    def _date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Date.today()
            offer.date_deadline = create_date + timedelta(days=offer.validity)

    def _inverse_date_deadline(self):
        for offer in self:
            create_date = offer.create_date or fields.Datetime.now()
            offer.validity = (offer.date_deadline - create_date.date()).days


    def accept_offer(self):
        for record in self:
            record.status='accepted'
    def reject_offer(self):
        for record in self:
            record.status='refused'


