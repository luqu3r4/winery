# -*- coding: utf-8 -*-

from odoo import models, fields, api


class GrapeWeighing(models.Model):
    _name = 'winery.grape.weighing'
    _description = 'Modelo de pesada'

    # El campo id no es necesario; Odoo lo crea automáticamente
    name = fields.Char(string="Referencia")
    datetime = fields.Datetime(string="Fecha y Hora")

    winegrower_id = fields.Many2one('winery.winegrower', required=True, string="Viticultor")
    winegrower_code = fields.Char(string="Código Viticultor", compute='_compute_winegrower_code', store=True)

    grape_variety_id = fields.Many2one('winery.grape_variety', required=True, string="Variedad de Uva")
    plot_id = fields.Many2one('winery.plot', string="Parcela")

    table_wine = fields.Boolean(string="Vino de Mesa")
    alcohol_degree = fields.Float(string="Grado Alcohólico", digits=(5, 2))

    gross_weight = fields.Float(string="Peso Bruto", digits=(10, 2))
    tare_weight = fields.Float(string="Peso Tara", digits=(10, 2))
    net_weight = fields.Float(string="Peso Neto", compute='_compute_net_weight', store=True, digits=(10, 2))

    notes = fields.Text(string="Notas")

    @api.depends('winegrower_id')
    def _compute_winegrower_code(self):
        for record in self:
            record.winegrower_code = record.winegrower_id.code if record.winegrower_id else ''

    @api.depends('gross_weight', 'tare_weight')
    def _compute_net_weight(self):
        for record in self:
            record.net_weight = (record.gross_weight or 0.0) - (record.tare_weight or 0.0)
