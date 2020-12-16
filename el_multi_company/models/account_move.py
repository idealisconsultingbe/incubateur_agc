from odoo import models, fields, _
from odoo.exceptions import UserError


class ElSaleAdvancePaymentInv(models.TransientModel):
    _inherit = 'sale.advance.payment.inv'

    def create_invoices(self):

        self = self.sudo() \
            .with_context(default_company_id=self.env.ref('base.main_company').id) \
            .with_company(self.env.ref('base.main_company')) \

        return super(ElSaleAdvancePaymentInv, self).create_invoices()

    # This method comes from standard, it adds the sudo() on invoice creation
    def _create_invoice(self, order, so_line, amount):
        if (self.advance_payment_method == 'percentage' and self.amount <= 0.00) or (self.advance_payment_method == 'fixed' and self.fixed_amount <= 0.00):
            raise UserError(_('The value of the down payment amount must be positive.'))

        amount, name = self._get_advance_details(order)

        invoice_vals = self._prepare_invoice_values(order, name, amount, so_line)

        if order.fiscal_position_id:
            invoice_vals['fiscal_position_id'] = order.fiscal_position_id.id
        invoice = self.env['account.move'].sudo().create(invoice_vals).with_user(self.env.uid)
        invoice.sudo().message_post_with_view('mail.message_origin_link',
                                              values={'self': invoice.sudo(), 'origin': order},
                                              subtype_id=self.env.ref('mail.mt_note').id)
        return invoice
