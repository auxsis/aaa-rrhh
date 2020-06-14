# -*- coding: utf-8 -*-
from odoo import http

# class ConsolidadoAutorizacionReportExcel(http.Controller):
#     @http.route('/consolidado_autorizacion_report_excel/consolidado_autorizacion_report_excel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/consolidado_autorizacion_report_excel/consolidado_autorizacion_report_excel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('consolidado_autorizacion_report_excel.listing', {
#             'root': '/consolidado_autorizacion_report_excel/consolidado_autorizacion_report_excel',
#             'objects': http.request.env['consolidado_autorizacion_report_excel.consolidado_autorizacion_report_excel'].search([]),
#         })

#     @http.route('/consolidado_autorizacion_report_excel/consolidado_autorizacion_report_excel/objects/<model("consolidado_autorizacion_report_excel.consolidado_autorizacion_report_excel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('consolidado_autorizacion_report_excel.object', {
#             'object': obj
#         })