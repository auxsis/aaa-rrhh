# -*- coding: utf-8 -*-
#################################################################################
# Author      : Acespritech Solutions Pvt. Ltd. (<www.acespritech.com>)
# Copyright(c): 2012-Present Acespritech Solutions Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#################################################################################

{
    'name': 'Leave Encash (Enterprise)',
    'category': 'HR',
    'description': """Leave Encash
                 """,
    'summary': 'Employe leave enchash.',
    'author': 'Acespritech Solutions Pvt. Ltd.',
    'website': 'http://www.acespritech.com',
    'price': 35.00,
    'currency': 'EUR',
    'depends': ['base', 'account', 'hr_payroll', 'hr', 'hr_attendance',
                'hr_contract', 'hr_recruitment', 'hr_timesheet',
                ],
    'images': ['static/description/main_screenshot.png'],
    'data': [
         'security/leave_security.xml',
         'views/hr_job_views.xml',
         'wizard/leave_encash_process_views.xml',
         'views/leave_config_setting_views.xml',
         'views/leave_encash_views.xml',
         'views/hr_payroll_views.xml',
         'views/hr_payroll_data.xml',
         'views/report.xml',
         'wizard/leave_encash_report_wizard.xml',
         'report/leave_encash_report.xml',
         'security/ir.model.access.csv',
         'security/ir.model.access.csv',
    ],
    'demo': [
    ],
    'external_dependencies': {
        'python': [
            'numpy'
        ],
    },
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
