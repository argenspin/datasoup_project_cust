from odoo import fields,models,api

class MrpPrduction(models.Model):
    _inherit = 'mrp.production'

    def _get_default_project_id(self):
        return self.env.context.get('default_project_id')
    
    project_id = fields.Many2one('project.project',string="Project" ,domain="[('company_id', '=', current_company_id)]", default = _get_default_project_id)

    project_product_line_id = fields.Many2one("project.product.line", string="Product in Project", readonly=True)

    product_name = fields.Text(string="Product Name", compute='_compute_product_name')

    # @api.depends('project_product_line_id','product_id')
    def _compute_product_name(self):
        for record in self:
            if record.project_product_line_id:
                record.product_name = record.project_product_line_id.sale_product_name
            else:
                record.product_name = record.product_id.name

    # def button_mark_done(self):
    #     res = super(MrpPrduction,self).button_mark_done()
    #     if self.project_product_line_id:
    #         self.project_product_line_id.write({'state':'mrp_complete'})
    #     return res
    
    @api.model
    def create(self,vals):
        new_order = super(MrpPrduction,self).create(vals)
        if new_order.project_product_line_id:
            new_order.project_product_line_id.write({'mrp_order': new_order.id})
        return new_order