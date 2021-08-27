from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class Medication(models.Model):
    _name = "clinic.medication"
    _description = "Medication"

    name = fields.Char(string="Medication name", required=True)
    therapeuticeffect = fields.Char(string="Therapeutic Effect")
    activecomponent = fields.Char(string="Active Component")
    prescription_id = fields.Many2one('clinic.appointment', string="Prescription")

    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'This medication already exists !')
    ]

class Prescription(models.Model):
    _name = "clinic.prescription"
    _description = "Prescription"

    name = fields.Char(string="Prescription name", required=True)
    presc_med_ids = fields.One2many('clinic.medicationpresc', 'prescription_id', string='Prescription Medications')



class AppointmentPrescription(models.Model):
    _name = "clinic.medicationpresc"
    _description = "Appointment Prescription"

    appointment_id = fields.Many2one('clinic.appointment', String = "Appointment Id")
    prescription_id = fields.Many2one('clinic.prescription', String="Prescription Id")
    medicament_id = fields.Many2one('clinic.medication', string="Medicament")
    concentration = fields.Many2one('clinic.concentration', string='Concentration')
    doasge_form = fields.Many2one('clinic.dosageform', string='Dosage Form')
    frequency = fields.Many2one('clinic.frequency', string='Frequency')
    duration = fields.Many2one('clinic.duration', string='Duration')
    note = fields.Char(string='Note')

class Concentration(models.Model):
    _name = "clinic.concentration"
    _description = "Concentration"

    name = fields.Char(string="Concentration", required=True)


class Dosageform(models.Model):
    _name = "clinic.dosageform"
    _description = "Dosageform"

    name = fields.Char(string="Dosage Form", required=True)


class Frequency(models.Model):
    _name = "clinic.frequency"
    _description = "Frequency"

    name = fields.Char(string="Frequency", required=True)


class Duration(models.Model):
    _name = "clinic.duration"
    _description = "Duration"

    name = fields.Char(string="Duration", required=True)
