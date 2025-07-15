from odoo import api, fields, models

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate Property"
    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date()
    expected_price = fields.Float()
    selling_price = fields.Float()
    bedrooms = fields.Integer()
    living_area = fields.Integer(string="Living Area(sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection( string='Garden Orientation Type',
        selection=[('north', 'North'), ('south', 'South'), ('west', 'West'), ('east', 'East')],)
    state = fields.Selection(
        selection=[('new', 'New'), ('offer', 'Offer Received'), ('sold', 'Sold'), ('cancel', 'Cancelled')],
        default='new'
    )
    active = fields.Boolean(default=True)
    property_type_id = fields.Many2one("estate.property.type", string="Property Type")
    salesman_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer")
    property_tags_ids = fields.Many2many("estate.property.tag",string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id",string="Offers")

    total_area = fields.Float(compute = "_compute_total")
    @api.depends("living_area","garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area=record.living_area + record.garden_area

    best_seller_price = fields.Float(compute="_best_seller_price")
    @api.depends("offer_ids.price")
    def _best_seller_price(self):
        for record in self:
            if record.offer_ids:
                record.best_seller_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_seller_price = 0.00

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area= 10
            self.garden_orientation='north'
        else:
            self.garden_area = 0
            self.garden_orientation= ''

    class TestAction(models.Model):
        _name = "test.action"
        name = fields.Char()
    def sell(self):
        for record in self:
            record.state = "sold"
        return True
    def cancel(self):
        for record in self:
           record.state = "cancel"
        return True

