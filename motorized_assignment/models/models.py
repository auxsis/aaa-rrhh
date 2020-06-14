# -*- coding: utf-8 -*-

from odoo import models, fields, api


import logging

_logger = logging.getLogger(__name__)


class Picking(models.Model):

    _inherit = "stock.picking"

    @api.multi
    def button_validate(self):

        res = super(Picking, self).button_validate()

        #self.env['stock.picking'].search()

        _logger.info("Picking TYPEEEPEPEPPEPEPEPEPP %r "  % self.picking_type_id)

        if self.picking_type_id.id == 3 :
            picking = self.env['stock.picking'].search([('origin', '=', self.origin), ('picking_type_id.id','=', 2)])
            picking.write({'x_studio_motorizado_1': self.x_studio_motorizado_1.id})
            picking.write({'x_studio_horario_de_entrega': self.x_studio_horario_de_entrega})
        return res
