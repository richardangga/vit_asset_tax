from odoo import api, fields, models, _

class disposal_tax(models.Model):
    _name = 'vit.disposal.line'
    _inherit = "vit.disposal.line"   
    
    disposal_tax = fields.Many2one(
        string='Tax',
        comodel_name='account.tax',
        required=True,
    )
    
    
    