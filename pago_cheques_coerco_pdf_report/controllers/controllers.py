# -*- coding: utf-8 -*-
from odoo import http

# class PagoChequesCoercoPdfReport(http.Controller):
#     @http.route('/pago_cheques_coerco_pdf_report/pago_cheques_coerco_pdf_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pago_cheques_coerco_pdf_report/pago_cheques_coerco_pdf_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pago_cheques_coerco_pdf_report.listing', {
#             'root': '/pago_cheques_coerco_pdf_report/pago_cheques_coerco_pdf_report',
#             'objects': http.request.env['pago_cheques_coerco_pdf_report.pago_cheques_coerco_pdf_report'].search([]),
#         })

#     @http.route('/pago_cheques_coerco_pdf_report/pago_cheques_coerco_pdf_report/objects/<model("pago_cheques_coerco_pdf_report.pago_cheques_coerco_pdf_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pago_cheques_coerco_pdf_report.object', {
#             'object': obj
#         })