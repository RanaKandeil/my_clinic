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

class ReferralDoctors(models.Model):
    _name = "clinic.referraldoctors"
    _description = "Referral Doctors"

    doctor_name = fields.Char(string="Doctor Name", required=True)

class ConsumableProduct(models.Model):
    _name = "clinic.consumables"
    _description = "Consumable"

    name = fields.Char(string="Product Name", required=True)
    description = fields.Char(string="Product Description", required=True)
    company = fields.Char(string="Company Name", required=True)

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'This product already exists !')
    ]

    def name_get(self):
        res = []
        for rec in self:
            if rec.name:
                res.append((rec.id, '%s - %s' % (rec.name, rec.company)))
            else:
                res.append((rec.id, '%s - %s' % (rec.name, '')))
        return res

class AppointmentConsumables(models.Model):
    _name = "clinic.appointmentconsumable"
    _description = "Consumables"

    consumable_id = fields.Many2one('clinic.consumables', string="Consumable")
    appointment_id = fields.Many2one('clinic.appointment', String="Appointment Id")
    quantity = fields.Integer(string='Quantity', required=True)


class RequiredSurgery(models.Model):
    _name = "clinic.reqsurgery"
    _description = "reqsurgery"

    name = fields.Char(string="Surgery Name", required=True)