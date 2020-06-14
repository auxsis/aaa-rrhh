'''
Created on Oct 17, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class HrPayslipEmployees(models.TransientModel):
    _inherit = 'hr.payslip.employees'
    
    @api.model
    def _get_company(self):
        active_id = self.env.context.get('active_id')
        if active_id:
            return self.env['hr.payslip.run'].browse(active_id).company_id

    company_id = fields.Many2one('res.company', string='Company', required = True, default=_get_company)   