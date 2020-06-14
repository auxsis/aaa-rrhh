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

from odoo import http
from odoo.http import request


class WebsiteLeaves(http.Controller):
    """Route to different pages from website"""
    @http.route('/page/my_leave_details',  type='http', auth='user', website=True)
    def leave_details(self):
       login = request.session.uid
       leave_details = request.env['hr.leave'].sudo().search([('user_id', '=', login)])
       return request.render('portal_leave_request.leaves_page', {'leaves': leave_details})

    @http.route('/leave_request', type='http', auth='user', website=True)
    def leave_requests(self):
        leave_type = request.env['hr.leave.type'].sudo().search([])
        leave = request.env['hr.leave'].sudo().search([])
        return request.render('portal_leave_request.leaves_create_page', {'leave_type': leave_type,
                                                                    'leave': leave})

    @http.route('/leave_created', type='http', auth='user', website=True)
    def success(self):
        response = request.render('portal_leave_request.leaves_created')
        return response

    @http.route('/leave_cancel', type='http', auth='user', website=True)
    def cancel(self):
        response = request.render('portal_leave_request.leaves_cancel',)
        return response

    @http.route('/request', type='json', auth='user', methods=['POST'], website=True, csrf=False)
    def submit(self, leave_type_select_name, date_from, date_to, duration, half_day, description, request_unit_half_name):
        leave_type_id = request.env['hr.leave.type'].sudo().search([('name', '=', leave_type_select_name)])
        leave_type = leave_type_id.id
        employee = request.env['hr.employee'].sudo().search([('user_id', '=', request.env.uid)])
        if not half_day:

            leaves = request.env['hr.leave'].sudo().search([])
            create_leave = {
                'employee_id': employee.id,
                'request_date_from': date_from,
                'request_date_to': date_to,
                'name': description,
                'holiday_status_id': leave_type,
                'number_of_days': duration
            }
            leaves += request.env['hr.leave'].sudo().create(create_leave)
        else:
            leaves = request.env['hr.leave'].sudo().search([])
            create_leave = {
                'employee_id': employee.id,
                'holiday_status_id': leave_type,
                'request_date_from': date_from,
                'number_of_days': duration,
                'request_unit_half': half_day,
                'request_date_from_period': request_unit_half_name,
                'name': description
            }
            leaves += request.env['hr.leave'].sudo().create(create_leave)
