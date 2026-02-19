# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Deposit(models.Model):
    _name = 'winery.deposit'
    _description = 'Depositos'

    name = fields.Char(string="Nombre del depósito", required=True)
    code = fields.Char(string="Código del depósito", required=True)

    depositType_id = fields.Many2one("winery.deposit_type", string="Tipo de depósito", required=True)

    sizeCapacity = fields.Integer(string="Capacidad", required=True)
    tolerance = fields.Integer(string="Tolerancia", required=True)
    
    maxCapacity = fields.Float(string="Capacidad máxima calculada")

    state = fields.Selection([
            ('active', 'Activo'),
            ('inactive', 'Inactivo'),
            ('in_maintenance', 'En mantenimiento')
        ], string='Estado', default='active')

    currentLitres = fields.Float(string="Litros actuales", required=True)
    
    percentageLitres = fields.Float(string="Porcentaje de llenado", required=True)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'El código del depósito debe ser único.')
    ]

    @api.onchange('sizeCapacity', 'tolerance')
    def _onchange_maxCapacity(self):
        for record in self:
            record.maxCapacity = record.sizeCapacity + (record.sizeCapacity * record.tolerance / 100.0)

    @api.onchange('currentLitres', 'sizeCapacity')
    def _onchange_percentageLitres(self):
        for record in self:
            if record.sizeCapacity > 0:
                record.percentageLitres = (record.currentLitres * 100.0) / record.sizeCapacity
            else:
                record.percentageLitres = 0.0