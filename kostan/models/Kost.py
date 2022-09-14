from dataclasses import field
from odoo import api, fields, models


class TipeKos(models.Model):
    _name = 'kostan.tipe'
    _description = 'New Description'

    name = fields.Selection([
        ('tipea', 'Tipe A'), ('tipeb', 'Tipe B'), ('tipec', 'Tipe C')
    ], string='Tipe Kost', required=True)
    harga = fields.Integer(string='Harga',required=True)
    
    karyawan_id = fields.Many2many(comodel_name='kostan.karyawan', string='Penjaga')
    stok = fields.Integer(string='Stok', required=True)