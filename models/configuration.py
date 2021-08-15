from odoo import api, fields, models

class AppointmentType(models.Model):
    _name = "clinic.appointmenttype"
    _description = "AppointmentType"

    name = fields.Char(string="Appointment Type", required=True)
    price = fields.Float(string="Price", required=True)