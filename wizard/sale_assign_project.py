from odoo import models,fields,api,_

class SaleAssignProjectWizard(models.Model):
    _name = "sale.assign.project.wizard"

    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
    partner_id = fields.Many2one('res.partner', string="Customer")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        return {'domain': {'project_id': [('partner_id','=',self.partner_id.id)]}}
    project_id = fields.Many2one("project.project", string="Project to Assign", required=True, domain="[('partner_id','=',partner_id)]")

    def action_assign_project(self):

        for line in self.sale_order_id.order_line:
            if not line.display_type and line.product_template_id.detailed_type=='product':
                self.env['project.product.line'].create({
                    'product_template_id': line.product_template_id.id,
                    'product_id': line.product_id.id,
                    'project_id': self.project_id.id,
                    'sale_order_id': self.sale_order_id.id,
                    'sale_line_id': line.id,
                })
        
        self.sale_order_id.project_id = self.project_id.id

        # return {
        #     'name': _("Projects"),
        #     'type': 'ir.actions.act_window',
        #     'res_model': 'project.project',
        #     'res_id': self.project_id.id,
        #     'view_mode': 'form,tree',
        # }
    