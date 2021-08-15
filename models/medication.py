from odoo import api, fields, models


class Medication(models.Model):
    _name = "clinic.medication"
    _description = "Medication"

    name = fields.Char(string="Medication name", required=True)
    indication = fields.Char(string="Indication")
    dose = fields.Char(string="Dose")
    frequency = fields.Char(string="Frequency")
    prescription_id = fields.Many2one('clinic.appointment', string="Prescription")

class Prescription(models.Model):
    _name = "clinic.prescription"
    _description = "Prescription"

    name = fields.Char(string="Prescription name", required=True)
    medication_ids = fields.Many2many('clinic.medication', 'prescription_medication_rel', 'prescription_id',
                                      'medication_id', string='Medications')