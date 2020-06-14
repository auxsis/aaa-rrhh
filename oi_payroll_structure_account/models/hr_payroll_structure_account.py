'''
Created on Dec 11, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields

class HrPayrollStructureAccount(models.Model):
    _name = 'hr.payroll.structure.account'
    _description = 'Salary Structure Account'
    _rec_name = 'rule_id'
    
    struct_id = fields.Many2one('hr.payroll.structure', required = True, ondelete='cascade', string="Salary Structure")
    rule_id = fields.Many2one('hr.salary.rule', required = True, string='Rule', ondelete='cascade')
    
    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', copy = False, company_dependent = True)
    account_tax_id = fields.Many2one('account.tax', 'Tax', copy = False, company_dependent = True)
    account_debit = fields.Many2one('account.account', 'Debit Account', domain=[('deprecated', '=', False)], copy = False, company_dependent = True)
    account_credit = fields.Many2one('account.account', 'Credit Account', domain=[('deprecated', '=', False)], copy = False, company_dependent = True)
    
    no_debit = fields.Boolean('Clear Debit Account')
    no_credit = fields.Boolean('Clear Credit Account')

    _sql_constraints = [
        ('rule_unique', 'UNIQUE(struct_id,rule_id)','Duplicate Rule!')
        ]
            