import base64
import logging
import tempfile
from odoo import models, fields, api, _
import logging as _logger

try:
    import xlsxwriter
except ImportError:
    _logger.warning("Cannot import xlsxwriter")
    xlsxwriter = False

class consolidado_autorizacion_report_excel(models.Model):
    _inherit = 'hr.payslip.run'



    def find_rule_value(self, list, code):
        sol = 0
        for lines in list:
            if lines.code == code:
                sol = lines.total
                break
        return sol



    def action_export_xls_custom_consolidado(self):
        if not xlsxwriter:
            raise UserError(_("The Python library xlsxwriter is installed. Contact your system administrator"))

        file_path = tempfile.mktemp(suffix='.xlsx')
        workbook = xlsxwriter.Workbook(file_path)
        worksheet = workbook.add_worksheet("Hoja 1")

        styles={
            'currency_format': workbook.add_format({
                'num_format': '#,##0.00',
                'font_size': 10,
                'border': 0,
            }),
            'main_data': workbook.add_format({
                'font_size': 10,
                'border': 0,
            }),
        }

        worksheet.set_column(0, 0, 10)
        worksheet.set_column(1, 1, 20)
        worksheet.set_column(2, 2, 12)
        worksheet.set_column(3, 3, 40)
        worksheet.set_column(4, 4, 12)

        worksheet.write(1, 0, 'CORPORACION DE EMPRESAS REGIONALES DE LA CONSTRUCCION', styles.get("main_data"))
        worksheet.write(3, 0, 'CONSOLIDADO PARA AUTORIZACION DE PAGO DE PANILLA EN BANCA EN LINEA', styles.get("main_data"))

        worksheet.write(5, 0, 'NO. EMP.',styles.get("main_data"))
        worksheet.write(5, 1, 'NOMBRES Y APELLIDOS', styles.get("main_data"))
        worksheet.write(5, 2, '# CUENTA', styles.get("main_data"))
        worksheet.write(5, 3, 'CONCEPTO', styles.get("main_data"))
        worksheet.write(5, 4, 'MONT APLICAR', styles.get("main_data"))
        column = 6
        for lines in self.slip_ids:
            if lines.employee_id.x_studio_forma_de_pago=="Transferencia":
                worksheet.write(column, 0, lines.employee_id.x_studio_numero_de_empleado, styles.get("main_data"))
                worksheet.write(column, 1, lines.employee_id.display_name, styles.get("main_data"))
                worksheet.write(column, 2, lines.employee_id.x_studio_numero_de_cuenta, styles.get("main_data"))
                worksheet.write(column, 3, lines.name, styles.get("main_data"))
                worksheet.write(column, 4, self.find_rule_value(lines.line_ids, 'N501NETO'),
                                styles.get("currency_format"))
                column += 1

        workbook.close()

        with open(file_path, 'rb') as r:
            xls_file = base64.b64encode(r.read())
        att_vals = {
            'name': u"{}#{}.xlsx".format("Reporte Consolidado para autorizacion de pago de planilla en banca en linea", fields.Date.today()),
            'type': 'binary',
            'datas': xls_file,
            'datas_fname': u"{}#{}.xlsx".format("Reporte Consolidado para autorizacion de pago de planilla en banca en linea", fields.Date.today()),
        }
        attachment_id = self.env['ir.attachment'].create(att_vals)
        self.env.cr.commit()
        action = {
            'type': 'ir.actions.act_url',
            'url': '/web/content/{}?download=true'.format(attachment_id.id, ),
            'target': 'self',
        }
        return action
