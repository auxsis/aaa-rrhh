'''
Created on Oct 15, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'
    
    @api.model
    def _company_domain(self):
        company_id = self._context.get('force_company') or self.env.user.company_id.id
        return [('company_id', '=', company_id)]       
    
    @api.model
    def _account_domain(self):
        return [('deprecated', '=', False)] + self._company_domain()
    

    analytic_account_id = fields.Many2one(company_dependent = True, domain = _company_domain)
    account_tax_id = fields.Many2one(company_dependent = True, domain = _company_domain)
    account_debit = fields.Many2one(company_dependent = True, domain = _account_domain)
    account_credit = fields.Many2one(company_dependent = True, domain = _account_domain)