from odoo.exceptions import ValidationError
from odoo import fields,models,api

# class Productproject(models.Model):
#     _inherit="product.template"

#     def _get_default_project_id(self):
#         if self.env.context.get('default_project_id'):
#             return [self.env.context.get('default_project_id')]
#         else:
#             return []
#     project_ids = fields.Many2many(
#         'project.project', company_dependent=False ,store = True, default=_get_default_project_id,
#         domain="[('company_id', '=', current_company_id)]",
#         help='Select a billable project on which tasks can be created. This setting must be set for each company.')


class ProjectProductLine(models.Model):
    _name = "project.product.line"

    def _get_default_project_id(self):
        return self.env.context.get('default_project_id')
    
    project_id = fields.Many2one('project.project',string="Project",default=_get_default_project_id)
    product_id = fields.Many2one('product.template', string="Product")
    default_code = fields.Char("Internal Reference",related="product_id.default_code")
    responsible_id = fields.Many2one("res.users",string="Responsible", related="product_id.responsible_id")
    product_tag_ids = fields.Many2many("product.tag",string="Product Tags", related="product_id.product_tag_ids")
    list_price = fields.Float(string="Sales Price",related="product_id.list_price")
    standard_price = fields.Float(string="Cost Price",related="product_id.standard_price")
    categ_id = fields.Many2one("product.category",string="Product Category",related="product_id.categ_id")
    qty_available = fields.Float(string="Quantity Available",related="product_id.qty_available")
    virtual_available = fields.Float(string="Forecasted Quantity",related="product_id.virtual_available")