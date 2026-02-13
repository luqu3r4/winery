# -*- coding: utf-8 -*-
from odoo import models, fields, api

class GrapeWeighing(models.Model):
    _name = 'winery.grape.weighing'
    _description = 'Pesadas de Uva'

    name = fields.Char(string="Referencia", required=True)
    state = fields.Selection([('draft', 'Borrador'), ('confirmed', 'Confirmada')], default='draft')
    entry_datetime = fields.Datetime(string="Fecha", default=fields.Datetime.now)
    
    winegrower_id = fields.Many2one('winery.winegrower', string="Viticultor")
    winegrower_code = fields.Char(related='winegrower_id.code', readonly=True)
    
    gross_weight = fields.Float(string="Bruto")
    tare_weight = fields.Float(string="Tara")
    net_weight = fields.Float(string="Neto", compute='_compute_net_weight', store=True)
    alcohol_degree = fields.Float(string="Grado")
    
    weighing_line_ids = fields.One2many('winery.grape.weighing.line', 'weighing_id', string="Líneas")
    description = fields.Text(string="Notas")

    @api.depends('gross_weight', 'tare_weight')
    def _compute_net_weight(self):
        for rec in self:
            rec.net_weight = (rec.gross_weight or 0.0) - (rec.tare_weight or 0.0)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_cancel(self):
        self.write({'state': 'draft'})