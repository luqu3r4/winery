# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GrapeWeighingLine(models.Model):
    _name = 'winery.grape.weighing.line'
    _description = 'Líneas de Pesada de Uva'

    name = fields.Char(string="Referencia", required=True)
    datetime = fields.Datetime(string="Fecha y Hora", required=True)
    
    winegrower_id = fields.Many2one('winery.winegrower', string="Viticultor", required=True)
    winegrower_code = fields.Char(string="Nº Viticultor", compute='_compute_winegrower_code', store=True, readonly=True)

    # Campo Many2one normal para seleccionar una parcela
    plot_id = fields.Many2one('winery.plot', string="Parcela")

    table_wine = fields.Boolean(string="¿Vino de mesa?")
    grape_variety_id = fields.Many2one('winery.grape.variety', string="Variedad de Uva")
    alcohol_degree = fields.Float(string="Graduación", digits=(5,2))

    gross_weight = fields.Float(string="Peso Bruto", digits=(10,2))
    tare_weight = fields.Float(string="Peso Tara", digits=(10,2))
    net_weight = fields.Float(string="Peso Neto", compute='_compute_net_weight', store=True, digits=(10,2))

    notes = fields.Text(string="Descripción")

    weighing_id = fields.Many2one('winery.grape.weighing', string="Pesada")  # Relación con la cabecera

    @api.depends('winegrower_id')
    def _compute_winegrower_code(self):
        for record in self:
            record.winegrower_code = record.winegrower_id.code if record.winegrower_id else ''

    @api.depends('gross_weight', 'tare_weight')
    def _compute_net_weight(self):
        for record in self:
            record.net_weight = (record.gross_weight or 0.0) - (record.tare_weight or 0.0)

    @api.onchange('winegrower_id')
    def _onchange_winegrower_id(self):
        # Filtra parcelas solo del viticultor seleccionado
        if self.winegrower_id:
            return {'domain': {'plot_id': [('winegrower_id', '=', self.winegrower_id.id)]}}
        # Si no hay viticultor, no mostrar ninguna parcela
        return {'domain': {'plot_id': [('id', '=', False)]}}
