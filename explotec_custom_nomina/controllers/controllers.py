# -*- coding: utf-8 -*-
from odoo import http

# class ExplotecCustomNomina(http.Controller):
#     @http.route('/explotec_custom_nomina/explotec_custom_nomina/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/explotec_custom_nomina/explotec_custom_nomina/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('explotec_custom_nomina.listing', {
#             'root': '/explotec_custom_nomina/explotec_custom_nomina',
#             'objects': http.request.env['explotec_custom_nomina.explotec_custom_nomina'].search([]),
#         })

#     @http.route('/explotec_custom_nomina/explotec_custom_nomina/objects/<model("explotec_custom_nomina.explotec_custom_nomina"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('explotec_custom_nomina.object', {
#             'object': obj
#         })