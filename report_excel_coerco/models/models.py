# -*- coding: utf-8 -*-
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


class report_excel_coerco(models.Model):
    _inherit = 'hr.payslip.run'

    def find_rule_value(self, list, code):
        sol = 0
        for lines in list:
            if lines.code == code:
                sol = lines.total
                break
        return sol

    def action_export_xls_custom(self):
        if not xlsxwriter:
            raise UserError(_("The Python library xlsxwriter is installed. Contact your system administrator"))

        file_path = tempfile.mktemp(suffix='.xlsx')
        workbook = xlsxwriter.Workbook(file_path)
        styles = {
            'main_data_top_left': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'top': 1,
                'left': 1,
            }),
            'main_data_top_right': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'top': 1,
                'right': 1,
            }),
            'main_data_middle_left': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'left': 1,
            }),
            'main_data_top': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'top': 1,
            }),
            'main_data_middle': workbook.add_format({
                'font_size': 10,
                'border': 0,

            }),
            'main_data_middle_right': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'right': 1,
            }),
            'main_data_bottom': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'bottom': 1,
            }),
            'main_data_bottom_left': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'bottom': 1,
                'left': 1,
            }),
            'main_data_bottom_right': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'bottom': 1,
                'right': 1,
            }),
            'main_data_bold': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'bold': True,
                'top': 1,
            }),
            'main_data_bold_dpto': workbook.add_format({
                'font_size': 10,
                'border': 0,
                'bold': True,

            }),
            'currency_format': workbook.add_format({
                'num_format': '#,##0.00',
                'font_size': 10,
                'border': 0,
            }),
            'currency_format_bottom': workbook.add_format({
                'num_format': '#,##0.00',
                'font_size': 10,
                'border': 0,
                'bottom': 1,
            }),

        }
        worksheet = workbook.add_worksheet("Hoja 1")
        worksheet.set_row(6, 25)
        worksheet.set_row(7, 35)
        worksheet.set_row(8, 31)
        worksheet.set_row(9, 28)

        date_first = str(self.date_start).split("-")
        final_date = str(self.date_end).split("-")

        worksheet.write(0,0,"Corporación de Empresas  Regionales de la Construcción",styles.get("main_data_middle"))

        worksheet.write(2, 0, "Planilla correspondiente del " + date_first[2] + "/" + date_first[1] + "/" + date_first[
            0] + " al " + final_date[2] + "/" + final_date[1] + "/" + final_date[0], styles.get("main_data_middle"))
        worksheet.write(2, 12, "USUARIO: " + self.env.user.name, styles.get("main_data_middle"))

        worksheet.set_column(0, 0, 15)
        worksheet.set_column(1, 1, 11)
        worksheet.set_column(2, 2, 15)
        worksheet.set_column(3, 3, 12)
        worksheet.set_column(4, 4, 12)
        worksheet.set_column(5, 5, 10)
        worksheet.set_column(6, 6, 10)
        worksheet.set_column(7, 7, 8)
        worksheet.set_column(8, 8, 12)
        worksheet.set_column(9, 9, 14)
        worksheet.set_column(10, 10, 10)
        worksheet.set_column(11, 11, 10)
        worksheet.set_column(12, 12, 10)
        worksheet.set_column(13, 13, 10)
        worksheet.set_column(14, 14, 10)
        worksheet.write(6, 0, 'No . Empleado', styles.get("main_data_top_left"))
        worksheet.write(7, 0, 'Salario Mensual', styles.get("main_data_middle_left"))
        worksheet.write(8, 0, 'Salario Ordinario', styles.get("main_data_middle_left"))
        worksheet.write(9, 0, 'INSS Laboral', styles.get("main_data_bottom_left"))
        worksheet.write(6, 1, 'Nombres y Apellidos', styles.get("main_data_top"))
        worksheet.write(7, 1, '% Antiguedad', styles.get("main_data_middle"))
        worksheet.write(8, 1, 'Antiguedad', styles.get("main_data_middle"))
        worksheet.write(9, 1, 'IR', styles.get("main_data_bottom"))
        worksheet.write(6, 2, '', styles.get("main_data_top"))
        worksheet.write(7, 2, 'Dias Feriados', styles.get("main_data_middle"))
        worksheet.write(8, 2, 'Monto Feriado', styles.get("main_data_middle"))
        worksheet.write(9, 2, 'ISSDHU Emergente', styles.get("main_data_bottom"))
        worksheet.write(6, 3, '', styles.get("main_data_top"))
        worksheet.write(7, 3, 'Días Carencia', styles.get("main_data_middle"))
        worksheet.write(8, 3, 'Monto Carencia', styles.get("main_data_middle"))
        worksheet.write(9, 3, 'Monto Seguro', styles.get("main_data_bottom"))
        worksheet.write(6, 4, '', styles.get("main_data_top"))
        worksheet.write(7, 4, 'Dias AYECCH', styles.get("main_data_middle"))
        worksheet.write(8, 4, 'Monto AYECCH', styles.get("main_data_middle"))
        worksheet.write(9, 4, 'INISER', styles.get("main_data_bottom"))
        worksheet.write(6, 5, 'Cargo', styles.get("main_data_top"))
        worksheet.write(7, 5, 'Días Riesgo \nProfesional', styles.get("main_data_middle"))
        worksheet.write(8, 5, 'Riesgo \nProfesional', styles.get("main_data_middle"))
        worksheet.write(9, 5, 'Adelanto de \nSalario', styles.get("main_data_bottom"))
        worksheet.write(6, 6, '', styles.get("main_data_top"))
        worksheet.write(7, 6, 'Días \nMaternidad', styles.get("main_data_middle"))
        worksheet.write(8, 6, 'Monto \nMaternidad', styles.get("main_data_middle"))
        worksheet.write(9, 6, 'ISSDHU \nExterno', styles.get("main_data_bottom"))
        worksheet.write(6, 7, 'No de \nCédula', styles.get("main_data_top"))
        worksheet.write(7, 7, 'Días \nAYECSH', styles.get("main_data_middle"))
        worksheet.write(8, 7, 'Monto \nAYECSH', styles.get("main_data_middle"))
        worksheet.write(9, 7, 'Sindicato', styles.get("main_data_bottom"))
        worksheet.write(6, 8, 'No de INSS', styles.get("main_data_top"))
        worksheet.write(7, 8, 'Cantidad Horas \nExtras', styles.get("main_data_middle"))
        worksheet.write(8, 8, 'Horas Extras', styles.get("main_data_middle"))
        worksheet.write(9, 8, 'Embargo \nAlimenticio', styles.get("main_data_bottom"))
        worksheet.write(6, 9, '', styles.get("main_data_top"))
        worksheet.write(7, 9, '', styles.get("main_data_middle"))
        worksheet.write(8, 9, 'Otros Ingresos', styles.get("main_data_middle"))
        worksheet.write(9, 9, 'Embargo Ejecutivo', styles.get("main_data_bottom"))
        worksheet.write(6, 10, 'Fecha de \nIngreso', styles.get("main_data_top"))
        worksheet.write(7, 10, 'Días \nVacaciones \nDescansadas', styles.get("main_data_middle"))
        worksheet.write(8, 10, 'Vacaciones \nDescansadas', styles.get("main_data_middle"))
        worksheet.write(9, 10, 'Otras \nDeduciones', styles.get("main_data_bottom"))
        worksheet.write(6, 11, '', styles.get("main_data_top"))
        worksheet.write(7, 11, 'Días \nVacaciones \nPagadas', styles.get("main_data_middle"))
        #worksheet.write(8, 11, 'Vacaciones \nPagadas', styles.get("main_data_middle"))
        worksheet.write(9, 11, 'Prestamo', styles.get("main_data_bottom"))
        worksheet.write(6, 12, '', styles.get("main_data_top"))
        worksheet.write(7, 12, 'Subsidio de \nTransporte', styles.get("main_data_middle"))
        worksheet.write(8, 12, 'INSS \nPatronal', styles.get("main_data_middle"))
        worksheet.write(9, 12, 'INATEC', styles.get("main_data_bottom"))
        worksheet.write(6, 13, '', styles.get("main_data_top"))
        worksheet.write(7, 13, '', styles.get("main_data_middle"))
        worksheet.write(8, 13, 'Total \nDevengado', styles.get("main_data_middle"))
        worksheet.write(9, 13, 'Total \nDeducciones', styles.get("main_data_bottom"))
        worksheet.write(6, 14, '', styles.get("main_data_top_right"))
        worksheet.write(7, 14, '', styles.get("main_data_middle_right"))
        worksheet.write(8, 14, '', styles.get("main_data_middle_right"))
        worksheet.write(9, 14, 'Neto a Recibir', styles.get("main_data_bottom_right"))

        total_salario_ordinario = 0
        total_inss_laboral = 0
        total_antiguedad = 0
        total_ir = 0
        total_monto_feriado = 0
        total_issdhu_emergente = 0
        total_monto_carencia = 0
        total_monto_seguro = 0
        total_monto_ayecch = 0
        total_iniser = 0
        total_riesgo_profesional = 0
        total_adelanto_salario = 0
        total_monto_maternidad = 0
        total_issdhu_externo = 0
        total_monto_ayecsh = 0
        total_sindicato = 0
        total_horas_extras = 0
        total_embargo_alimenticio = 0
        total_otros_ingresos = 0
        total_embargo_ejecutivo = 0
        total_vacasiones_descansadas = 0
        total_otras_deducciones = 0
        #total_vacasiones_pagadas = 0
        total_prestamos = 0
        total_total_devengado = 0
        total_total_deducciones = 0
        total_neto_recibir = 0
        total_inss_patronal =0
        total_inatec = 0

        list_departmens = []
        lines_by_department = dict()
        for lines in self.slip_ids:
            if lines.contract_id.department_id.name in lines_by_department:
                lines_by_department[lines.contract_id.department_id.name].append(lines)
            else:
                lines_by_department[lines.contract_id.department_id.name] = []
                lines_by_department[lines.contract_id.department_id.name].append(lines)
                list_departmens.append(lines.contract_id.department_id.name)

        column = 10
        for names_departmens in list_departmens:
            worksheet.write(column, 0, 'Departamento de ' + names_departmens, styles.get("main_data_bold_dpto"))
            column += 1
            dep_total_salario_ordinario = 0
            dep_total_inss_laboral = 0
            dep_total_antiguedad = 0
            dep_total_ir = 0
            dep_total_monto_feriado = 0
            dep_total_issdhu_emergente = 0
            dep_total_monto_carencia = 0
            dep_total_monto_seguro = 0
            dep_total_monto_ayecch = 0
            dep_total_iniser = 0
            dep_total_riesgo_profesional = 0
            dep_total_adelanto_salario = 0
            dep_total_monto_maternidad = 0
            dep_total_issdhu_externo = 0
            dep_total_monto_ayecsh = 0
            dep_total_sindicato = 0
            dep_total_horas_extras = 0
            dep_total_embargo_alimenticio = 0
            dep_total_otros_ingresos = 0
            dep_total_embargo_ejecutivo = 0
            dep_total_vacasiones_descansadas = 0
            dep_total_otras_deducciones = 0
            #dep_total_vacasiones_pagadas = 0
            dep_total_prestamos = 0
            dep_total_total_devengado = 0
            dep_total_total_deducciones = 0
            dep_total_neto_recibir = 0
            dep_total_inss_patronal =0
            dep_total_inatec =0
            for lines in lines_by_department[names_departmens]:
                date_contract = str(lines.contract_id.date_start).split("-")
                worksheet.write(column, 0, lines.employee_id.x_studio_numero_de_empleado,
                                styles.get("main_data_middle"))
                worksheet.write(column, 1, lines.employee_id.display_name, styles.get("main_data_middle"))
                worksheet.write(column, 5, lines.employee_id.job_id.name, styles.get("main_data_middle"))
                worksheet.write(column, 7, lines.employee_id.identification_id, styles.get("main_data_middle"))
                worksheet.write(column, 8, lines.employee_id.x_studio_numero_inss, styles.get("main_data_middle"))
                worksheet.write(column, 10, date_contract[2] + "/" + date_contract[1] + "/" + date_contract[0],
                                styles.get("main_data_middle"))
                worksheet.write(column + 1, 0, lines.contract_id.wage, styles.get("currency_format"))
                salario_ordinario = self.find_rule_value(lines.line_ids, 'I101SAORD')
                worksheet.write(column + 2, 0, salario_ordinario, styles.get("currency_format"))
                total_salario_ordinario += salario_ordinario
                dep_total_salario_ordinario += salario_ordinario
                insslaboral = self.find_rule_value(lines.line_ids, 'D301INSSL')
                worksheet.write(column + 3, 0, insslaboral, styles.get("currency_format_bottom"))
                total_inss_laboral += insslaboral
                dep_total_inss_laboral += insslaboral
                worksheet.write(column + 1, 1, self.find_rule_value(lines.line_ids, 'I101PORANT'),
                                styles.get("currency_format"))
                antiguedad = self.find_rule_value(lines.line_ids, 'I102ANTIG') + self.find_rule_value(lines.line_ids,
                                                                                                      'I102ANTCAR') + self.find_rule_value(
                    lines.line_ids, 'I102ANT40%') + self.find_rule_value(lines.line_ids, 'I102ANT60%')
                worksheet.write(column + 2, 1, antiguedad,
                                styles.get("currency_format"))
                total_antiguedad += antiguedad
                dep_total_antiguedad += antiguedad
                ir = self.find_rule_value(lines.line_ids, 'D312IMPRE')
                worksheet.write(column + 3, 1, ir,
                                styles.get("currency_format_bottom"))
                total_ir += ir
                dep_total_ir += ir
                worksheet.write(column + 1, 2, self.find_rule_value(lines.line_ids, 'P007HFERI'),
                                styles.get("currency_format"))
                monto_feriado = self.find_rule_value(lines.line_ids, 'I101MFERI')
                worksheet.write(column + 2, 2, monto_feriado,
                                styles.get("currency_format"))
                total_monto_feriado += monto_feriado
                dep_total_monto_feriado += monto_feriado
                ISSDHU_Emergente = self.find_rule_value(lines.line_ids, 'D306ISDEM')
                worksheet.write(column + 3, 2, ISSDHU_Emergente,
                                styles.get("currency_format_bottom"))
                total_issdhu_emergente += ISSDHU_Emergente
                dep_total_issdhu_emergente += ISSDHU_Emergente
                worksheet.write(column + 1, 3, self.find_rule_value(lines.line_ids, 'P006DCARE'),
                                styles.get("currency_format"))
                monto_carencia = self.find_rule_value(lines.line_ids, 'I102MCARE')
                worksheet.write(column + 2, 3, monto_carencia,
                                styles.get("currency_format"))
                total_monto_carencia += monto_carencia
                dep_total_monto_carencia += monto_carencia
                monto_seguro = self.find_rule_value(lines.line_ids, 'D311IMSENIC') + self.find_rule_value(
                    lines.line_ids, 'D311IMSECONS3')
                worksheet.write(column + 3, 3, monto_seguro,
                                styles.get("currency_format_bottom"))
                total_monto_seguro += monto_seguro
                dep_total_monto_seguro += monto_seguro
                worksheet.write(column + 1, 4, self.find_rule_value(lines.line_ids, 'P007AECCH'),
                                styles.get("currency_format"))
                monto_ayecch = self.find_rule_value(lines.line_ids, 'I102MAECCH')
                worksheet.write(column + 2, 4, monto_ayecch,
                                styles.get("currency_format"))
                total_monto_ayecch += monto_ayecch
                dep_total_monto_ayecch += monto_ayecch
                iniser = self.find_rule_value(lines.line_ids, 'D313INISE')
                worksheet.write(column + 3, 4, iniser,
                                styles.get("currency_format_bottom"))
                total_iniser += iniser
                dep_total_iniser += iniser
                worksheet.write(column + 1, 5, self.find_rule_value(lines.line_ids, 'P007DIRPR'),
                                styles.get("currency_format"))
                riesgo_profesional = self.find_rule_value(lines.line_ids, 'I102MRIPR')
                worksheet.write(column + 2, 5, riesgo_profesional,
                                styles.get("currency_format"))
                total_riesgo_profesional += riesgo_profesional
                dep_total_riesgo_profesional += riesgo_profesional
                adelanto_salario = self.find_rule_value(lines.line_ids, 'D314ADSAL')
                worksheet.write(column + 3, 5, adelanto_salario,
                                styles.get("currency_format_bottom"))
                total_adelanto_salario += adelanto_salario
                dep_total_adelanto_salario += adelanto_salario
                worksheet.write(column + 1, 6, self.find_rule_value(lines.line_ids, 'P007DIMAT'),
                                styles.get("currency_format"))
                monto_maternidad = self.find_rule_value(lines.line_ids, 'B20360IMAT') + self.find_rule_value(
                    lines.line_ids, 'B20240IMAT')
                worksheet.write(column + 2, 6, monto_maternidad,
                                styles.get("currency_format"))
                total_monto_maternidad += monto_maternidad
                dep_total_monto_maternidad += monto_maternidad
                issdhu_externo = self.find_rule_value(lines.line_ids, 'D315ISDEX')
                worksheet.write(column + 3, 6, issdhu_externo,
                                styles.get("currency_format_bottom"))
                total_issdhu_externo += issdhu_externo
                dep_total_issdhu_externo += issdhu_externo
                worksheet.write(column + 1, 7, self.find_rule_value(lines.line_ids, 'P007DAECSH'),
                                styles.get("currency_format"))
                monto_ayecsh = self.find_rule_value(lines.line_ids, 'I102MAECSH')
                worksheet.write(column + 2, 7, monto_ayecsh,
                                styles.get("currency_format"))
                total_monto_ayecsh += monto_ayecsh
                dep_total_monto_ayecsh += monto_ayecsh
                sindicato = self.find_rule_value(lines.line_ids, 'D317SINDI')
                worksheet.write(column + 3, 7, sindicato,
                                styles.get("currency_format_bottom"))
                total_sindicato += sindicato
                dep_total_sindicato += sindicato
                worksheet.write(column + 1, 8, self.find_rule_value(lines.line_ids, 'P007CHEXT'),
                                styles.get("currency_format"))
                horas_extras = self.find_rule_value(lines.line_ids, 'I103HOEXT')
                worksheet.write(column + 2, 8, horas_extras,
                                styles.get("currency_format"))
                total_horas_extras += horas_extras
                dep_total_horas_extras += horas_extras
                embargo_alimenticio = self.find_rule_value(lines.line_ids, 'D318EMBAL')
                worksheet.write(column + 3, 8, embargo_alimenticio,
                                styles.get("currency_format_bottom"))
                total_embargo_alimenticio += embargo_alimenticio
                dep_total_embargo_alimenticio += embargo_alimenticio
                worksheet.write(column + 1, 9, "",
                                styles.get("currency_format"))
                otros_ingresos = self.find_rule_value(lines.line_ids, 'I105OTING')
                worksheet.write(column + 2, 9, otros_ingresos,
                                styles.get("currency_format"))
                total_otros_ingresos += otros_ingresos
                dep_total_otros_ingresos += otros_ingresos
                embargo_ejecutivo = self.find_rule_value(lines.line_ids, 'D319EMBEJ')
                worksheet.write(column + 3, 9, embargo_ejecutivo,
                                styles.get("currency_format_bottom"))
                total_embargo_ejecutivo += embargo_ejecutivo
                dep_total_embargo_ejecutivo += embargo_ejecutivo
                worksheet.write(column + 1, 10, self.find_rule_value(lines.line_ids, 'P003DVDES'),
                                styles.get("currency_format"))
                vacasiones_descansadas = self.find_rule_value(lines.line_ids, 'I106VADES')
                worksheet.write(column + 2, 10, vacasiones_descansadas,
                                styles.get("currency_format"))
                total_vacasiones_descansadas += vacasiones_descansadas
                dep_total_vacasiones_descansadas += vacasiones_descansadas
                otras_deducciones = self.find_rule_value(lines.line_ids, 'D321OTDED')
                worksheet.write(column + 3, 10, otras_deducciones,
                                styles.get("currency_format_bottom"))
                total_otras_deducciones += otras_deducciones
                dep_total_otras_deducciones += otras_deducciones
                worksheet.write(column + 1, 11, self.find_rule_value(lines.line_ids, 'P004DVPAG'),
                                styles.get("currency_format"))
                #vacasiones_pagadas = self.find_rule_value(lines.line_ids, 'I107VAPAG')
                #worksheet.write(column + 2, 11, vacasiones_pagadas,
                                #styles.get("currency_format"))
                #total_vacasiones_pagadas += vacasiones_pagadas
                #dep_total_vacasiones_pagadas += vacasiones_pagadas
                prestamos = self.find_rule_value(lines.line_ids, 'D321PREST')
                worksheet.write(column + 3, 11, prestamos,
                                styles.get("currency_format_bottom"))
                total_prestamos += prestamos
                dep_total_prestamos += prestamos

                worksheet.write(column + 1, 12, self.find_rule_value(lines.line_ids, 'I280MONST'),
                                styles.get("currency_format"))
                insspatronal = self.find_rule_value(lines.line_ids, 'C601INSSPAT')
                worksheet.write(column + 2, 12,insspatronal,
                                styles.get("currency_format"))
                dep_total_inss_patronal+=insspatronal
                total_inss_patronal+=insspatronal
                inatec = self.find_rule_value(lines.line_ids, 'C602INATEC')
                worksheet.write(column + 3, 12, inatec,
                                styles.get("currency_format_bottom"))
                dep_total_inatec+=inatec
                total_inatec+=inatec

                total_devengado = self.find_rule_value(lines.line_ids, 'B299TODEV')
                worksheet.write(column + 2, 13, total_devengado,
                                styles.get("currency_format"))
                total_total_devengado += total_devengado
                dep_total_total_devengado += total_devengado
                total_deducciones = self.find_rule_value(lines.line_ids, 'P010TODED')
                worksheet.write(column + 3, 13, total_deducciones,
                                styles.get("currency_format_bottom"))
                total_total_deducciones += total_deducciones
                dep_total_total_deducciones += total_deducciones
                neto_a_recibir = self.find_rule_value(lines.line_ids, 'N501NETO')
                worksheet.write(column + 3, 14, neto_a_recibir,
                                styles.get("currency_format_bottom"))
                total_neto_recibir += neto_a_recibir
                dep_total_neto_recibir += neto_a_recibir
                column += 4
            column += 1

            worksheet.write(column, 0, 'Total Departamento', styles.get("main_data_bold_dpto"))
            worksheet.write(column + 1, 0, dep_total_salario_ordinario, styles.get("currency_format"))
            worksheet.write(column + 2, 0, dep_total_inss_laboral, styles.get("currency_format"))
            worksheet.write(column + 1, 1, dep_total_antiguedad, styles.get("currency_format"))
            worksheet.write(column + 2, 1, dep_total_ir, styles.get("currency_format"))
            worksheet.write(column + 1, 2, dep_total_monto_feriado, styles.get("currency_format"))
            worksheet.write(column + 2, 2, dep_total_issdhu_emergente, styles.get("currency_format"))
            worksheet.write(column + 1, 3, dep_total_monto_carencia, styles.get("currency_format"))
            worksheet.write(column + 2, 3, dep_total_monto_seguro, styles.get("currency_format"))
            worksheet.write(column + 1, 4, dep_total_monto_ayecch, styles.get("currency_format"))
            worksheet.write(column + 2, 4, dep_total_iniser, styles.get("currency_format"))
            worksheet.write(column + 1, 5, dep_total_riesgo_profesional, styles.get("currency_format"))
            worksheet.write(column + 2, 5, dep_total_adelanto_salario, styles.get("currency_format"))
            worksheet.write(column + 1, 6, dep_total_monto_maternidad, styles.get("currency_format"))
            worksheet.write(column + 2, 6, dep_total_issdhu_externo, styles.get("currency_format"))
            worksheet.write(column + 1, 7, dep_total_monto_ayecsh, styles.get("currency_format"))
            worksheet.write(column + 2, 7, dep_total_sindicato, styles.get("currency_format"))
            worksheet.write(column + 1, 8, dep_total_horas_extras, styles.get("currency_format"))
            worksheet.write(column + 2, 8, dep_total_embargo_alimenticio, styles.get("currency_format"))
            worksheet.write(column + 1, 9, dep_total_otros_ingresos, styles.get("currency_format"))
            worksheet.write(column + 2, 9, dep_total_embargo_ejecutivo, styles.get("currency_format"))
            worksheet.write(column + 1, 10, dep_total_vacasiones_descansadas, styles.get("currency_format"))
            worksheet.write(column + 2, 10, dep_total_otras_deducciones, styles.get("currency_format"))
            #worksheet.write(column + 1, 11, dep_total_vacasiones_pagadas, styles.get("currency_format"))
            worksheet.write(column + 2, 11, dep_total_prestamos, styles.get("currency_format"))
            worksheet.write(column + 1, 12, dep_total_inss_patronal, styles.get("currency_format"))
            worksheet.write(column + 2, 12, dep_total_inatec, styles.get("currency_format"))
            worksheet.write(column + 1, 13, dep_total_total_devengado, styles.get("currency_format"))
            worksheet.write(column + 2, 13, dep_total_total_deducciones, styles.get("currency_format"))
            worksheet.write(column + 2, 14, dep_total_neto_recibir, styles.get("currency_format"))
            column += 4

        worksheet.set_row(column + 4, 28)
        worksheet.set_row(column + 5, 28)
        worksheet.set_column(column + 4, column + 4, 15)
        worksheet.set_column(column + 5, column + 5, 15)
        worksheet.write(column + 3, 0, 'Totales', styles.get("main_data_bold"))
        worksheet.write(column + 4, 0, 'Salario Ordinario', styles.get("main_data_middle"))
        worksheet.write(column + 5, 0, 'INSS Laboral', styles.get("main_data_bottom_left"))
        worksheet.write(column + 3, 1, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 1, 'Antiguedad', styles.get("main_data_middle"))
        worksheet.write(column + 5, 1, 'IR', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 2, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 2, 'Monto Feriado', styles.get("main_data_middle"))
        worksheet.write(column + 5, 2, 'ISSDHU Emergente', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 3, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 3, 'Monto Carencia', styles.get("main_data_middle"))
        worksheet.write(column + 5, 3, 'Monto Seguro', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 4, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 4, 'Monto AYECCH', styles.get("main_data_middle"))
        worksheet.write(column + 5, 4, 'INISER', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 5, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 5, 'Riesgo \nProfesional', styles.get("main_data_middle"))
        worksheet.write(column + 5, 5, 'Adelanto de \nSalario', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 6, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 6, 'Monto \nMaternidad', styles.get("main_data_middle"))
        worksheet.write(column + 5, 6, 'ISSDHU \nExterno', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 7, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 7, 'Monto \nAYECSH', styles.get("main_data_middle"))
        worksheet.write(column + 5, 7, 'Sindicato', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 8, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 8, 'Horas Extras', styles.get("main_data_middle"))
        worksheet.write(column + 5, 8, 'Embargo \nAlimenticio', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 9, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 9, 'Otros Ingresos', styles.get("main_data_middle"))
        worksheet.write(column + 5, 9, 'Embargo Ejecutivo', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 10, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 10, 'Vacaciones \nDescansadas', styles.get("main_data_middle"))
        worksheet.write(column + 5, 10, 'Otras \nDeduciones', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 11, '', styles.get("main_data_bold"))
        #worksheet.write(column + 4, 11, 'Vacaciones \nPagadas', styles.get("main_data_middle"))
        worksheet.write(column + 5, 11, 'Prestamo', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 12, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 12, 'INSS \nPatronal', styles.get("main_data_middle"))
        worksheet.write(column + 5, 12, 'INATEC', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 13, '', styles.get("main_data_bold"))
        worksheet.write(column + 4, 13, 'Total \nDevengado', styles.get("main_data_middle"))
        worksheet.write(column + 5, 13, 'Total \nDeducciones', styles.get("main_data_bottom"))
        worksheet.write(column + 3, 14, '', styles.get("main_data_top_right"))
        worksheet.write(column + 4, 14, '', styles.get("main_data_middle_right"))
        worksheet.write(column + 5, 14, 'Neto a Recibir', styles.get("main_data_bottom_right"))

        worksheet.write(column + 6, 0, total_salario_ordinario, styles.get("currency_format"))
        worksheet.write(column + 7, 0, total_inss_laboral, styles.get("currency_format"))
        worksheet.write(column + 6, 1, total_antiguedad, styles.get("currency_format"))
        worksheet.write(column + 7, 1, total_ir, styles.get("currency_format"))
        worksheet.write(column + 6, 2, total_monto_feriado, styles.get("currency_format"))
        worksheet.write(column + 7, 2, total_issdhu_emergente, styles.get("currency_format"))
        worksheet.write(column + 6, 3, total_monto_carencia, styles.get("currency_format"))
        worksheet.write(column + 7, 3, total_monto_seguro, styles.get("currency_format"))
        worksheet.write(column + 6, 4, total_monto_ayecch, styles.get("currency_format"))
        worksheet.write(column + 7, 4, total_iniser, styles.get("currency_format"))
        worksheet.write(column + 6, 5, total_riesgo_profesional, styles.get("currency_format"))
        worksheet.write(column + 7, 5, total_adelanto_salario, styles.get("currency_format"))
        worksheet.write(column + 6, 6, total_monto_maternidad, styles.get("currency_format"))
        worksheet.write(column + 7, 6, total_issdhu_externo, styles.get("currency_format"))
        worksheet.write(column + 6, 7, total_monto_ayecsh, styles.get("currency_format"))
        worksheet.write(column + 7, 7, total_sindicato, styles.get("currency_format"))
        worksheet.write(column + 6, 8, total_horas_extras, styles.get("currency_format"))
        worksheet.write(column + 7, 8, total_embargo_alimenticio, styles.get("currency_format"))
        worksheet.write(column + 6, 9, total_otros_ingresos, styles.get("currency_format"))
        worksheet.write(column + 7, 9, total_embargo_ejecutivo, styles.get("currency_format"))
        worksheet.write(column + 6, 10, total_vacasiones_descansadas, styles.get("currency_format"))
        worksheet.write(column + 7, 10, total_otras_deducciones, styles.get("currency_format"))
        #worksheet.write(column + 6, 11, total_vacasiones_pagadas, styles.get("currency_format"))
        worksheet.write(column + 7, 11, total_prestamos, styles.get("currency_format"))
        worksheet.write(column + 6, 12, total_inss_patronal, styles.get("currency_format"))
        worksheet.write(column + 7, 12, total_inatec, styles.get("currency_format"))
        worksheet.write(column + 6, 13, total_total_devengado, styles.get("currency_format"))
        worksheet.write(column + 7, 13, total_total_deducciones, styles.get("currency_format"))
        worksheet.write(column + 7, 14, total_neto_recibir, styles.get("currency_format"))

        worksheet.write(column + 13, 1, 'ELABORADO POR', styles.get("main_data_bold"))
        worksheet.write(column + 13, 6, 'REVISADO POR', styles.get("main_data_bold"))
        worksheet.write(column + 13, 11, 'AUTORIZADO POR', styles.get("main_data_bold"))

        workbook.close()

        with open(file_path, 'rb') as r:
            xls_file = base64.b64encode(r.read())
        att_vals = {
            'name': u"{}#{}.xlsx".format(self.name, fields.Date.today()),
            'type': 'binary',
            'datas': xls_file,
            'datas_fname': u"{}#{}.xlsx".format(self.name, fields.Date.today()),
        }
        attachment_id = self.env['ir.attachment'].create(att_vals)
        self.env.cr.commit()
        action = {
            'type': 'ir.actions.act_url',
            'url': '/web/content/{}?download=true'.format(attachment_id.id, ),
            'target': 'self',
        }
        return action



