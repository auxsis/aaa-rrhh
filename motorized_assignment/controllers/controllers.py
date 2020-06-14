# -*- coding: utf-8 -*-
from odoo import http

# class MotorizedAssignment(http.Controller):
#     @http.route('/motorized_assignment/motorized_assignment/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/motorized_assignment/motorized_assignment/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('motorized_assignment.listing', {
#             'root': '/motorized_assignment/motorized_assignment',
#             'objects': http.request.env['motorized_assignment.motorized_assignment'].search([]),
#         })

#     @http.route('/motorized_assignment/motorized_assignment/objects/<model("motorized_assignment.motorized_assignment"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('motorized_assignment.object', {
#             'object': obj
#         })