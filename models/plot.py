# -*- coding: utf-8 -*-

from odoo import models, fields, api

class plot(models.Model):
    _name = 'winery.plot'
    _description = 'Parcelas de la bodega'

    # Campos básicos
    name = fields.Char(string='Nombre', compute='_compute_name', store=True)
    plot_number = fields.Char(string='Número de Parcela')
    cadastral_ref = fields.Char(string='Referencia Catastral')
    
    # Ubicación Geográfica
    city = fields.Char(string='Ciudad/Municipio')
    gps_coords = fields.Char(string='Coordenadas GPS')
    
    # Relaciones (Foreign Keys)
    country_id = fields.Many2one('res.country', string='País', default=68)
    state_id = fields.Many2one('res.country.state', string='Provincia/Estado', default=427)
    
    # Datos Agrícolas
    area_ha = fields.Float(string='Área (Ha)', digits=(10, 2))
    
    # Relaciones específicas del negocio (Ajusta los modelos 'comodel_name' según tu código real)
    grape_variety_id = fields.Many2one('winery.grape_variety', string='Variedad de Uva')
    winegrower_id = fields.Many2one('winery.winegrower', string='Viticultor')
    
    # Otros detalles
    aggregation = fields.Char(string='Agregación', required=True)
    zone = fields.Char(string='Zona')
    
    # Campos de texto largo
    sigpac_info = fields.Text(string='Información SIGPAC')
    description = fields.Text(string='Descripción')

    # Estado
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('active', 'Activo'),
        ('archived', 'Archivado')
    ], string='Estado', default='draft')
    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False
        return {
            'domain': {
                'state_id': [('country_id', '=', self.country_id.id)]
            }
        } 
    
    @api.depends('plot_number', 'state_id','aggregation','grape_variety_id')
    def _compute_name(self):
        for rec in self:
            parts = [
                f"Nº {rec.plot_number}" if rec.plot_number else None,
                rec.state_id.name if rec.state_id else None,
                rec.aggregation,
                rec.grape_variety_id.name,
            ]
            rec.name = ' - '.join(filter(None, parts))



