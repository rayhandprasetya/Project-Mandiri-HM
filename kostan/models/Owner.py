from odoo import api, fields, models


class Owner(models.Model):
    _inherit = 'res.partner'
    _description = 'Contact'

    is_owner = fields.Boolean(string='Is Owner')