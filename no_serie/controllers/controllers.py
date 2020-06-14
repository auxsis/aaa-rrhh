# -*- coding: utf-8 -*-
from odoo import http

# class Features(http.Controller):
#     @http.route('/features/features/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/features/features/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('features.listing', {
#             'root': '/features/features',
#             'objects': http.request.env['features.features'].search([]),
#         })

#     @http.route('/features/features/objects/<model("features.features"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('features.object', {
#             'object': obj
#         })