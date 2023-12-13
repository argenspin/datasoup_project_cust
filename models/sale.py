from odoo import fields,models,api

class Projectsale(models.Model):
    _inherit = 'sale.order'

    def _get_default_project_id(self):
        return self.env.context.get('default_project_id')
    
    project_id = fields.Many2one('project.project',string="Project" ,default = _get_default_project_id, domain="[('company_id', '=', current_company_id)]")
