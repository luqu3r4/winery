# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Winegrower(models.Model):
    _name = 'winery.winegrower'
    _description = 'Model of winegrower creator.'

    name = fields.Char(string = "Nombre")
    nif = fields.Char(required = True, string = "NIF/CIF")
    code = fields.Char(required = True, string = "Código")
    street = fields.Char(string = "Calle")
    city = fields.Char(string = "Localidad")
    state_id = fields.Many2one('res.country.state', required = True, string = "Provincia", default=427)
    country_id = fields.Many2one('res.country', required = True, string = "País", default=68)
    zip = fields.Char(string = "Código Postal")
    phone = fields.Char(required = True, string = "Teléfono")
    email = fields.Char(string = "Correo")
    notes = fields.Text(string = "Notas")
    plot_id = fields.One2many('winery.plot', 'winegrower_id', string="Parcelas")
    typeOf = fields.Selection(selection=[('Pequeño', 'Pequeño'), ('Mediano', 'Mediano'), ('Grande', 'Grande')], string = "Tamaño del viticultor.")

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False
        return {
            'domain': {
                'state_id': [('country_id', '=', self.country_id.id)]
            }
        }
   
    @api.depends('plot_id.area_ha')
    def _depends_typeOf(self):
        sumaTotal = 0
        for parcela in self:
            sumaTotal += parcela.plot_id.area_ha
 
        if (sumaTotal < 5):
            self.typeOf = "Pequeño"
        elif (sumaTotal < 20):
            self.typeOf = "Mediano"
        else:
            self.typeOf = "Grande"