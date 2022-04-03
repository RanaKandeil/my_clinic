from odoo import api, fields, models



class LabtestUnit(models.Model):
    _name = "clinic.labtestunit"
    _description = "Labtestnit"

    name = fields.Char(string="Unit", required=True)
    code = fields.Char(string="Code")

class Parameters(models.Model):
    _name = "clinic.parameters"
    _description = "parameters"

    name = fields.Char(string="Name", required=True)
    minValue = fields.Float(string="Minimum Value")
    maxValue = fields.Float(string="Maximum Value")
    unit_id = fields.Many2one('clinic.labtestunit', string="Unit")

class Sample(models.Model):
    _name = "clinic.sample"
    _description = "sample"

    name = fields.Char(string="Sample", required=True)


class Preinformation(models.Model):
    _name = "clinic.preinformation"
    _description = "preinformation"

    name = fields.Char(string="Name", required=True)


class Labtest(models.Model):
    _name = "clinic.labtest"
    _description = "Labtest"

    name = fields.Char(string="Labtest name", required=True)
    sample_id = fields.Many2one('clinic.sample', string='Sample')
    preinformation_id = fields.Many2one('clinic.preinformation', string='Pre-Information')


class LabtestPatientResult(models.Model):
    _name = "clinic.labtestpatientresult"
    _description = "Labtest_patient_result"

    labtest_id = fields.Many2one('clinic.labtest', string='Lab Test')
    sample_id = fields.Many2one(related='labtest_id.sample_id',readonly=True)
    preinformation_id =  fields.Many2one(related='labtest_id.preinformation_id',readonly=True)
    result_image = fields.Binary(string='Result Image')
    labtest_result_id = fields.Many2one('clinic.labtestresults', String="Result Id")

class LabtestResults(models.Model):
    _name = "clinic.labtestresults"
    _description = "labtestresults"

    patient_id = fields.Many2one('clinic.patient', string="Patient",required=True)
    phoneNumber = fields.Char(related='patient_id.phoneNumber',readonly=True)
    labtest_result_ids = fields.One2many('clinic.labtestpatientresult', 'labtest_result_id', String='LabTest Result')
    results_date = fields.Date(string='Results Date',
                                       default=lambda self: fields.Date.context_today(self).replace(month=1, day=1),
                                       required=True, help="That is the date of the results.")
