from . import models
from odoo.tools.sql import rename_column

def pre_init_hook(cr):
    for col in ['analytic_account_id', 'account_tax_id', 'account_debit', 'account_credit']:
        rename_column(cr, 'hr_salary_rule', col, 't_' + col)