from odoo import fields, models, api

class ExampleLines(models.Model):
    _name = "example.lines"

    product_id = fields.Many2one('product.product', string="Product ID")
    quantity = fields.Integer()
    price = fields.Integer()
    subtotal = fields.Integer(compute='_compute_subtotal')
    example_id = fields.Many2one("example", string="Example ID")

    @api.depends('quantity', 'price')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.quantity * rec.price