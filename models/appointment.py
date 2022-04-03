from odoo import api, fields, models, _, tools
from odoo.exceptions import UserError, ValidationError



class Appointment(models.Model):
    _name = "clinic.appointment"
    _description = "Appointment"

    today = fields.Datetime.now()
    appointmentDate = fields.Datetime(string='Appointment Date', required=True)
    arrivaltime = fields.Datetime(string='Arrival Time')
    patientStatus = fields.Selection([
        ('ambulatory', 'Ambulatory'),
        ('outpatient', 'OutPatient'),
        ('inpatient', 'InPatient'),
    ], string='Status', required=True, default='ambulatory')
    weight = fields.Integer(string="Weight in kg")
    height = fields.Integer(string='Height in cm')
    bmi = fields.Integer(string="BMI" )
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
    insurance_id = fields.Many2one('clinic.insurance', string="Insurance")
    doctor_id = fields.Many2one('clinic.doctor', string="Doctor")
    appointment_type_id = fields.Many2one('clinic.appointmenttype', string="Appointment Type", required=True)
    prescription_id = fields.Many2one('clinic.prescription', string="Prescription")
    medication_Prescrption_ids = fields.One2many('clinic.medicationpresc', 'appointment_id', String='Prescription')
    consumable_ids = fields.One2many('clinic.appointmentconsumable', 'appointment_id', String='Consumable')
    inventory_ids = fields.One2many('clinic.appointmentinventory', 'appointment_id', String='Inventory')
    quantity = fields.Integer(related='inventory_ids.quantity')
    stock = fields.Integer(related='inventory_ids.stock', readonly=False, store=True)
    labtest_ids = fields.Many2many('clinic.labtest', 'appointment_labtest_rel', 'appointment_id',
                                      'labtest_id', string='My Labtests')
    labtest_results = fields.Char(string='Labtests Results')
    labtest_img = fields.Image(string="Lab Test Image")
    imaging_ids = fields.Many2many('clinic.imaging', 'appointment_imaging_rel', 'appointment_id',
                                   'imaging_id', string='My Imaging')
    imaging_results = fields.Char(string='Imaging Results')
    required_surgery_ids = fields.Many2many('clinic.reqsurgery', 'appointment_reqsurgery_rel', 'appointment_id',
                                   'reqsurgery_id', string='Required Surgery')
    notes_html = fields.Text('Notes', help="Rich-text/HTML message")
    company_id = fields.Many2one('res.company', required=True, default=lambda self: self.env.company , readonly=True)
    patient_history_list = fields.Many2many('clinic.patienthistory', 'appointment_history_rel', 'appointment_id',
                                   'patient_history_id', string='Patient History')
    diagnosis_list = fields.Many2many('clinic.diagnosis', 'appointment_diagnosis_rel', 'appointment_id',
                                            'diagnosis_id', string='Diagnosis')
    patient_complain = fields.Many2many('clinic.complain', 'appointment_ptn_complain_rel', 'appointment_id',
                                      'ptn_complain_id', string='Patient Complain')
    services = fields.Char(string="Services",default="")
    current_user = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)

    def name_get(self):
        res = []
        for rec in self:
            print(rec)
            if rec != None and rec.id:
                res.append((rec.id, '%s - %s' % ('Appointment', rec.id)))

        return res

    @api.onchange('inventory_ids')
    def onchange_inventory_ids(self):
        if self.inventory_ids:
            if self.inventory_ids.filtered(lambda i:i.quantity > 0 and i.quantity > i.stock):
                self.inventory_ids = self.inventory_ids.filtered(lambda i:i.quantity > 0 and i.quantity > i.stock)
                raise ValidationError(
                    _('There is not enough stock from this product. Please update your Inventory first'))

    @api.model
    def create(self, vals):
        if vals.get('inventory_ids') != None:
            for i in range(len(vals['inventory_ids'])):
                #Add Inventory to update the stock
                if vals['inventory_ids'][i][2] != False and vals['inventory_ids'][i][0] == 0:
                    vals['inventory_ids'][i][2]['stock'] = vals['inventory_ids'][i][2]['stock'] - vals['inventory_ids'][i][2]['quantity']
        return super().create(vals)

    def write(self, vals):
        deletedItems =[]
        if vals.get('inventory_ids') != None:
            for i in range(len(vals['inventory_ids'])):
                #Update  inventory Id is 1
                if vals['inventory_ids'][i][2] != False and vals['inventory_ids'][i][0] == 1:
                    self.inventory_ids[i].stock += self.inventory_ids[i].quantity
                    self.inventory_ids[i].stock = self.inventory_ids[i].stock - vals['inventory_ids'][i][2]['quantity']
                    vals['inventory_ids'][i] += [{'stock': self.inventory_ids[i].stock}]
                # ADD inventory Id is 0
                elif vals['inventory_ids'][i][2] != False and vals['inventory_ids'][i][0] == 0:
                    vals['inventory_ids'][i][2]['stock'] = vals['inventory_ids'][i][2]['stock'] - vals['inventory_ids'][i][2]['quantity']
                #Delete inventory Id is 2
                elif vals['inventory_ids'][i][2] == False and vals['inventory_ids'][i][0] == 2:
                    # Add deleted items to array then add them at the end to the list
                    deletedItems.append([1,vals['inventory_ids'][i][1],{'stock': self.inventory_ids[i].quantity + self.inventory_ids[i].stock}])
                if deletedItems:
                    for i in range(len(deletedItems)):
                        vals['inventory_ids'].append(deletedItems[i])
        return super(Appointment, self).write(vals)

    def unlink(self):
        if self.inventory_ids != []:
            if len(self.inventory_ids) > 0:
                raise ValidationError(
                    _('Please Delete the inventory first before deleteing the appointment. To Adjust product inventory'))
        return super(Appointment, self).unlink()

    @api.onchange('prescription_id','imaging_ids','consumable_ids','labtest_ids','required_surgery_ids')
    def onchange_fields(self):
        self.services = ''
        if len(self.prescription_id) > 0:
            self.medication_Prescrption_ids = self.prescription_id.presc_med_ids
            if len(self.medication_Prescrption_ids) > 0:
                self.services += ' P '
        else:
            self.medication_Prescrption_ids = None
        if len(self.consumable_ids) > 0:
            self.services += ' C '
        if len(self.labtest_ids) > 0:
            self.services += ' L '
        if len(self.imaging_ids) > 0:
            self.services += ' I '
        if len(self.required_surgery_ids) > 0:
            self.services += ' RS '

    def send_msg(self):
        return {'type': 'ir.actions.act_window',
                'name': _('Whatsapp Message'),
                'res_model': 'whatsapp.new.message.wizard',
                'target': 'new',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_user_id': self.patient_id.id},
                }

    @api.onchange('appointmentDate', 'arrivaltime')
    def onchange_appointment_date(self):
        if self.arrivaltime and self.appointmentDate:
            if self.arrivaltime < self.appointmentDate:
                raise ValidationError(
                    _('Arrival time should be greater than appointment Date !'))



    @api.onchange('weight','height')
    def onchange_weight(self):
        if self.weight > 0 and self.height > 0:
            if self.height > 0:
                self.bmi = (self.weight * 10000) / (self.height * self.height)
        else:
            self.bmi = 0
    #
    # @api.onchange('prescription_id')
    # def onchange_prescription_id(self):
    #     if self.prescription_id:
    #         self.medication_Prescrption_ids = self.prescription_id.presc_med_ids
    #         # if len(self.medication_Prescrption_ids) > 0:
    #         #     if self.services.find('P') == -1:
    #         #         self.services += 'P'
    #     else:
    #         self.medication_Prescrption_ids = None

    @api.onchange('appointment_type_id')
    def onchange_appointment_type_id(self):
        if self.appointment_type_id:
            self.price = self.appointment_type_id.price

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        print(self.appointmentDate)
        print(self.appointmentDate.strftime('%Y-%m-%d'))
        print(self.today)
        if self.appointmentDate.strftime('%Y-%m-%d') > self.today.strftime('%Y-%m-%d'):
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

class PatientHistory(models.Model):
    _name = "clinic.patienthistory"
    _description = "patienthistory"

    name = fields.Char(string="Patient History")

class PatientComplain(models.Model):
    _name = "clinic.complain"
    _description = "patinet Complain"

    name = fields.Char(string="Diagnosis")

class Diagnosis(models.Model):
    _name = "clinic.diagnosis"
    _description = "diagnosis"

    name = fields.Char(string="Diagnosis")

    # def write(self, vals):
    #     if len(self.medication_Prescrption_ids) > 0:
    #         vals.update({'services': 'P'})
    #     if len(self.consumable_ids) > 0:
    #         if vals['services']:
    #             vals.update({'services': vals['services'] + ', C'})
    #         else:
    #             vals.update({'services': 'C'})
    #     if len(self.labtest_ids) > 0:
    #         if vals['services']:
    #             vals.update({'services': vals['services'] + ', L'})
    #         else:
    #             vals.update({'services': 'L'})
    #     if len(self.imaging_ids) > 0:
    #         if vals['services']:
    #             vals.update({'services': vals['services'] + ', I'})
    #         else:
    #             vals.update({'services': 'I'})
    #     return super(Appointment, self).write(vals)
