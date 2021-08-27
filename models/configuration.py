from odoo import api, fields, models

class AppointmentType(models.Model):
    _name = "clinic.appointmenttype"
    _description = "AppointmentType"


    name = fields.Char(string="Appointment Type", required=True)
    price = fields.Float(string="Price", required=True)
    hospital = fields.Many2one('clinic.hospital', string="Hospital")

    def name_get(self):
        res = []
        for rec in self:
            if rec.hospital.name:
                res.append((rec.id, '%s - %s' % (rec.name, rec.hospital.name)))
            else:
                res.append((rec.id, '%s - %s' % (rec.name, 'Clinic')))
        return res

class Hospital(models.Model):
    _name = "clinic.hospital"
    _description = "Hospital"

    name = fields.Char(string="Hospital Name", required=True)

class ReferalDoctors(models.Model):
    _name = "clinic.referaldoctors"
    _description = "Referal Doctors"

    doctor_name = fields.Char(string="Doctor Name", required=True)