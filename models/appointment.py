from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError

class Appointment(models.Model):
    _name = "clinic.appointment"
    _description = "Appointment"

    today = fields.Datetime.now()
    appointmentDate = fields.Datetime(string='Appointment Date', required=True)
    patientStatus = fields.Selection([
        ('ambulatory', 'Ambulatory'),
        ('outpatient', 'OutPatient'),
        ('inpatient', 'InPatient'),
    ], string='Status', required=True, default='ambulatory')

    urgencyLevel = fields.Selection([
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('emergency', 'Medical Emergency'),
    ], string='Urgency Level', required=True, default='normal')

    patientTemp = fields.Float(string="Patient Temperature", default="36.5")

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Canceled'),
    ], string='State', default='draft')
    observation = fields.Char(string="Observation")
    price = fields.Float(string="Price")
    patient_id = fields.Many2one('clinic.patient', string="Patient")
    appointment_type_id = fields.Many2one('clinic.appointmenttype', string="Appointment Type", required=True)
    prescription_id = fields.Many2one('clinic.prescription', string="Prescription")
    medication_ids = fields.Many2many('clinic.medication', 'appointment_medication_rel', 'appointment_id',
                                      'medication_id', string='My Medications')
    # medication_Prescrption_ids = fields.Many2many('clinic.medicationpresc', 'appointment_med_presc_rel', 'appointment_id',
    #                                   'medication_presc_id', string='My Prescription')
    medication_Prescrption_ids = fields.One2many('clinic.medicationpresc', 'appointment_id', String='Prescription')
    labtest_ids = fields.Many2many('clinic.labtest', 'appointment_labtest_rel', 'appointment_id',
                                      'labtest_id', string='My Labtests')
    labtest_results = fields.Char(string='Labtests Results')
    imaging_ids = fields.Many2many('clinic.imaging', 'appointment_imaging_rel', 'appointment_id',
                                   'imaging_id', string='My Imaging')
    imaging_results = fields.Char(string='Imaging Results')

    diagnosis_html = fields.Text('Diagnosis', help="Rich-text/HTML message")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company , readonly=True)

    @api.onchange('prescription_id')
    def onchange_prescription_id(self):
        if self.prescription_id:
            self.medication_Prescrption_ids = self.prescription_id.presc_med_ids
        else:
            self.medication_Prescrption_ids = None

    @api.onchange('appointment_type_id')
    def onchange_appointment_type_id(self):
        if self.appointment_type_id:
            self.price = self.appointment_type_id.price

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        print(self.appointmentDate)
        print(self.today)
        if self.appointmentDate > self.today:
            raise ValidationError(
                _('Appointment Date is greater than today. So It cannot be Confirmed !'))
        else:
            self.state = 'done'

    def action_draft(self):
        self.state = 'draft'

    def action_cancel(self):
        self.appointment_type_id = None
        self.price = 0
        self.state = 'cancel'

   