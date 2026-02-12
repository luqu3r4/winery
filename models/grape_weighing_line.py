# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GrapeWeighingLine(models.Model):
    _name = 'winery.grape.weighing.line'
    _description = 'Linea de Pesada'

    weighing_id = fields.Many2one('winery.grape.weighing', ondelete='cascade')
    
    # Campo que faltaba y causaba el error
    datetime = fields.Datetime(string="Fecha", default=fields.Datetime.now)
    
    winegrower_id = fields.Many2one('winery.winegrower', string="Viticultor")
    plot_id = fields.Many2one('winery.plot', string="Parcela")
    grape_variety_id = fields.Many2one('winery.grape_variety', string="Variedad")
    
    table_wine = fields.Boolean(string="Vino Mesa")
    alcohol_degree = fields.Float(string="Grado")
    
    gross_weight = fields.Float(string="Bruto")
    tare_weight = fields.Float(string="Tara")
    net_weight = fields.Float(string="Neto", compute='_compute_net_weight', store=True)

    @api.depends('gross_weight', 'tare_weight')
    def _compute_net_weight(self):
        for rec in self:
            rec.net_weight = (rec.gross_weight or 0.0) - (rec.tare_weight or 0.0)