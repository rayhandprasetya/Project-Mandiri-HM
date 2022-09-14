from genericpath import exists
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools.misc import unique


class Transaksi(models.Model):
    _name = 'kostan.transaksi'
    _description = 'New Description'

    nama_penyewa = fields.Char(string='Nama Penyewa', required=True)
    nik = fields.Char(string='NIK', required=True)
    tgl_sewa = fields.Datetime(string='Mulai Sewa', required=True)
    total_bayar = fields.Integer(compute='_compute_totalbayar', string='Total Pembayaran')
    transaksiorder_ids = fields.One2many(comodel_name='kostan.transaksiorder', inverse_name='transaksi_id', string='Detail Transaksi')

    state = fields.Selection(string='Status', selection=[('draft', 'Draft'),
                                                                        ('confirm', 'Confirm'),
                                                                        ('done', 'Done'),
                                                                        ('cancel', 'Cancel')], required=True, readonly=True, default='draft')

    def action_confirm(self):
        self.write({'state': 'confirm'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})

    @api.depends('transaksiorder_ids')
    def _compute_totalbayar(self):
        for rec in self:
            a = sum(self.env['kostan.transaksiorder'].search([('transaksi_id', '=', rec.id)]).mapped('subtotal'))
            rec.total_bayar = a

    #untuk odoo 14 dan 15
    def unlink(self):
        if self.filtered(lambda line: line.state != 'draft'):
            raise ValidationError("Status draft tidak bisa dihapus")
        if self.transaksiorder_ids:
            a = []
            for rec in self:
                a = self.env['kostan.transaksiorder'].search([('transaksi_id', '=', rec.id)])
                print(a)
            for ob in a:
                print(ob.barang_id.name + ' ' + str(ob.jmlh_kamar))
                ob.barang_id.stok += ob.jmlh_kamar
        record = super(Transaksi,self).unlink()

    _sql_constraints = [
        ('no_nik', 'unique (nik)', 'NIK sudah terdaftar')
    ]

    def write(self,vals):
        for rec in self:
            a = self.env['kostan.transaksiorder'].search([('transaksi_id', '=', rec.id)])
            print(a)
            for data in a:
                print(str(data.barang_id.name) + ' ' + str(data.jmlh_kamar) + ' ' + str(data.barang_id.stok))
                data.barang_id.stok += data.jmlh_kamar
        record = super(Transaksi,self).write(vals)

        for rec in self:
            b = self.env['kostan.transaksiorder'].search([('transaksi_id', '=', rec.id)])
            print(a)
            print(b)
            for databaru in b:  
                if databaru in a:
                    print(str(databaru.barang_id.name) + ' ' + str(databaru.jmlh_kamar) + ' ' + str(databaru.barang_id.stok))
                    databaru.barang_id.stok -= databaru.jmlh_kamar
                else:       
                    pass
        return record

class TransaksiOrder(models.Model):    
    _name = 'kostan.transaksiorder'
    _description = 'New Description'

    name = fields.Char(string='Nama')
    transaksi_id = fields.Many2one(comodel_name='kostan.transaksi', string='Detail Transaksi')
    barang_id = fields.Many2one(comodel_name='kostan.tipe', string='List Kost')
    harga_sewa = fields.Integer(string='Harga Sewa (1 Bulan)')
    jmlh_kamar = fields.Integer(string='Jumlah Kamar')

    subtotal = fields.Integer(compute='_compute_subtotal', string='Subtotal')

    @api.depends('harga_sewa', 'jmlh_kamar')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = rec.jmlh_kamar * rec.harga_sewa


    @api.onchange('barang_id')
    def _onchange_barang_id(self):  
        if (self.barang_id.harga):
            self.harga_sewa = self.barang_id.harga

    @api.model
    def create(self, vals):
        record = super(TransaksiOrder,self).create(vals)
        if record.jmlh_kamar:
            self.env['kostan.tipe'].search([('id', '=', record.barang_id.id)]).write({'stok': record.barang_id.stok - record.jmlh_kamar})
        return record
    
    
    @api.constrains('jmlh_kamar')
    def check_quantity(self):
        for rec in self:
            if rec.jmlh_kamar < 1:
                raise ValidationError('Quantity tidak boleh kosong')
            elif rec.barang_id.stok < rec.jmlh_kamar:
                raise ValidationError('Stok {} tidak mencukupi, hanya tersedia {}'.format(rec.barang_id.name, rec.barang_id.stok))
    
    # _sql_constraints = [
    #     ('durasi_stok', 'CHECK (jmlh_kamar > 1)', 'Quantity tidak boleh kosong')
    # ]   