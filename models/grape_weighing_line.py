# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GrapeWeighingLine(models.Model):
    _name = 'winery.grape.weighing.line'
    _description = 'Líneas de Pesada de Uva'

    name = fields.Char(string="Referencia")
    datetime = fields.Datetime(string="Fecha y Hora")
    winegrower_id = fields.Many2one('winery.winegrower', string="Viticultor")
    grape_variety_id = fields.Many2one('winery.grape.variety', string="Variedad de Uva")
    plot_id = fields.Many2one('winery.plot', string="Parcela")
    gross_weight = fields.Float(string="Peso Bruto", digits=(10,2))
    tare_weight = fields.Float(string="Peso Tara", digits=(10,2))
    net_weight = fields.Float(string="Peso Neto", compute='_compute_net_weight', store=True, digits=(10,2))
    alcohol_degree = fields.Float(string="Grado Alcohólico", digits=(5,2))

    weighing_id = fields.Many2one('winery.grape.weighing', string="Pesada")  # Relación Many2one

    @api.depends('gross_weight', 'tare_weight')
    def _compute_net_weight(self):
        for record in self:
            record.net_weight = (record.gross_weight or 0.0) - (record.tare_weight or 0.0)
