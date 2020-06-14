# -*- coding: utf-8 -*-
# Copyright (C) 2017-present  Technaureus Info Solutions(<http://www.technaureus.com/>).

{
    'name': 'TDS or Withholding Tax',
    'version': '1.1',
    'category': 'Accounting & Finance',
    'sequence': 1,
    'summary': 'Tax Deducted at Source(TDS) or Withholding Tax.',
    'description': """
Manage Tax Deducted at Source(TDS) or Withholding Tax
===========================================================

This application allows you to apply TDS or withholding tax at the time of invoice or payment.

    """,
    'website': 'http://www.technaureus.com/',
    'author': 'Technaureus Info Solutions Pvt. Ltd.',
    'depends': ['account'],
    'price': 165,
    'currency': 'EUR',
    'license': 'Other proprietary',
    'data': [
        'views/account_view.xml',
        'views/res_partner_view.xml',
        'views/account_payment_view.xml',
        'views/account_invoice_view.xml',
    ],
    'demo': [],
    'css': [],
    'images': ['images/tds_screenshot.png'],
    'installable': True,
    'auto_install': False,
    'application': True,
    'live_test_url': 'https://www.youtube.com/watch?v=_KfswiLoSok'
}
