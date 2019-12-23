
{
    'name': "vit_asset_tax",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Vit Training",
    'website': "http://www.vitraining.com",

    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base','om_account_accountant','vit_asset'],
    'data': [
        'views/views.xml',
        # 'views/templates.xml',
    ],
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}