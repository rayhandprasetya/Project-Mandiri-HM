from odoo import api, fields, models


class Karyawan(models.Model):
    _name = 'kostan.karyawan'
    _description = 'New Description'

    name = fields.Char(string='Nama', required=True)
    gender = fields.Selection([
        ('lakilaki', 'Laki-laki'), ('perempuan', 'Perempuan')
    ], string='Gender', required=True)
    alamat = fields.Char(string='Alamat', required=True)
    no_telp = fields.Char(string='No. Telp', required=True)
    
    karyawan_id = fields.Many2many(comodel_name='kostan.tipe', string = 'Unit yang dijaga')
