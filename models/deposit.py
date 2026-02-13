# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Deposit(models.Model):
    _name = 'winery.deposit'
    _description = 'Depositos'

    name = fields.Char(string="Nombre del depósito", required=True)
    code = fields.Char(string="Código del depósito", required=True)

    # CORRECCIÓN 1: Many2one con 'o' minúscula
    depositType_id = fields.Many2one("winery.deposit_type", string="Tipo de depósito", required=True)

    # Corrección de un pequeño typo en el string: "Capacida" -> "Capacidad"
    sizeCapacity = fields.Integer(string="Capacidad", required=True)
    tolerance = fields.Integer(string="Tolerancia", required=True)
    
    # CORRECCIÓN 2: Eliminado el argumento posicional extra
    maxCapacity = fields.Float(string="Capacidad máxima calculada")

    state = fields.Selection([
            ('active', 'Activo'),
            ('inactive', 'Inactivo'),
            ('in_maintenance', 'En mantenimiento')
        ], string='Estado', default='active')

    currentLitres = fields.Float(string="Litros actuales", required=True)
    
    # CORRECCIÓN 3: Cambiado 'requires' por 'required'
    percentageLitres = fields.Float(string="Porcentaje de llenado", required=True)

    _sql_constraints = [
        ('code_unique', 'UNIQUE(code)', 'El código del depósito debe ser único.')
    ]

    # CORRECCIÓN 4: El onchange se dispara al cambiar la capacidad o la tolerancia
    @api.onchange('sizeCapacity', 'tolerance')
    def _onchange_maxCapacity(self):
        for record in self:
            record.maxCapacity = record.sizeCapacity + (record.sizeCapacity * record.tolerance / 100.0)

    # CORRECCIÓN 5: Nombre de función único y protección contra división por cero
    @api.onchange('currentLitres', 'sizeCapacity')
    def _onchange_percentageLitres(self):
        for record in self:
            if record.sizeCapacity > 0:
                record.percentageLitres = (record.currentLitres * 100.0) / record.sizeCapacity
            else:
                record.percentageLitres = 0.0