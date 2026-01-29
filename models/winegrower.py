# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Winegrower(models.Model):
    _name = 'winery.winegrower'
    _description = 'Model of winegrower creator.'

    id = fields.Integer(required = True)
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

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if self.state_id and self.state_id.country_id != self.country_id:
            self.state_id = False
        return {
            'domain': {
                'state_id': [('country_id', '=', self.country_id.id)]
            }
        }