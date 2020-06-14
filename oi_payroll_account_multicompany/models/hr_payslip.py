'''
Created on Oct 15, 2018

@author: Zuhair Hammadi
'''
from odoo import models, api, fields

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'
    
    journal_id = fields.Many2one(domain="[('company_id','=', company_id)]")
    
    @api.multi
    def action_payslip_done(self):    
        for record in self:
            super(HrPayslip, record.with_context(force_company = record.company_id.id)).action_payslip_done()
        return True