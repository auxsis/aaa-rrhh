'''
Created on Dec 11, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class HrSalaryRule(models.Model):
    _inherit = 'hr.salary.rule'

    t_analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', company_dependent = True)
    t_account_tax_id = fields.Many2one('account.tax', 'Tax', company_dependent = True)
    t_account_debit = fields.Many2one('account.account', 'Debit Account', domain=[('deprecated', '=', False)], company_dependent = True)
    t_account_credit = fields.Many2one('account.account', 'Credit Account', domain=[('deprecated', '=', False)], company_dependent = True)

    analytic_account_id = fields.Many2one(compute = '_calc_account', store = False)
    account_tax_id = fields.Many2one(compute = '_calc_account', store = False)
    account_debit = fields.Many2one(compute = '_calc_account', store = False)
    account_credit = fields.Many2one(compute = '_calc_account', store = False)
    
    account_ids = fields.One2many('hr.payroll.structure.account','rule_id', copy = False)

    @api.depends('t_analytic_account_id','t_account_tax_id', 't_account_debit', 't_account_credit')
    def _calc_account(self):
        struct_id = self._context.get('struct_id') 
        for record in self:
            struct_account_id = struct_id and self.env['hr.payroll.structure.account'].search([('struct_id','=', struct_id), ('rule_id','=', record.id)], limit = 1)
            for fname in ['analytic_account_id', 'account_tax_id', 'account_debit', 'account_credit']:
                
                if struct_account_id:
                    if struct_account_id.no_debit and fname == 'account_debit':
                        record[fname] = False
                        continue
                    
                    if struct_account_id.no_credit and fname == 'account_credit':
                        record[fname] = False
                        continue
                
                record[fname] = struct_account_id and struct_account_id[fname] or record['t_%s' % fname]
                    