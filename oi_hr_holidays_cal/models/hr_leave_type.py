'''
Created on Jan 27, 2019

@author: Zuhair Hammadi
'''
from odoo import models, fields

class HolidaysType(models.Model):
    _inherit = "hr.leave.type"

    calc_type = fields.Selection([('work', 'Working Days'), ('calendar', 'Calendar Days')], string='Calculation Type', required = True, default = 'work')