from odoo import fields,models,api,_

class Projectsale(models.Model):
    _inherit = 'sale.order'

    def _get_default_project_id(self):
        return self.env.context.get('default_project_id')
    
    project_id = fields.Many2one('project.project',string="Project" ,default = _get_default_project_id, domain="[('company_id', '=', current_company_id)]", tracking=True)

    def action_create_project(self):
        new_project = self.env['project.project'].create({
            'name': 'Draft Project',
            'is_favorite': False,
            'partner_id': self.partner_id.id,
        }
        )
        for line in self.order_line:
            if not line.display_type and line.product_template_id.detailed_type=='product':
                self.env['project.product.line'].create({
                    'product_template_id': line.product_template_id.id,
                    'product_id' : line.product_id.id,
                    'sale_product_name': line.name,
                    'project_id': new_project.id,
                    'sale_order_id': self.id,
                    'sale_line_id': line.id,
                })
        
        self.project_id = new_project.id

        return {
            'name': _("Projects"),
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'res_id': new_project.id,
            'view_mode': 'form,tree',
        }
    

    def action_assign_project(self):

        return {
            'name': _('Assign Project'),
            'res_model': 'sale.assign.project.wizard',
            'view_mode': 'form',
            'context': {
                'default_sale_order_id': self.id,
                'default_partner_id': self.partner_id.id
            },
            'target': 'new',
            'type': 'ir.actions.act_window',
        }
    
    def action_view_project(self):

        return {
            'name': _("Projects"),
            'type': 'ir.actions.act_window',
            'res_model': 'project.project',
            'res_id': self.project_id.id,
            'view_mode': 'form,tree',
        }
    
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def create(self,vals):
        new_line = super(SaleOrderLine,self).create(vals)
        if new_line.order_id.project_id:
            self.env['project.product.line'].create({
                'product_template_id': new_line.product_template_id.id,
                'product_id' : new_line.product_id.id,
                'sale_product_name': new_line.name,
                'project_id': new_line.order_id.project_id.id,
                'sale_order_id': new_line.order_id.id,
                'sale_line_id': new_line.id,
            })
        return new_line

    
    @api.onchange('name')
    def _onchange_product_name(self):
        if self.order_id.project_id:
            project_product_line = self.env['project.product.line'].search([('sale_line_id','=',self.id)])
            project_product_line.write({
                'product_template_id': self.product_template_id.id,
                'product_id' : self.product_id.id,
                'sale_product_name': self.name,
                'project_id': self.order_id.project_id.id,
                'sale_order_id': self.order_id.id,
                'sale_line_id': self.id,
            }) 
