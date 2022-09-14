from odoo import models, fields


class PartnerXlsx(models.AbstractModel):
    _name = 'report.kostan.report_transaksi_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    tgl_lap = fields.Date.today()

    def generate_xlsx_report(self, workbook, data, supplier):
        sheet = workbook.add_worksheet('Daftar Penjualan')
        bold = workbook.add_format({'bold': True})
        sheet.write(0, 0, str(self.tgl_lap))
        sheet.write(1, 0, 'nama_penyewa')
        sheet.write(1, 1, 'nik')
        sheet.write(1, 2, 'tgl_sewa')
        sheet.write(1, 3, 'total_bayar')
        row = 2
        col = 0
        for obj in supplier:
            col = 0
            date_style = workbook.add_format({'text_wrap': True, 'num_format': 'dd-mm-yyyy'})
            sheet.write(row, col, obj.nama_penyewa)
            sheet.write(row, col+1, obj.nik)
            sheet.write(row, col+2, obj.tgl_sewa, date_style)
            sheet.write(row, col+3, obj.total_bayar)