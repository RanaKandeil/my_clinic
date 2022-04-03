from odoo import api, fields, models , _ , SUPERUSER_ID
from datetime import date, datetime
import json
class ClinicPatient(models.Model):
    _name = "hospital.patient"
    _description = "Clinic Patient"


class ClinicPatient(models.Model):
    _name = "clinic.patient"
    _description = "Clinic Patient"

    @api.model
    def _default_user(self):
        return self.env.context.get('user_id', self.env.user.id)

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
    appointment_ids = fields.One2many('clinic.appointment', 'patient_id',
                                       domain=lambda self: [ ('doctor_id.user_id.id', '=', self.env.user.id)],
                                      string='My Appointments')
    labTest_ids = fields.One2many('clinic.labtestresults', 'patient_id',
                                      # domain=lambda self: [('doctor_id.user_id.id', '=', self.env.user.id)],
                                      string='My LAbtests')
    # medication_Prescrption_ids = fields.One2many(related='appointment_ids.medication_Prescrption_ids')
    # @api.multi
    # @api.depends('current_user')
    # def _compute_appointment_ids_domain(self):
    #     for rec in self:
    #         print(rec.current_user.name)
    #        #  rec.appointment_ids_domain = json.dumps(
    #        #     [('type', '=', 'product'), ('name', 'like', rec.name)]
    #        # )

    # @api.depends('price')
    # def _compute_my_appointments(self):
    #     print(self.dateOfBirth)
        # for app in self.filtered(lambda p: p.my_appointments):
        #     print('ALOOOOOOOOOOOOO')
        #     print(self.current_user.name)
        #     self.my_appointments = self.my_appointments.filtered(
        #         lambda app: app.doctor_id.user_id.name == self.env.user.name)
        #     print(self.my_appointments)
        #     return self.my_appointments


    def open_patient_graph(self):
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
