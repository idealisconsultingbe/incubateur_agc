from odoo import models, api


class ElSaleOrder(models.Model):
    _inherit = 'sale.order.line'

    # This method comes from standard, it removes the 'filtered' by company on taxes
    def _compute_tax_id(self):
        for line in self:
            line = line.with_company(line.company_id)
            fpos = line.order_id.fiscal_position_id or line.order_id.fiscal_position_id.get_fiscal_position(line.order_partner_id.id)
            taxes = line.product_id.taxes_id
            line.tax_id = fpos.map_tax(taxes, line.product_id, line.order_id.partner_shipping_id)
