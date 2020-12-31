# -*- coding: utf-8 -*-
import openerp.tools
from odoo import models, fields, api, _
from openerp.tools.translate import _
from controlcode import ControlCode
from datetime import datetime
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, float_compare


class account_journal(models.Model):

    _inherit = "account.journal"

    fecha_limite = fields.Date('Limite de emision',help = 'La fecha presente en la dosificacion')
    autorizacion_dosificacion = fields.Char('Autorizacion',help = 'Autorizacion presente en la dosificacion')
    llave_dosificacion = fields.Char('Llave',help = 'Llave presente en la dosificacion')
    direccion_sucursal = fields.Text('Direccion Casa Matriz',help = 'Es la direccion, telefonos, ciudad de la Casa Matriz que aparece en las facturas')
    direccion_sucursal_2 = fields.Text('Direccion de la Sucursal',help = 'Es la direccion, telefonos, ciudad de la sucursal que aparece en las facturas')
    actividad_dosificacion = fields.Char('Actividad',help = 'Actividad de contribuyente')
    leyenda_dosificacion = fields.Text('Leyenda de la factura',help = 'Leyenda de la factura')
    leyenda_secundaria = fields.Text('Leyenda de la dosificacion',help = 'Leyenda secundaria de la dosificacion')
    nit_contribuyente = fields.Char('Nit del Contribuyente',help = 'Nit del contribuyente')
    nombre_sucursal = fields.Char('CASA MATRIZ',help = 'Nombre de la sucural, ejemplo CASA MATRIZ o SUCURSAL 8')
    nombre_sucursal_2 = fields.Char('SUCURSAL',help = 'Nombre de la sucural, ejemplo SUCURSAL 8')
    dosificacion = fields.Boolean('Dosificacion',help = 'Se usa el diario como dosificacion para facturas')
    mensaje_factura = fields.Char('Mensaje en Factura',help = 'Mensaje que se imprime en todas las facturas en la parte inferior')
    razon_social = fields.Char('Razon Social',help = 'Razon Social o Nombre Comercial')
    nombre_unipersonal = fields.Char('Nombre Unipersonal',help = 'Nombre Unipersonal')
    titulo = fields.Char('Titulo de la factura',help = 'Ejemplo FACTURA o FACTURA TURISTICA')
    subtitulo = fields.Char('Subtitulo de la factura',help = 'Ejemplo No valido para credito fiscal')
    estado_factura = fields.Char('estado_factura',help = 'V = Valido | A = Anulado', default="V")
    separador_qr = fields.Char('separador',help = 'Separador para QR', default="|")


class account_invoice(models.Model):

    _inherit = "account.invoice"
    _order = 'id desc'

    nit = fields.Char(related='partner_id.nit', string="NIT",store=True)
    code = fields.Char('Codigo de Control',size=64,help = 'Codigo de control valido para el SIN',readonly=True)
    autorizacion = fields.Char(related='journal_id.autorizacion_dosificacion', string="Autorizacion",store=True,readonly=True)
    llave = fields.Char(related='journal_id.llave_dosificacion',string="Llave de la dosificacion",store=True,readonly=True)
    fecha = fields.Date(related='journal_id.fecha_limite',string="Limite de emision",store=True,readonly=True)
    direccion = fields.Text(related='journal_id.direccion_sucursal',string="Direccion de la Casa Matriz",store=True,readonly=True)
    direccion_2 = fields.Text(related='journal_id.direccion_sucursal_2',string="Direccion de la sucursal",store=True,readonly=True)
    actividad = fields.Char(related='journal_id.actividad_dosificacion',string="Actividad del contribuyente",store=True,readonly=True)
    leyenda = fields.Text(related='journal_id.leyenda_dosificacion',string="Leyenda de la factura",store=True,readonly=True)
    leyenda2 = fields.Text(related='journal_id.leyenda_secundaria',string="Leyenda de la dosificacion",store=True,readonly=True)
    nit_empresa = fields.Char(related='journal_id.nit_contribuyente',string="Nit contribuyente",store=True,readonly=True)
    sucursal = fields.Char(related='journal_id.nombre_sucursal',string="Casa Matriz",store=True,readonly=True)
    sucursal_2 = fields.Char(related='journal_id.nombre_sucursal_2',string="Nombre de la sucursal",store=True,readonly=True)
    mensaje = fields.Char(related='journal_id.mensaje_factura',string="Mensaje Opcional",store=True,readonly=True)
    razon = fields.Char(related='journal_id.razon_social',string="Razon Social",store=True,readonly=True)
    unipersonal = fields.Char(related='journal_id.nombre_unipersonal',string="Unipersonal",store=True,readonly=True)
    factura_titulo = fields.Char(related='journal_id.titulo',string="Titulo",store=True,readonly=True)
    factura_subtitulo = fields.Char(related='journal_id.subtitulo',string="Sub Titulo",store=True,readonly=True)
    operador = fields.Char(related='partner_id.res_operador',string="Observaciones",store=True)
    estado_factura = fields.Char(related='journal_id.estado_factura',string="Estado Factura",store=True,readonly=True)
    separador_qr = fields.Char(related='journal_id.separador_qr',string="Separador QR",store=True,readonly=True)


    _sql_constraints = [
         ('number_uniq', 'Check(1=1)', 'Nro unico'),
    ]


    @api.multi
    def invoice_validate(self):
        res = super(account_invoice, self).invoice_validate()
        for inv in self:
            dt = datetime.strptime(inv.date_invoice, DEFAULT_SERVER_DATE_FORMAT)
            inv_date = datetime.strftime(dt,'%Y/%m/%d')
            cc = ControlCode(inv.autorizacion, inv.llave)
            cc.set_date(inv_date) \
            .set_nit(int(inv.nit))

            inv_num = inv.number
            split_invoice = inv_num.split("/")
            int_inv_num = split_invoice[-1:]
            number = int(str(int_inv_num[0]))

            control_code = cc.generate(number, inv.amount_total_company_signed)
            if not inv_date or not number or not inv.amount_total_company_signed:
                self.write({'code':'No valido para crédito fiscal'})
            else:
                self.write({'code':control_code})
        return res


class ResCurrency(models.Model):

    _inherit= 'res.currency'

    currency_unit_label = fields.Char("Currency Unit")
    currency_subunit_label = fields.Char("Currency Subunit", default="/100 Bs.")

    amount_separator = fields.Char("Unit/Subunit Separator Text", default="con")
    close_financial_text = fields.Char("Close Financial Text")
