# -*- coding: utf-8 -*-
from odoo import models, fields, api


class GrapeVariety(models.Model):
    _name = 'winery.grape_variety'
    _description = 'Tipo de Uva'

    name = fields.Char(string="Nombre de la variedad de uva", required=True)

    color = fields.Selection(
        [
            ('tinto', 'Tinto'),
            ('blanco', 'Blanco'),
            ('rosado', 'Rosado'),
        ],
        string="Clasificación visual de la uva",
        required=True)
    
    origin_region_id = fields.Many2one(comodel_name = 'res.country.state', string = "Región de origen de la uva")
    is_seedless = fields.Boolean(string="Indica si es una variedad sin pepitas")
    acidity_level = fields.Float(string="Nivel aproximado de acidez (0-10)")
    notes = fields.Text(string="Información adicional")