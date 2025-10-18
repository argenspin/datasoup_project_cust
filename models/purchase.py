from odoo import fields,models,api

class ProjectPurchase(models.Model):
    _inherit = 'purchase.order'

    def _get_default_project_id(self):
        return self.env.context.get('default_project_id')
    
    project_id = fields.Many2one('project.project',string="Project" ,domain="[('company_id', '=', current_company_id)]", default = _get_default_project_id)

    def _prepare_invoice(self):
        """Prepare the dict of values to create the new invoice for a purchase order.
        """
        self.ensure_one()
        invoice_vals = super()._prepare_invoice()
        invoice_vals.update({
            'project_id': self.project_id.id,
        })
        return invoice_vals