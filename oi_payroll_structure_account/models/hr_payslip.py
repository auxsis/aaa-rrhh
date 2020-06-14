'''
Created on Dec 11, 2018

@author: Zuhair Hammadi
'''
from odoo import models, api

class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    @api.multi
    def action_payslip_done(self):
        for record in self:
            record = record.with_context(struct_id = record.struct_id.id)
            super(HrPayslip, record).action_payslip_done()
            
        return True