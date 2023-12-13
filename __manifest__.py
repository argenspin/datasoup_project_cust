{
    'name': "Datasoup Project Extensions",
    'version': '1.0',
    'summary': "Integration of Sales, Purchase and Manufacturing apps with Project",
    'description': "Connects Project with Sales, Manufacturing and Inventory",
    'author':'DataSoup',
    'category': 'Services/Project',
    'depends': ['stock','product','purchase','sale','sale_management','mrp','project'],
    'data': [
        'security/ir.model.access.csv',
        'views/project_extended_views.xml',
    ],
    
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
