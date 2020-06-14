from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'

    code = fields.Char(string='Code', compute='_compute_code', inverse='_set_code', store=True,
                       help="The code of the Leave Type which can be used for Python code in salary rules."
                       " For example, if you have a Legal Leave Type with code of LEGALLEAVE, you can get"
                       " number of left days with the formula \"result=worked_days.LEGALLEAVE.number_of_days\""
                       )
    _sql_constraints = [
        ('name_company_unique',
         'UNIQUE(name,company_id)',
         "The Leave Type's name must be unique per company"),
        ('code_company_unique',
         'UNIQUE(code,company_id)',
         "The Leave Type's code must be unique per company")
    ]

    @api.constrains('code')
    def _check_code_validity(self):
        for r in self:
            if r.code and not r.code.isidentifier():
                raise ValidationError(_("The code \"%s\" is not a valid code. A valid code may contain alphanumeric and underscore only.") % (r.code,))

    @api.depends('name')
    def _compute_code(self):
        for r in self:
            r.code = r.name.strip().replace(" ", "").encode('ascii', 'ignore').upper() if r.name else False

    def _set_code(self):
        pass

