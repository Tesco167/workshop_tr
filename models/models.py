from odoo import models, fields, api, exceptions

class tr_project(models.Model):
    _name = 'tr.project'

    name = fields.Char(
        string="Name",
        required=True,
    )

    code = fields.Char(
        string="Code",
        required=True,
    )

    @api.multi
    @api.constrains('code')
    def _identify_same_name(self):
        for record in self:
            obj = self.search([('code', '=ilike', record.code), ('id', '!=', record.id)])
            if obj:
                raise exceptions.ValidationError(
                    "Already have code!")

    budget = fields.Float(
        digits=(6, 2),
        string="Budget",
        required=True,
    )

    @api.multi
    @api.constrains('budget')
    def _identify_same_name(self):
        for record in self:
            if record.budget < 0:
                raise exceptions.ValidationError(
                    "Budget must over 0")

    customer_id = fields.One2many(
        comodel_name="tr.take.customer",
        inverse_name="tr_project_id",
        string="Customer",
        required=False,
        domain=[('state', '=', 'approve')],
        readonly=True
    )

    balance = fields.Float(
        digits=(6, 2),
        string="Balance",
        compute='_compute_name'
    )

    @api.multi
    def _compute_name(self):
        i = 0
        for a in self.customer_id:
            if a.state == 'approve':
                i += a.amount

        for record in self:
            record.balance = (record.budget - i)

    progress_balance = fields.Integer(
        string="",
        required=False,
        compute='_get_balance_progress'
    )

    @api.multi
    def _get_balance_progress(self):
        for a in self:
            self.progress_balance = ((a.balance / a.budget) * 100)

class tr_take_customer(models.Model):
    _name = 'tr.take.customer'

    tr_project_id = fields.Many2one(
        comodel_name="tr.project",
        string="Project",
        required=True,
        states={'approve': [('readonly', True)],
                'reject': [('readonly', True)]}
    )

    visit_date = fields.Date(
        string="Visit Date",
        required=True,
        default=fields.date.today(),
        states={'approve': [('readonly', True)],
                'reject': [('readonly', True)]}
    )

    customer_id = fields.Many2one(
        comodel_name="res.partner",
        string="Customer",
        required=True,
        domain=[('customer', '=', True)],
        states={'approve': [('readonly', True)],
                'reject': [('readonly', True)]}
    )

    sales_id = fields.Many2many(
        comodel_name="res.users",
        relation="map_customer_sales",
        column1="sales_id",
        column2="id",
        string="Sales",
        states={'approve': [('readonly', True)],
                'reject': [('readonly', True)]}
    )

    sales_order_ids = fields.Many2one(
        comodel_name="sale.order",
        string="Sales Order",
        required=False,
    )

    amount = fields.Float(
        digits=(6, 2),
        string="Amount",
        required=True,
        states={'approve': [('readonly', True)],
                'reject': [('readonly', True)]}
    )

    @api.multi
    @api.constrains('amount')
    def _identify_same_name(self):
        for record in self:
            if record.amount < 0:
                raise exceptions.ValidationError(
                    "Amount must over 0")

    state = fields.Selection([
            ('draft', 'Draft'),
            ('wait', 'Wait'),
            ('approve', 'Approve'),
            ('reject', 'Reject'),
            ('done','Done')
            ],default='draft')

    balance = fields.Float(
        string="Project balance",
        required=False,
        compute='_balance_check'
    )

    @api.model
    def _balance_check(self):
        self.balance = self.tr_project_id.balance

    # This function is triggered when the user clicks on the button 'Set to started'
    @api.multi
    def request_progressbar(self):
        for record in self:
            if (self.tr_project_id.balance - self.amount) >= 0:
                record.write({
                    'state': 'approve'
                })
            else:
                record.write({
                    'state': 'wait'
                })

    # This function is triggered when the user clicks on the button 'In progress'
    @api.multi
    def approve_progressbar(self):
        for record in self:
            record.write({
                'state': 'approve'
            })

    # This function is triggered when the user clicks on the button 'Done'
    @api.multi
    def reject_progressbar(self):
        for record in self:
            record.write({
                'state': 'reject',
            })