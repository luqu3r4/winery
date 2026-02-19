# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DepositType(models.Model):
    _name = 'winery.deposit_type'
    _description = 'Tipo de Deposito'

    name = fields.Char(string='Nombre', required = True)
    code = fields.Char(string='Código interno', required=True)

    material = fields.Char(string='Material', required=True)
    default_capacity = fields.Float(
        string='Capacidad por defecto (L)', required=True
    )
    default_tolerance = fields.Float(
        string='Tolerancia por defecto (%)', required=True
    )

    state = fields.Selection([
        ('active', 'Activo'),
        ('inactive', 'Inactivo')
    ], string='Estado', default='active', required=True)
    description = fields.Text(string='Descripción adicional')

    deposit_ids = fields.One2many(
        'winery.deposit', 
        'depositType_id', 
        string="Depósitos reales"
    )
