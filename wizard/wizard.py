# -*- coding: utf-8 -*-

from odoo import models, fields, api


class set_delete(models.TransientModel):
    _name = 'delete.wizard'

    def get_customer(self):
        payments = self.env['tr.take.customer'].search(['|',
                                                        ('state','=','reject'),'&',
                                                        ('state','=','draft'),
                                                        ('amount','<','1000')]) #.unlink()
        payment_ids = []
        for line in payments:
            payment_ids.append(line.id)
        return payment_ids

    customer_ids = fields.Many2many(
        comodel_name="tr.take.customer",
        string="Customer",
        required=False,
        readonly=True,
        default=get_customer
    )


    def delete_cutomer(self):
        self.customer_ids.unlink()


class tranfer_date_amount(models.TransientModel):
    _name = 'tranfer.date.amount.wizard'

    def get_date(self):
        active_model = self._context['active_model']
        active_id = self._context['active_id']
        date = self.env[active_model].search([('id','=',active_id)]).visit_date

        return date

    def get_amount(self):
        active_model = self._context['active_model']
        active_id = self._context['active_id']
        amount = self.env[active_model].search([('id', '=', active_id)]).amount

        return amount

    visit_date = fields.Date(
        string="Visit Date",
        required=False,
        default=get_date
    )

    amount = fields.Float(
        digits=(6, 2),
        string="Amount",
        required=True,
        default=get_amount
    )

    def tranfer_date_amount(self):
        active_model = self._context['active_model']
        active_id = self._context['active_id']
        pos_obj = self.env[active_model].search([('id', '=', active_id)])
        pos_obj.write({'amount': self.amount,
                       'visit_date': self.visit_date})


class set_done(models.TransientModel):
    _name = 'done.wizard'

    def get_customer(self):
        payments = self.env['tr.take.customer'].search([('state', '=', 'approve')]) #.unlink()
        payment_ids = []
        for line in payments:
            payment_ids.append(line.id)
        return payment_ids

    customer_ids = fields.Many2many(
        comodel_name="tr.take.customer",
        string="Customer",
        required=False,
        default=get_customer
    )

    def update_approve_done(self):
        for a in self.customer_ids:
            a.write({'state': 'done'})
