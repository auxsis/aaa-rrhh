'''
Created on Oct 17, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class HrPayslipRun(models.Model):
    _inherit = 'hr.payslip.run'
    
    journal_id = fields.Many2one(domain="[('company_id','=', company_id)]")

    company_id = fields.Many2one('res.company', string='Company', required = True, default=lambda self: self.env.user.company_id)   
    
    @api.onchange('company_id')
    def _onchange_company_id(self):
        if self.journal_id.company_id != self.company_id:
            self.journal_id = False