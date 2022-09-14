from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'
    _description = 'New Description'

    is_direksi = fields.Boolean(string='Is Direksi')