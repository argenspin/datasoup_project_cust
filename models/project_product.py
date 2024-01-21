from odoo.exceptions import ValidationError
from odoo import fields,models,api,_
from odoo.exceptions import ValidationError

class ProjectProductLine(models.Model):
    _rec_name = "sale_product_name"
    _name = "project.product.line"

    def _get_default_project_id(self):
        return self.env.context.get('default_project_id')
    
    project_id = fields.Many2one('project.project',string="Project",default=_get_default_project_id, ondelete="cascade")
    sale_order_id = fields.Many2one('sale.order', string="Sale Order", ondelete="cascade")
    sale_line_id = fields.Many2one('sale.order.line', string="Sale Line", ondelete='cascade')
    product_template_id = fields.Many2one('product.template', string="Product", related="sale_line_id.product_template_id", store=True)
    sale_product_name = fields.Text(string="Product Description", related="sale_line_id.name")
    product_id = fields.Many2one('product.product', string="Reference Product")
    mrp_order = fields.Many2one('mrp.production',string="Manufacturing Order")
    state = fields.Selection(string="Status",selection=[('mrp_to_do','To Manufacture'),('mrp_order','Order Created'),('mrp_confirm','Order Confirmed'), ('mrp_in_progress','In Progress'),('mrp_to_close','To Close'),('mrp_complete','Manufacturing Completed'),('order_cancel','Order Cancelled')], default="mrp_to_do", compute="_compute_state")
    def action_create_mrp_order(self):
        bom = self.env['mrp.bom'].search([('product_tmpl_id','=',self.product_template_id.id)])
        if bom:

            return {
                'name': _("Manufacturing Order"),
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.production',
                'view_mode': 'form',
                'context':{
                    'default_product_id': self.product_id.id,
                    'default_project_id': self.project_id.id,
                    'default_bom_id': bom.id,
                    'default_project_product_line_id':self.id,
                }
            }
        else:
            raise ValidationError("Cannot find any Bill of Materials for this product")
        
    @api.depends('mrp_order','mrp_order.state')
    def _compute_state(self):
        for record in self:
            record.state = 'mrp_to_do'
            if record.mrp_order:
                record.state = 'mrp_order'
                if record.mrp_order.state=='cancel':
                    record.state = 'order_cancel'
                elif record.mrp_order.state=='progress' or record.mrp_order.state=='to_close':
                    record.state= 'mrp_in_progress'
                elif record.mrp_order.state=='confirmed':
                    record.state= 'mrp_confirm'
                elif record.mrp_order.state=='done':
                    record.state = 'mrp_complete'

    def action_view_mrp_order(self):
        if self.mrp_order:
            return {
                'name': _("Manufacturing Order"),
                'type': 'ir.actions.act_window',
                'res_model': 'mrp.production',
                'view_mode': 'form',
                'res_id': self.mrp_order.id
            }
        else: 
            raise ValidationError("Cannot find any manufacturing order associated with this product!")
