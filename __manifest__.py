# -*- coding: utf-8 -*-
{
    'name': "Workshop TR",

    'summary': """Workshop TR""",

    'description': """
        Workshop TR
    """,

    'author': "James",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        #'templates.xml',
        'wizard/wizard_mark_done.xml',
        'wizard/wizard_tranferdate_amount.xml',
        'wizard/open_wizard_delete.xml',
        'views/open_tr.xml',
        #'views/sales_order.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo.xml',
    ],
}