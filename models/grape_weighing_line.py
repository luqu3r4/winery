# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GrapeWeighingLine(models.Model):
    _name = 'winery.grape.weighing.line'
    _description = 'Líneas de Pesada de Uva'

    name = fields.Char(string="Referencia", required=True)
    datetime = fields.Datetime(string="Fecha", required=True)

    winegrower_id = fields.Many2one('winery.winegrower', string="Viticultor", required=True)
    winegrower_code = fields.Char(string="Nº Viticultor", compute='_compute_winegrower_code', store=True, readonly=True)

    # Parcela filtrada por viticultor
    plot_id = fields.Many2one('winery.plot', string="Parcela")

    table_wine = fields.Boolean(string="¿Vino de mesa?")
    grape_variety_id = fields.Many2one('winery.grape_variety', string="Variedad de Uva")
    alcohol_degree = fields.Float(string="Graduación", digits=(5,2))

    gross_weight = fields.Float(string="Peso Bruto", digits=(10,2))
    tare_weight = fields.Float(string="Peso Tara", digits=(10,2))
    net_weight = fields.Float(string="Peso Neto", compute='_compute_net_weight', store=True, digits=(10,2))

    notes = fields.Text(string="Descripción")

    # Relación con la cabecera (obligatoria para One2many)
    weighing_id = fields.Many2one('winery.grape.weighing', string="Pesada", required=True)

    @api.depends('winegrower_id')
    def _compute_winegrower_code(self):
        for rec in self:
            rec.winegrower_code = rec.winegrower_id.code if rec.winegrower_id else ''

    @api.depends('gross_weight', 'tare_weight')
    def _compute_net_weight(self):
        for rec in self:
            rec.net_weight = (rec.gross_weight or 0.0) - (rec.tare_weight or 0.0)

    @api.onchange('winegrower_id')
    def _onchange_winegrower_id(self):
        if self.winegrower_id:
            self.plot_id = False
            return {
                'domain': {
                    'plot_id': [('winegrower_id', '=', self.winegrower_id.id)]
                }
            }
        else:
            self.plot_id = False
            return {
                'domain': {
                    'plot_id': [('id', '=', False)]
                }
            }

