# -*- coding: utf-8 -*-
# Copyright 2018 Openinside co. W.L.L.
{
    "name": "Payroll - Accrued Leave Rules",
    "summary": "Payroll - Accrued Leave Rules",
    "version": "12.0.1.1.0",
    'category': 'Human Resources',
    "website": "https://www.open-inside.com",
	"description": """
		Payroll - Accrued Leave Rules
		 
    """,
	'images':[
        
	],
    "author": "Openinside",
    "license": "OPL-1",
    "price" : 9.99,
    "currency": 'EUR',
    "installable": True,
    "depends": [
        'hr_payroll','oi_hr_holidays_allocation_date'
    ],
    "data": [
        'data/hr_salary_rule.xml'
    ],
    'odoo-apps' : True    
}

