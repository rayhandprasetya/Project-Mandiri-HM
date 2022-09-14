# -*- coding: utf-8 -*-
# from odoo import http


# class Kostan(http.Controller):
#     @http.route('/kostan/kostan', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/kostan/kostan/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('kostan.listing', {
#             'root': '/kostan/kostan',
#             'objects': http.request.env['kostan.kostan'].search([]),
#         })

#     @http.route('/kostan/kostan/objects/<model("kostan.kostan"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('kostan.object', {
#             'object': obj
#         })
