'''
Created on Dec 11, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields

class HrPayrollStructure(models.Model):
    _inherit = 'hr.payroll.structure'
    
    account_ids = fields.One2many('hr.payroll.structure.account','struct_id', copy = True)