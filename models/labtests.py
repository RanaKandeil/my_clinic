from odoo import api, fields, models


class Labtest(models.Model):
    _name = "clinic.labtest"
    _description = "Labtest"

    name = fields.Char(string="Lab Test name", required=True)
    prerequisites = fields.Char(string="Prerequisites")
    code = fields.Char(string="Code")
