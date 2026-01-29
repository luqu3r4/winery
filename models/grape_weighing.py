# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GrapeWeighing(models.Model):
    _name = 'winery.grape.weighing'
    _description = 'Pesadas de Uva'

    name = fields.Char(string="Referencia", required=True)
    datetime = fields.Datetime(string="Fecha", required=True)
    alcohol_degree = fields.Float(string="Grado Alcohólico", digits=(5,2))
    gross_weight = fields.Float(string="Peso Bruto", digits=(10,2))
    tare_weight = fields.Float(string="Peso Tara", digits=(10,2))
    net_weight = fields.Float(string="Peso Neto", compute='_compute_net_weight', store=True, digits=(10,2))

    # One2many hacia las líneas
    line_ids = fields.One2many(
        'winery.grape.weighing.line', 
        'weighing_id', 
        string="Líneas de Pesada"
    )

    @api.depends('gross_weight', 'tare_weight')
    def _compute_net_weight(self):
        for rec in self:
            rec.net_weight = (rec.gross_weight or 0.0) - (rec.tare_weight or 0.0)
