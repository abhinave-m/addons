from cffi.model import qualify

from odoo import fields, models


class Example(models.Model):
    _name = "example"
    _description = "Example"

    name = fields.Char(string='Name')
    partner_id = fields.Many2one('res.partner', 'Partner')
    tag_ids = fields.Many2many('example.tags', string='Tags')
    line_ids = fields.One2many('example.lines','example_id')
    tags_ids = fields.Many2many('example.tags', string='Tagsss', relation='example_example_tags2_rel', column1='example_id', column2='tag_id')

    def action_test(self):
        product_id = self.env['product.product'].search([], limit=1, order='id DESC')
        print(f'Hi  {self, product_id}')
        # self.line_ids = [fields.Command.create({
        #     'product_id': product_id.id,
        #     'quantity': 1,
        #     'price': product_id.list_price,
        # })]
        # self.env['example.lines'].create({
        #     'product_id': product_id.id,
        #     'quantity': 1,
        #     'price': product_id.list_price,
        #     'example_id': self.id
        # })
        # line_id=self.line_ids[0]
        new_line_ids=self.line_ids.search([('example_id','=',False)])

        print(new_line_ids.ids)
        # self.line_ids = [fields.Command.update(line_id.id,{
        #     'quantity': 3,
        # })]
        # line_id.quantity=2
        # self.env['example.lines'].search([('example_id',"=",self.id)]).write({'quantity': 4})
        # self.line_ids = [fields.Command.delete(line_id.id)]
        # line_id.unlink()
        #  self.line_ids = [fields.Command.unlink(line_id.id)]
        # line_id.write({
        #     'example_id':False
        # })

        # self.line_ids = [fields.Command.link(new_line_id.id)]
        # new_line_id.write({
        #     'example_id':self.id
        #  })
        # self.line_ids = [fields.Command.clear()]
        # self.line_ids.write({'example_id': False})
        # self.line_ids = [fields.Command.set(new_line_ids.ids)
        # self.line_ids = [fields.Command.clear(),fields.Command.link(new_line_ids[0].id)]

        # self.line_ids = [fields.Command.create({
        #         'product_id': product_id.id,
        #         'quantity': 1,
        #         'price': product_id.list_price,
        #     }),fields.Command.create({
        #         'product_id': product_id.id,
        #         'quantity': 2,
        #         'price': product_id.list_price,
        #     }),fields.Command.create({
        #         'product_id': product_id.id,
        #         'quantity': 3,
        #         'price': product_id.list_price,
        #     })]

        prev_exmple =self.search([('id','!=',self.id)],order ='id DESC')
        print(prev_exmple)
        o2m_ids = prev_exmple.line_ids
        # self.line_ids = o2m_ids
        # o2m_list = []
        print(o2m_ids)
        # for rec in o2m_ids:
        #     print('rec',rec)
        #     dictionary={
        #         'product_id':rec.product_id.id,
        #         'quantity':rec.quantity,
        #         'price':rec.price
        #     }
        #     o2m_list.append(fields.Command.create(dictionary))
        # print(o2m_list)
        # self.line_ids = [fields.Command.create({
        #         'product_id':rec.product_id.id,
        #         'quantity':rec.quantity,
        #         'price':rec.price
        #     }) for rec in o2m_ids]

        # self.tag_ids = [fields.Command.link(self.env.ref('example.example_tag_abc').id)]
        # filtered_lines = self.line_ids.filtered(lambda x: x.quantity >= 10).sorted('price', reverse=False).mapped('product_id.name')
        # print(self.read())
        # print(self.search_read([('id', '!=', self.id)], ['name', 'line_ids']))

