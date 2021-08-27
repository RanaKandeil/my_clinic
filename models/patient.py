from odoo import api, fields, models
from datetime import date, datetime

class ClinicPatient(models.Model):
    _name = "hospital.patient"
    _description = "Clinic Patient"


class ClinicPatient(models.Model):
    _name = "clinic.patient"
    _description = "Clinic Patient"

    name = fields.Char(string='Name', required=True)
    age = fields.Char(string='Age')
    maretial_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widow', 'Widow'),
    ], default='single')
    smoking = fields.Boolean(string="Smoking",default=False)
    profession = fields.Char(string="Profession")
    referal_ads = fields.Selection([
        ('fb', 'Facebook'),
        ('instgram', 'Instgram'),
        ('google', 'Google'),
    ])
    referal_drs_id = fields.Many2one('clinic.referaldoctors', string="Referal Doctors")
    referal_patients_id = fields.Many2one('clinic.patient', string="Referal Patients")
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

    @api.onchange('dateOfBirth')
    def onchange_dateOfBirth(self):
        if self.dateOfBirth:
            self.age = date.today().year - self.dateOfBirth.year
        else:
            self.age = 0


