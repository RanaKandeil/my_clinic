from odoo import api, fields, models

class ClinicPatient(models.Model):
    _name = "hospital.patient"
    _description = "Clinic Patient"


class ClinicPatient(models.Model):
    _name = "clinic.patient"
    _description = "Clinic Patient"

    name = fields.Char(string='Name', required=True)
    age = fields.Integer(string='Age')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
    ], required=True, default='male')
    dateOfBirth = fields.Date(string='Date Of Birth', required=True)
    bloodType = fields.Char(string='Blood Type')
    RH = fields.Selection([
        ('positive', '+ve'),
        ('negative', '-ve'),
    ])
    insurance = fields.Char(string="Insurance")
    address = fields.Char(string="Address")
    phoneNumber = fields.Char(string='Phone Number', required=True)

    note = fields.Text(string='Notes')
    appointment_ids = fields.One2many('clinic.appointment','patient_id',string='My Appointments')