
{
    'name': "vit_asset_tax",

    'summary': """
        Dependency om_account_accountant as Accounting module to vit_asset as Asset module including function taxes, analytic account, assets, products, and etc.
        Module om_account_accountant(Accounting) and vit_asset(Asset) must be installed to use all the function in module vit_asset_tax.""",
        
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