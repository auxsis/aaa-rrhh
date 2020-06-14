# -*- coding: utf-8 -*-
from odoo import http

# class ReportExcelCoerco(http.Controller):
#     @http.route('/report_excel_coerco/report_excel_coerco/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/report_excel_coerco/report_excel_coerco/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('report_excel_coerco.listing', {
#             'root': '/report_excel_coerco/report_excel_coerco',
#             'objects': http.request.env['report_excel_coerco.report_excel_coerco'].search([]),
#         })

#     @http.route('/report_excel_coerco/report_excel_coerco/objects/<model("report_excel_coerco.report_excel_coerco"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('report_excel_coerco.object', {
#             'object': obj
#         })