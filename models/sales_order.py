# -*- coding: utf-8 -*-
from odoo import fields, models, api

class sales_order(models.Model):
    _inherit = 'sale.order'

    # Add a new column to the res.partner model, by default partners are not
    # instructors
    tr_project_id = fields.Many2one(
        comodel_name="tr.project",
        string="TR Project",
        required=False,
    )

    tr_customer_ids = fields.One2many(
        comodel_name="tr.take.customer",
        inverse_name="sales_order_ids",
        string="TR Customer",
        required=False
    )

    @api.onchange('tr_project_id')
    def test_change(self):
        dd = self._origin.id
        payments = self.tr_customer_ids.search([('tr_project_id','=',self.tr_project_id.id)]) #.unlink()
        payment_ids = []
        for line in payments:
            payment_ids.append(line.id)

        pos_obj = self.env['tr.take.customer'].search([('tr_project_id','=',self.tr_project_id.id)])
        pos_obj.write({'sales_order_ids': dd})

        self.tr_customer_ids = payment_ids