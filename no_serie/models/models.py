# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
import logging
_logger = logging.getLogger(__name__)


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    lot_ids = fields.Char(string='Número Serie')
    lot_assign = fields.Boolean(default=False, required=True)



class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.model
    def _write(self, vals):

        super(AccountInvoice, self)._write(vals)

        if self.env.context.get('Break'):
            return

        self = self.with_context(Break=True)


        _logger.info("EJECUTANDO WRITETETETETETTE")

        picking = self.env['stock.picking'].search([('origin', '=', self.origin)])

        _logger.info("dfkdvknvkc %r " % [ picking, self.origin])
        if picking:
            picking[0].update_invoice_line()



# class SaleOrderLine(models.Model):
#     _inherit = "sale.order.line"
#
#     @api.multi
#     def _prepare_invoice_line(self, qty):
#         self.ensure_one()
#         res = {}
#         account = self.product_id.property_account_income_id or self.product_id.categ_id.property_account_income_categ_id
#
#         if not account and self.product_id:
#             raise UserError(_('Please define income account for this product: "%s" (id:%d) - or for its category: "%s".') %
#                 (self.product_id.name, self.product_id.id, self.product_id.categ_id.name))
#
#         fpos = self.order_id.fiscal_position_id or self.order_id.partner_id.property_account_position_id
#         if fpos and account:
#             account = fpos.map_account(account)
#         picking = self.env['stock.picking'].search(['&', ('origin', '=', self.order_id.name), ('state', '=', "done")])
#         lot = " "
#         if picking:
#             pic = picking[0].id
#             move = self.env['stock.move'].search([ '&', ('picking_id', '=', pic),('product_id', '=', self.product_id.id) ])
#             if move:
#                 move_line = self.env['stock.move.line'].search(['&', ('move_id', '=', move.id), ('product_id', '=', self.product_id.id)])
#
#                 _logger.info("LOTESESESESEESES % r" % move_line)
#
#                 if move_line:
#                     if move_line.lot_id.name:
#                         lot = move_line.lot_id.name
#         res = {
#             'name': self.name,
#             'sequence': self.sequence,
#             'origin': self.order_id.name,
#             'account_id': account.id,
#             'price_unit': self.price_unit,
#             'quantity': qty,
#             'discount': self.discount,
#             'uom_id': self.product_uom.id,
#             'product_id': self.product_id.id or False,
#             'invoice_line_tax_ids': [(6, 0, self.tax_id.ids)],
#             'account_analytic_id': self.order_id.analytic_account_id.id,
#             'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
#             'display_type': self.display_type,
#             'lot_ids': lot,
#
#         }
#         return res

class Picking(models.Model):
    _inherit = "stock.picking"



    def update_invoice_line(self):

        picking_type = self.picking_type_id

        if picking_type.use_create_lots or picking_type.use_existing_lots:

            lines_to_check = self.move_line_ids


            lotes = {}


            for line in lines_to_check:

                lot = []

                product = line.product_id

                if product.id in lotes:

                    lotes[product.id].append(line.lot_id.name)
                else:
                    lot.append(line.lot_id.name)
                    lotes[product.id] = lot



            _logger.info("LOTEESEESEESESEESESE %r " % [lotes, len(self.move_line_ids)])


            invoices = True

            for lot in lotes:

                if not invoices:
                    break

                for l in lotes[lot]:

                    account_invoice_line = self.env['account.invoice.line'].search([('origin', '=', self.origin)
                                                                                       , ('product_id', '=', lot),
                                                                                    ('lot_assign', '=', False)])

                    if account_invoice_line:

                        if len(account_invoice_line) > 1:
                            account_invoice_line[0].lot_ids = '[' + l + ']'
                            account_invoice_line[0].lot_assign = True

                        else:
                            account_invoice_line.lot_ids = '[' + l + ']'
                            account_invoice_line.lot_assign = True

                    else:

                        account_invoice_line = self.env['account.invoice.line'].search([('origin', '=', self.origin)
                                                                                           , ('product_id', '=', lot)])

                        if account_invoice_line:

                            aux = account_invoice_line[0].lot_ids.strip('][').split(',')

                            if l not in aux:
                                aux.append(l)

                            s = ''
                            for e in aux:

                                if s:
                                    s += ',' + e
                                else:
                                    s += e

                            _logger.info('AUXXXXXXXXXXXX%r' % [aux, s])

                            account_invoice_line[0].lot_ids = '[' + s + ']'
                            account_invoice_line[0].lot_assign = True
                        else:
                            invoices = False
                            break




            # for line in lines_to_check:
            #     product = line.product_id
            #
            #     account_invoice_line = self.env['account.invoice.line'].search([('origin', '=', self.origin)
            #                                                                        , ('product_id', '=', product.id),
            #                                                                     ('lot_assign', '=', False)])
            #
            #     if account_invoice_line:
            #
            #         if len(account_invoice_line) > 1:
            #             account_invoice_line[0].lot_ids = line.lot_id.name
            #             account_invoice_line[0].lot_assign = True
            #
            #         else:
            #             account_invoice_line.lot_ids = line.lot_id.name
            #             account_invoice_line.lot_assign = True


    @api.multi
    def button_validate(self):

        res = super(Picking, self).button_validate()

        # self.env['stock.picking'].search()

        picking_type = self.picking_type_id

        if picking_type.use_create_lots or picking_type.use_existing_lots:

            lines_to_check = self.move_line_ids

            for line in lines_to_check:
                product = line.product_id

                account_invoice_line = self.env['account.invoice.line'].search([('origin', '=', self.origin)
                                                                                   , ('product_id', '=', product.id)])
                if account_invoice_line:
                    for line in account_invoice_line:
                        line.lot_assign = False


        self.update_invoice_line()

        return res