from odoo import api, fields, models, _

class disposal_tax(models.Model):
    _name = 'vit.disposal.line'
    _inherit = "vit.disposal.line"   
    
    disposal_tax = fields.Many2one(
        string='Tax',
        comodel_name='account.tax',
        required=True,
    )
    
    # def disposal_net_profit(self):
    #     profit_untaxed = vit.disposal.line.amount - vit.disposal.line.value_residual
    #     tax_value = vit.disposal.line.amount * disposal_tax
    #     net_profit = profit_untaxed - tax_value

    