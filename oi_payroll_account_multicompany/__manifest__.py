# -*- coding: utf-8 -*-
# Copyright 2018 Openinside co. W.L.L.
{
    "name": "Payroll Accounting - Multi Company Settings",
    "summary": "Payroll Accounting - Multi Company Settings",
    "version": "12.0.1.1.0",
    'category': 'Human Resources',
    "website": "https://www.open-inside.com",
	"description": """
		salary rules accounting settings for multi company
		 
    """,
	'images':[
        
	],
    "author": "Openinside",
    "license": "OPL-1",
    "price" : 9.99,
    "currency": 'EUR',
    "installable": True,
    "depends": [
        'hr_payroll_account'
    ],
    "data": [
        'view/hr_payslip_run.xml',
        'view/hr_payslip_employees.xml'
    ],
    'odoo-apps' : True,
    'images':[
        'static/description/cover.png'
    ]        
}

