# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright 2019 EquickERP
#
##############################################################################
{
    'name': "Batch Payslip Report",
    'category': 'Payroll',
    'version': '1.0',
    'author': 'Equick ERP',
    'description': """
        This Module allows to print Payroll PDF & Excel Report.
    """,
    'summary': 'This Module allows to print Payroll PDF & Excel Report.',
    'depends': ['base', 'hr_payroll'],
    'price': 25,
    'currency': 'EUR',
    'license': 'AGPL-3',
    'website': "",
    'data': [
        'wizard/wizard_batch_payslip_report.xml',
        'report/report_batch_payslip_template.xml',
        'report/report.xml'
    ],
    'demo': [],
    'images': ['static/description/main_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: