{
    'name': "HR Payroll Leave Type Code",

    'summary': """
        Add field Code to Leave Type to simplify input in salary rules""",

    'description': """
The problem
===========
When worked days lines are loaded in a payslip, leave type's names, as Odoo default, are encoded as codes in the payslip which causes problem in salary rule computation
if the leave type's names are not in compliant within Python variable syntax (e.g. 'Legal Leave' was appeared as the code while it should be either 'LEGALLEAVE' or 'legalleave' or something else similar).

Solution
========
This module adds a code field to the leave type then user can use it as Code for payslip calculation instead


Editions Supported
==================
1. Community Edition
2. Enterprise Edition

    """,

    'author': "T.V.T Marine Automation (aka TVTMA)",
    'website': 'https://www.tvtmarine.com',
    'live_test_url': 'https://v12demo-int.erponline.vn',
    'support': 'support@ma.tvtmarine.com',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['hr_payroll'],

    # always loaded
    'data': [
        'views/hr_leave_type_views.xml'
    ],

    'installable': True,
    'application': False,
    'auto_install': True,
    'price': 9.9,
    'currency': 'EUR',
    'license': 'OPL-1',
}
