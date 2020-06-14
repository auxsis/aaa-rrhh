from odoo import models, api


class hr_payslip(models.Model):
    _inherit = 'hr.payslip'

    @api.model
    def get_worked_day_lines(self, contract_ids, date_from, date_to):
        """
        @param contract_ids: list of contract id
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        res = super(hr_payslip, self).get_worked_day_lines(contract_ids, date_from, date_to)
        if res:
            for line in res:
                company_id = self.env['hr.contract'].search([('id', '=', line['contract_id'])], limit=1).employee_id.company_id
                leave_type_id = self.env['hr.leave.type'].search([('name', '=', line['name']), '|', ('company_id', '=', company_id.id), ('company_id', '=', False)], limit=1)
                if leave_type_id:
                    ######### START MONKEY PATCHING ##############
                    # Since Odoo recalls computing for the code field,
                    # we must query the value from the database instead of holiday_type_id.code
                    # see the issue https://github.com/odoo/odoo/issues/25169
                    self.env.cr.execute("SELECT code FROM hr_leave_type WHERE id=%s", (leave_type_id.id,))
                    row = self.env.cr.fetchone()
                    line['code'] = row[0]
                    ######### END MONKEY PATCHING ##############
                    # The line below should be uncommented when the issue a.m. is solve
#                     line['code'] = leave_type_id.code
        return res
