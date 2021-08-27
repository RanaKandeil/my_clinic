# -*- coding: utf-8 -*-
{
    'name': "My Clinic Managment",
    'summary': """All Data required for my Clinic and Doctor analysis """,
    'description': """Patients, Appointments, Prescriptions""",
    'sequence': -100,
    'author': "Odoo House",
    'website': "http://www.RANK.com",
    'category': 'Productivity',
    'version': '14.0',
    'depends': [],
    'data': [
        'security/ir.model.access.csv',
        'views/patient.xml',
        'views/appointment.xml',
        'views/prescription.xml',
        'views/configuration.xml',
        'views/labtest.xml',
        'views/imaging.xml',
        # 'report/appointment_prescreption.xml',
        'report/appointment_prescription_arabic.xml',
        'report/report.xml',
    ],
    'demo': [],
    'installable':True,
    'application': True,
    'auto_install': False
}