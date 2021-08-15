from odoo import api, fields, models


class Imaging(models.Model):
    _name = "clinic.imaging"
    _description = "Imaging"

    name = fields.Char(string="Imaging name", required=True)
    prerequisites = fields.Char(string="Prerequisites")
    code = fields.Char(string="Code")
    service = fields.Char(string="Service")
    type = fields.Char(string="Type")
