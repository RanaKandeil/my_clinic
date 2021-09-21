from odoo import api, fields, models

class Product(models.Model):
    _name = "clinic.product"
    _description = "Product"

    name = fields.Char(string="Product Name", required=True)
    company = fields.Char(string="Company", required=True)
    description = fields.Char(string="Description", required=True)
    warning_quantity = fields.Integer(string="Warning Quantity", required=True)

class Inventory(models.Model):
    _name = "clinic.inventory"
    _description = "Inventory"

    product_id = fields.Many2one('clinic.product', String='Product Inventory')
    product_company = fields.Char(related='product_id.company', readonly=True)
    warning_quan = fields.Integer(related='product_id.warning_quantity', readonly=True)
    expiration_date = fields.Date(string='Expiration',required=True)
    quantity = fields.Integer(string='Quantity')

    def name_get(self):
        res = []
        for rec in self:
            if rec.product_id:
                res.append((rec.id, '%s' % (rec.product_id.name)))
        return res

    _sql_constraints = [
        ('unique_inv_date', 'UNIQUE(product_id,expiration_date)',
         'This inventory already exists with the same expiry date. Please update the record with the new quantity')
    ]

class AppointmentInventory(models.Model):
    _name = "clinic.appointmentinventory"
    _description = "Inventory"

    inventory_id = fields.Many2one('clinic.inventory', string="Inventory",required=True)
    expiration_date = fields.Date(related='inventory_id.expiration_date')
    product_company = fields.Char(related='inventory_id.product_company')
    stock = fields.Integer(related='inventory_id.quantity',string="stock",readonly=False)
    appointment_id = fields.Many2one('clinic.appointment', String="Appointment Id")
    quantity = fields.Integer(string='Quantity', required=True)

    _sql_constraints = [
        ('unique_appointment_inventory', 'UNIQUE(inventory_id,appointment_id)',
         'You had added the same inventory more than one time.')
    ]


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

    consumable_id = fields.Many2one('clinic.consumables', string="Consumable",required=True)
    description = fields.Char(related='consumable_id.description', required=True)
    appointment_id = fields.Many2one('clinic.appointment', String="Appointment Id")
    quantity = fields.Integer(string='Quantity', required=True)
