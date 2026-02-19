# -*- coding: utf-8 -*-

from odoo import models, fields, api


class DepositType(models.Model):
    _name = 'winery.deposit_type'
    _description = 'Tipo de Deposito'

    name = fields.Char(string='Name', required = True)
    code = fields.Char(string='Internal Code', required=True)

    material = fields.Char(string='Material', required=True)
    default_capacity = fields.Float(
        string='Default Capacity (L)', required=True
    )
    default_tolerance = fields.Float(
        string='Default Tolerance (%)', required=True
    )

    active = fields.Boolean(string='Active')
    description = fields.Text(string='Description or Observations')

    deposit_ids = fields.One2many(
        'winery.deposit', 
        'depositType_id', 
        string="Depósitos reales"
    )
