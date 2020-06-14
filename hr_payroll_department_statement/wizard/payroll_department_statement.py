# -*- coding: utf-8 -*-

import xlwt
import io
# import cStringIO
import base64
import time
from dateutil.relativedelta import relativedelta
from openerp import models, fields, api, _
from openerp.exceptions import Warning
from openerp.http import request
from datetime import datetime, date

from odoo.exceptions import UserError

class SalaryMonthlyStatement(models.TransientModel):
    _name = 'payroll.department.statement'
    
    today = date.today()
    first_day = today.replace(day=1)
    last_day = date(today.year,today.month,1)+relativedelta(months=1,days=-1)

    start_date = fields.Date(
        string='Dia de inicio',
        required=True,
        default=first_day,
    )
    end_date = fields.Date(
        string='Dia de fin',
        required=True,
        default=last_day,
    )
    company_id = fields.Many2one(
        'res.company',
        string='Compañia',
        required=True,
        default=lambda self: self.env.user.company_id,
    )
    department_ids = fields.Many2many(
        'hr.department',
        string="Departamentos",
    )

    @api.model
    def _get_rules(self, payslips_dict):
        rules = self.env['hr.salary.rule'].search([('parent_rule_id', '=', False)], order='sequence')
        RULES_DICT = {}
        RULES_NAME = {}
        cnt = 2
        for payslips in payslips_dict:
            for date in payslips_dict[payslips]:
                for payship_id in payslips_dict[payslips][date]:
                    for line in payship_id.line_ids:
                        if line.salary_rule_id.code not in RULES_DICT:

                            if line.salary_rule_id.appears_on_payslip:
                                RULES_DICT.update({line.salary_rule_id.code : cnt})
                                RULES_NAME.update({line.salary_rule_id.code: line.salary_rule_id.name})
                                cnt += 1
        return RULES_DICT, RULES_NAME

    @api.model
    def _get_payslips(self):
        department_ids = False
        if self.department_ids:
            department_ids = self.department_ids
        else:
            department_ids = self.env['hr.department'].search([])
        department_wise_payslip = {}
        for department in department_ids:
            domain = []
            employees = self.env['hr.employee'].search([('department_id','=', department.id)])
            domain.append(('date_from', '>=', self.start_date))
            domain.append(('date_from', '<=', self.end_date))
            domain.append(('employee_id', 'in', employees.ids))
            if self.company_id:
                domain.append(('company_id', '=', self.company_id.id))
            domain.append(('state', '=', 'draft'))
            payslips = self.env['hr.payslip'].search(domain, order = 'date_from')

            payslips_dict = {}
            for payslip in payslips:
                if payslip.date_from not in payslips_dict:
                    payslips_dict[payslip.date_from] = payslip
                else:
                    payslips_dict[payslip.date_from] += payslip
                if not payslips:
                    raise Warning(_('Payslips are not found!'))


            department_wise_payslip[department.name] = payslips_dict
        for res in self:
            if not res.department_ids:
                domain = []
                employees = res.env['hr.employee'].search([('department_id','=',False)])
                domain.append(('date_from', '>=', res.start_date))
                domain.append(('date_from', '<=', res.end_date))
                if employees.ids:
                    domain.append(('employee_id', 'in', employees.ids))
                if res.company_id:
                    domain.append(('company_id', '=', res.company_id.id))
                domain.append(('state', '=', 'draft'))
                payslips = res.env['hr.payslip'].search(domain, order = 'date_from')

                if not payslips:
                    raise UserError("No se han encontrado boletas de pago  de empleados en estado borrador en este rango de fecha")

                payslips_dict = {}
                for payslip in payslips:
                    if payslip.date_from not in payslips_dict:
                        payslips_dict[payslip.date_from] = payslip
                    else:
                        payslips_dict[payslip.date_from] += payslip
                    if not payslips:
                        raise Warning(_('Payslips are not found!'))
                    department_wise_payslip['Unknown'] = payslips_dict
        return department_wise_payslip
    
    @api.multi
    def print_payroll_statement_excel(self):
        workbook = xlwt.Workbook()
        title_style_comp_left = xlwt.easyxf('align: horiz center ; font: name Times New Roman,bold off, italic off, height 450')
        title_style = xlwt.easyxf('align: horiz center ;font: name Times New Roman,bold off, italic off, height 350')
        title_style2 = xlwt.easyxf('font: name Times New Roman, height 200')
        title_style1 = xlwt.easyxf('font: name Times New Roman,bold on, italic off, height 190; borders: top thin, bottom thin, left thin, right thin;')
        title_style1_table_head = xlwt.easyxf('font: name Times New Roman,bold off, italic off, height 200;')
        title_style1_table_head1 = xlwt.easyxf('font: name Times New Roman,bold on, italic off, height 200')
        title_style1_table_head_center = xlwt.easyxf('align: horiz center ;font: name Times New Roman,bold on, italic off, height 200')
        borders = xlwt.easyxf('font: name Times New Roman,bold on, italic off, height 200; borders: top thin;')

        sheet_name = 'Estado Nomina Departamento'
        sheet = workbook.add_sheet(sheet_name)
        sheet.write_merge(0, 1, 0, 6, 'Declaracion de Salario por Departamento' , title_style_comp_left)
        sheet.write(3, 0, 'Company:', title_style1_table_head1)
        sheet.write(3, 1, self.company_id.name, title_style2)

        row_date_count = 4
        user = request.env.user
        now_date_time = datetime.now().strftime('%d/%m/%Y %H:%M:%S')
        sheet.write(3, 3, 'Generado por:', title_style1_table_head1)
        sheet.write(3, 4, user.name, title_style2)
        sheet.write(3, 7, 'Generado en:', title_style1_table_head1)
        sheet.write_merge(3, 3, 8, 9,now_date_time, title_style2)
        start_date = datetime.strftime(datetime.strptime(str(self.start_date), '%Y-%m-%d'), '%d/%m/%Y')
        end_date = datetime.strftime(datetime.strptime(str(self.end_date), '%Y-%m-%d'), '%d/%m/%Y')
        sheet.write(row_date_count, 0, 'Dia inicial:', title_style1_table_head1)
        sheet.write(row_date_count, 1, start_date, title_style2)
        sheet.write(row_date_count, 3, 'Dia final:', title_style1_table_head1)
        sheet.write(row_date_count, 4, end_date, title_style2)

        department_wise_dict = self._get_payslips()
        RULES_DICT, RULES_NAME = self._get_rules(department_wise_dict)
        print ("&&&&&&&&&&&&&&&&&&&&&&",RULES_DICT)

        if not RULES_DICT:
            message = "No se encontraron reglas salariales para las opciones dadas"
            raise UserError(message)

        department_count = 6
        final_total_salary = 0.0
        for dept in department_wise_dict:
            if not department_wise_dict[dept]:
                continue
            sheet.write(department_count, 0, 'Departamentos:', title_style1_table_head1)
            sheet.write_merge(department_count, department_count, 1, 2, dept, title_style2)
            payslips_dict_key = department_wise_dict[dept]
            payslips_dict = payslips_dict_key.keys()
            list(payslips_dict).sort()
            payslips_month_count = department_count + 1
            dept_wise_total_salary=0.0
            for payslips_month in payslips_dict:
                payslip_month = datetime.strftime(datetime.strptime(str(payslips_month), '%Y-%m-%d'), '%B-%Y')
                sheet.write(payslips_month_count, 0, 'Nómina Mensual:', title_style1_table_head1)
                sheet.write_merge(payslips_month_count, payslips_month_count, 1, 2, payslip_month, title_style2)
                sheet.write(payslips_month_count+1, 0, 'Sr.No', title_style1)
                sheet.write(payslips_month_count+1, 1, 'Empleado', title_style1)
                for rule in RULES_DICT:
                    sheet.write(payslips_month_count+1, RULES_DICT[rule], RULES_NAME[rule], title_style1)
                monthly_total_salary = 0.0
                payslip_line_count = payslips_month_count + 2
                sr_count = 1
                for payslip in payslips_dict_key[payslips_month]:
                    sheet.write(payslip_line_count, 0, sr_count, title_style1_table_head)
                    sheet.write(payslip_line_count, 1, payslip.employee_id.name, title_style1_table_head)
                    for line in payslip.line_ids:

                        try:
                            if line.appears_on_payslip:
                                if self.company_id.currency_id.position == 'after':
                                    sheet.write(payslip_line_count, RULES_DICT[line.code],"{0:.2f}".format(line.total), title_style1_table_head)
                                if self.company_id.currency_id.position == 'before':
                                    sheet.write(payslip_line_count, RULES_DICT[line.code],"{0:.2f}".format(line.total), title_style1_table_head)
                        except:
                            pass

                        if line.code == 'EXP_OPE_Neto':
                            monthly_total_salary += line.total

                    sr_count += 1
                    payslip_line_count += 1
                sheet.write_merge(payslip_line_count, payslip_line_count, len(RULES_DICT) - 1, len(RULES_DICT), 'Total de Salario Mensual', borders)
                if self.company_id.currency_id.position == 'after':
                    sheet.write(payslip_line_count, len(RULES_DICT) + 1,"{0:.2f}".format(monthly_total_salary), borders)
                if self.company_id.currency_id.position == 'before':
                    sheet.write(payslip_line_count, len(RULES_DICT) + 1, "{0:.2f}".format(monthly_total_salary), borders)
                dept_wise_total_salary += monthly_total_salary
                payslips_month_count = payslip_line_count + 1
            sheet.write_merge(payslips_month_count, payslips_month_count, len(RULES_DICT) - 1, len(RULES_DICT), 'Salario mensual total por departamento', borders)
            if self.company_id.currency_id.position == 'after':
                sheet.write(payslips_month_count, len(RULES_DICT) + 1,"{0:.2f}".format(dept_wise_total_salary), borders)
            if self.company_id.currency_id.position == 'before':
                sheet.write(payslips_month_count, len(RULES_DICT) + 1, "{0:.2f}".format(dept_wise_total_salary), borders)
            department_count = payslips_month_count + 1
            final_total_salary += dept_wise_total_salary
        print ("***********************department_count",department_count,len(RULES_DICT))
        sheet.write_merge(department_count, department_count, len(RULES_DICT) - 1, len(RULES_DICT), 'Salario Total', borders)
        if self.company_id.currency_id.position == 'after':
            sheet.write(department_count, len(RULES_DICT) + 1,"{0:.2f}".format(final_total_salary), borders)
        if self.company_id.currency_id.position == 'before':
            sheet.write(department_count, len(RULES_DICT) + 1, "{0:.2f}".format(final_total_salary), borders)
#         stream = cStringIO.StringIO()
        stream = io.BytesIO() # odoo11
        workbook.save(stream)
        attach_id = self.env['payroll.department.statement.excel'].create({'name':'Payroll Statement Department.xls', 'xls_output': base64.encodestring(stream.getvalue())})
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'payroll.department.statement.excel',
            'res_id':attach_id.id,
            'type': 'ir.actions.act_window',
            'target':'new'
        }

class PayrollDepartmentStatementExcel(models.Model):
    _name = 'payroll.department.statement.excel'
    _description = 'Wizard to store the Excel output'

    xls_output = fields.Binary(string='Excel Output',
                               readonly=True
                               )
    name = fields.Char(string='File Name',
                        help='Save report as .xls format',
                        default='Payroll Statement Department.xls',
                        )

# #vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
