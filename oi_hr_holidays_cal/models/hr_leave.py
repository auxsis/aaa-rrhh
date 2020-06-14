'''
Created on Jan 27, 2019

@author: Zuhair Hammadi
'''
from odoo import models

class HolidaysRequest(models.Model):
    _inherit = "hr.leave"
    
    def _get_number_of_days(self, date_from, date_to, employee_id):
        if self.holiday_status_id.calc_type=='calendar':
            return (date_to - date_from).days + 1
        return super(HolidaysRequest, self)._get_number_of_days(date_from, date_to, employee_id)
