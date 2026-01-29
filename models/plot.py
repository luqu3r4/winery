# -*- coding: utf-8 -*-
from odoo import models, fields, api

class Plot(models.Model): # Por convención, las clases empiezan en mayúscula
    _name = 'winery.plot'
    _description = 'Parcelas de la bodega'

    # 1. Identificación: El nombre debe ser calculado y no editable manualmente
    name = fields.Char(string='Nombre', store=True)
    plot_number = fields.Char(string='Número de Parcela')
    cadastral_ref = fields.Char(string='Referencia Catastral')
    
    # 2. Localización
    city = fields.Char(string='Localidad')
    gps_coords = fields.Char(string='Coordenadas GPS')
    country_id = fields.Many2one('res.country', string='País', default=68)
    state_id = fields.Many2one('res.country.state', string='Provincia', default=427)
    
    # 3. Datos Agrícolas (Superficie en hectáreas)
    # Usamos area_ha para el cálculo del Viticultor
    area_ha = fields.Float(string='Superficie (Ha)', digits=(10, 2))
    
    # 4. Relaciones
    # grape_variety_id debe ser Many2one o Many2many según el negocio. La práctica dice "variedad o variedades".
    grape_variety_id = fields.Many2one('winery.grape_variety', string='Variedad de Uva')
    winegrower_id = fields.Many2one('winery.winegrower', string='Viticultor', required=True)
    
    aggregation = fields.Char(string='Agregado', required=True)
    zone = fields.Char(string='Zona')
    sigpac_info = fields.Text(string='Información SIGPAC')
    description = fields.Text(string='Descripción libre')

    # 5. Estado de la parcela
    state = fields.Selection([
        ('active', 'Activa'),
        ('inactive', 'Inactiva'),
        ('suspended', 'Suspendida')
    ], string='Estado', default='active')

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False
        return {
            'domain': {
                'state_id': [('country_id', '=', self.country_id.id)]
            }
        }
    
    @api.depends('plot_number', 'state_id', 'aggregation', 'grape_variety_id')
    def _compute_name(self):
        for rec in self:
            # Obtenemos el nombre de la variedad si existe
            variety_name = rec.grape_variety_id.name if rec.grape_variety_id else None
            parts = [
                f"Nº {rec.plot_number}" if rec.plot_number else None,
                rec.state_id.name if rec.state_id else None,
                rec.aggregation,
                variety_name,
            ]
            rec.name = ' - '.join(filter(None, parts))



