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

class Insurance(models.Model):
    _name = "clinic.insurance"
    _description = "Insurance"

    name = fields.Char(string="Insurance", required=True)
    price = fields.Char(string="Price",default='50')
class ReferralDoctors(models.Model):
    _name = "clinic.referraldoctors"
    _description = "Referral Doctors"

    name = fields.Char(string="Doctor Name", required=True)



class RequiredSurgery(models.Model):
    _name = "clinic.reqsurgery"
    _description = "reqsurgery"

    name = fields.Char(string="Surgery Name", required=True)

class Doctor(models.Model):
    _name = "clinic.doctor"
    _description = "doctor"
    _sql_constraints = [('doctor_user_presence_unique', 'unique(user_id)', 'A user can be assigned to one doctor only.')]

    name = fields.Char(string="Doctor Name", required=True)
    user_id = fields.Many2one('res.users', 'User', required=True, index=True, ondelete='cascade')
    specialty = fields.Char(string="Specialty")
    faculty = fields.Char(string="Faculty")
    masters = fields.Char(string="Masters")
    PHD = fields.Char(string="PHD")