from odoo import api, fields, models , _
from datetime import date, datetime

class ClinicPatient(models.Model):
    _name = "hospital.patient"
    _description = "Clinic Patient"


class ClinicPatient(models.Model):
    _name = "clinic.patient"
    _description = "Clinic Patient"

    name = fields.Char(string='Name', required=True)
    age = fields.Char(string='Age')
    marital_status = fields.Selection([
        ('single', 'Single'),
        ('married', 'Married'),
        ('divorced', 'Divorced'),
        ('widow', 'Widow'),
    ], default='single',string="Marital Status")
    smoking = fields.Boolean(string="Smoking",default=False)
    profession = fields.Char(string="Profession")
    referral_ads = fields.Selection([
        ('fb', 'Facebook'),
        ('instgram', 'Instgram'),
        ('google', 'Google'),
    ])
    referral_drs_id = fields.Many2one('clinic.referraldoctors', string="Referral Doctors")
    referral_patients_id = fields.Many2one('clinic.patient', string="Referral Patients")
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
    behavior = fields.Selection([
        ('good', 'Good'),
        ('trouble_maker', 'Trouble Maker'),
        ('blocked', 'Blocked'),
    ], default='good')
    insurance = fields.Char(string="Insurance")
    address = fields.Char(string="Address")
    phoneNumber = fields.Char(string='Phone Number', required=True)

    note = fields.Text(string='Notes')
    appointment_ids = fields.One2many('clinic.appointment','patient_id',string='My Appointments')


    def open_patient_graph(self):
        print(self.name == 'Patient1')
        print(self.appointment_ids.patient_id.id)
        return {
            'name': _('BMI'),
            'domain': [('patient_id.id', '=', self.id)],
            'view_type': 'graph',
            'res_model': 'clinic.appointment',
            'view_id': self.env.ref('my_clinic.patient_appointment_graph').id,
            'view_mode': 'graph',
            'type': 'ir.actions.act_window',
            # 'context': self.env.context,
        }

    @api.onchange('dateOfBirth')
    def onchange_dateOfBirth(self):
        if self.dateOfBirth:
            self.age = date.today().year - self.dateOfBirth.year
        else:
            self.age = 0


