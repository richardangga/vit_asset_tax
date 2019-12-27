from odoo import api, fields, models, _
import time
from odoo.exceptions import UserError, Warning
import logging
_logger = logging.getLogger(__name__)
import odoo.addons.decimal_precision as dp
import datetime
STATES = [('draft', 'Draft'), ('open', 'Open'), ('done','Done') ]
TYPES = [('writeoff','Write Off'),('sale','Sale')]

class disposal_line_tax(models.Model):
    _name = 'vit.disposal.line'
    _inherit = "vit.disposal.line"   
    disposal_tax = fields.Many2many('account.tax', 'tax_disposal','account_id', 'tax_id', string='Tax')
class disposal_invoice_tax(models.Model):
    _name = "vit.disposal"
    _inherit = "vit.disposal"
    
    # amount_untaxed = fields.Monetary(string='Untaxed Amount',store=True, readonly=True, compute='_compute_amount_total', track_visibility='always')
    # amount_total = fields.Monetary(string='Total',store=True, readonly=True, compute='_compute_amount_total')
    # amount_tax = fields.Monetary(string='Tax',store=True, readonly=True, compute='_compute_amount_total')
        
    @api.multi
    def action_approve(self):
        self.validity_check()
        for me_id in self :
            if me_id.state != 'open' :
                continue
            if me_id.disposal_type == 'sale' :
                existence = 'sold'
                me_id.create_sale_invoice()
            else :
                existence = 'writeoff'
                me_id.create_write_off_journal()
            for line in me_id.disposal_line :
                line.asset_id.action_close({'existence':existence})
            me_id.write({'state':STATES[2][0]})
            
    @api.model
    def create_sale_invoice(self): 
        self.ensure_one()
        if self.disposal_type != 'sale' :
            return
        inv_line_vals = []
        inv_line_vals.append((0,0,{
            'name': 'Disposal %s'%(self.name),
            'account_id': self.disposal_line.asset_id.category_id.asset_disposal_profit_id.id,
            'quantity': 1,
            'invoice_line_tax_ids': [(6,None,self.disposal_line.disposal_tax.ids)],
            'price_unit': self.disposal_line.value_residual,
        }))
        invoice_id = self.env['account.invoice'].create({
            'partner_id': self.disposal_customer_id.id,
            'journal_id': self.disposal_journal_id.id,
            'account_id': self.disposal_customer_id.property_account_receivable_id.id,
            'type': 'out_invoice',
            'origin': self.name,
            'invoice_line_ids': inv_line_vals,
            'comment': self.notes,
        })
        self.write({'disposal_invoice_id':invoice_id.id})
        
    @api.multi
    def preview_invoice(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'target': 'self',
            'url': self.get_portal_url(),
        }
    
    # @api.one
    # @api.depends('amount','disposal_tax')
    # def _compute_amount_total(self):
    #     # self.ensure_one()
    #     # for line in self.disposal_line :
    #         self.amount_untaxed = line.amount
    #         self.amount_tax = line.id*line.amount
    #         self.amount_total = self.amount_untaxed - self.amount_tax     
    
    # @api.multi
    # def action_invoice_sent(self):
    #     """ Open a window to compose an email, with the edi invoice template
    #         message loaded by default
    #     """
    #     self.ensure_one()
    #     template = self.env.ref('account.email_template_edi_invoice', False)
    #     compose_form = self.env.ref('account.account_invoice_send_wizard_form', False)
    #     # have model_description in template language
    #     lang = self.env.context.get('lang')
    #     if template and template.lang:
    #         lang = template._render_template(template.lang, 'account.invoice', self.id)
    #     self = self.with_context(lang=lang)
    #     TYPES = {
    #         'out_invoice': _('Invoice'),
    #         'in_invoice': _('Vendor Bill'),
    #         'out_refund': _('Credit Note'),
    #         'in_refund': _('Vendor Credit note'),
    #     }
    #     ctx = dict(
    #         default_model='account.invoice',
    #         default_res_id=self.id,
    #         default_use_template=bool(template),
    #         default_template_id=template and template.id or False,
    #         default_composition_mode='comment',
    #         mark_invoice_as_sent=True,
    #         model_description=TYPES[self.type],
    #         custom_layout="mail.mail_notification_paynow",
    #         force_email=True
    #     )
    #     return {
    #         'name': _('Send Invoice'),
    #         'type': 'ir.actions.act_window',
    #         'view_type': 'form',
    #         'view_mode': 'form',
    #         'res_model': 'account.invoice.send',
    #         'views': [(compose_form.id, 'form')],
    #         'view_id': compose_form.id,
    #         'target': 'new',
    #         'context': ctx,
    #     }
    