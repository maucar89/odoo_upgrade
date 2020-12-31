# -*- coding: utf-8 -*-
{
    'name': 'Facturacion Computarizada',
    'version': '1.5.1',
    'category': 'Account',
    'summary': 'Facturacion aprobada por el SIN Bolivia',
    'author': 'Mauricio Carreño S.',
    'website': 'http://www.odoo.org.bo',
    'depends': ['account','sale','base','purchase'],
    'data': ['views/control_code_view.xml',
    'views/res_partner_view.xml',
    'views/amount_in_words.xml'],
    'images': ['static/description/background.png'],
    'installable': True,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
