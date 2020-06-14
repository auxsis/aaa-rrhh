# -*- coding: utf-8 -*-
######################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2019-TODAY Cybrosys Technologies(<https://www.cybrosys.com>).
#    Author: Nimisha Murali (Contact : odoo@cybrosys.com)
#
#    This program is under the terms of the Odoo Proprietary License v1.0 (OPL-1)
#    It is forbidden to publish, distribute, sublicense, or sell copies of the Software
#    or modified copies of the Software.
#
#    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#    IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#    DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
#    ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#    DEALINGS IN THE SOFTWARE.
#
########################################################################################
import datetime
import decimal
import datetime as dt
from odoo import models, api
from odoo.tools.float_utils import float_round
import math


class Leaves(models.TransientModel):
    _name = 'website.leave'

    @api.model
    def get_days(self, date_from, date_to):
        """ Returns the employee work days data between dates"""
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)])
        date1 = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        date2 = datetime.datetime.strptime(date_to, '%Y-%m-%d')
        for i in employee.resource_calendar_id.attendance_ids:
            if i.dayofweek == str(date1.weekday()):
                time1 = '0' + str(i.hour_from)[:1] + '00' if len(str(i.hour_from)) == 3 else str(i.hour_from)[
                                                                                                 :2] + '00'
            if i.dayofweek == str(date2.weekday()):
                time2 = '0' + str(i.hour_to)[:1] + '00' if len(str(i.hour_to)) == 3 else str(i.hour_to)[
                                                                                                 :2] + '00'
        time_obj1 = dt.datetime.strptime(time1, '%H%M').time()
        time_obj2 = dt.datetime.strptime(time2, '%H%M').time()

        date_obj1 = dt.datetime.strptime(date_from, '%Y-%m-%d')
        date_time1 = dt.datetime.combine(date_obj1.date(), time_obj1)
        date_obj2 = dt.datetime.strptime(date_to, '%Y-%m-%d')
        date_time2 = dt.datetime.combine(date_obj2.date(), time_obj2)

        return math.ceil(employee.get_work_days_data(date_time1, date_time2)['days'])

    @api.model
    def get_days_half(self, date_from, date_to):
        """ Returns the employee work days data between dates"""
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)])
        date1 = datetime.datetime.strptime(date_from, '%Y-%m-%d')
        for i in employee.resource_calendar_id.attendance_ids:
            if i.dayofweek == str(date1.weekday()):
                time1 = '0' + str(i.hour_from)[:1] + '00' if len(str(i.hour_from)) == 3 else str(i.hour_from)[
                                                                                             :2] + '00'
                time2 = '0' + str(i.hour_to)[:1] + '00' if len(str(i.hour_to)) == 3 else str(i.hour_to)[
                                                                                         :2] + '00'
        time_obj1 = dt.datetime.strptime(time1, '%H%M').time()
        time_obj2 = dt.datetime.strptime(time2, '%H%M').time()

        date_obj1 = dt.datetime.strptime(date_from, '%Y-%m-%d')
        date_time1 = dt.datetime.combine(date_obj1.date(), time_obj1)
        date_obj2 = dt.datetime.strptime(date_to, '%Y-%m-%d')
        date_time2 = dt.datetime.combine(date_obj2.date(), time_obj2)
        if 0 < employee.get_work_days_data(date_time1, date_time2)['days'] < 1:
            return 0.5
        else:
            return employee.get_work_days_data(date_time1, date_time2)['days']

    @api.model
    def alert_leave(self, date_from, date_to, request_unit_half):
        """ Check whether leave is created or not for requested dates"""
        date_obj1 = dt.datetime.strptime(date_from, '%Y-%m-%d')
        date_obj2 = dt.datetime.strptime(date_to, '%Y-%m-%d')
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)])
        if request_unit_half is True:
            res = self.env['hr.leave'].sudo().search_count(
                [('request_date_from', '=', date_obj1)])
            if res != 0:
                flag = 1
                return flag
            else:

                flag = 0
                return flag

        else:
            res = self.env['hr.leave'].sudo().search_count([('request_date_from', '<=', date_obj2),
                                                            ('request_date_to', '>=', date_obj1),
                                                            ('employee_id', '=', employee.id),
                                                            ('state', 'not in', ['cancel', 'refuse'])])
            if res != 0:
                flag = 1
                return flag
            else:
                flag = 0
                return flag

    @api.model
    def alert_leave_type(self, select_leave, duration):
        """Check number of leaves remaining for the selected leave type"""
        leave_type_id = self.env['hr.leave.type'].sudo().search([('name', '=', select_leave)])
        employee = self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)])
        duration_float = float(duration)
        leave_count = float_round(leave_type_id.with_context(employee_id=employee.id).virtual_remaining_leaves,
                                  precision_digits=2)
        if leave_count < duration_float:
            flag = 1
            return flag

    @api.model
    def action_cancel(self, leave_id):
        """ Delete leave request"""
        self.env['hr.leave'].sudo().browse(leave_id).unlink()
