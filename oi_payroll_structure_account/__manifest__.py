# -*- coding: utf-8 -*-
# Copyright 2018 Openinside co. W.L.L.
{
    "name": "Payroll - Account By Salary Structure",
    "summary": "Payroll - Account By Salary Structure",
    "version": "12.0.1.1.4",
    'category': 'Human Resources',
    "website": "https://www.open-inside.com",
	"description": """
		 Payroll - Account By Salary Structure
		 
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
        'view/hr_payroll_structure.xml',
        'view/hr_salary_rule.xml',
        'security/ir.model.access.csv'
    ],
    'pre_init_hook' : 'pre_init_hook',
    'odoo-apps' : True    
}

