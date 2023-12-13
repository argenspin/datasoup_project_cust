from odoo.exceptions import ValidationError
from odoo import fields,models,api
import logging

class Projectdocument(models.Model):
    _inherit="project.project"

    sale_order_ids = fields.One2many('sale.order','project_id',string="Sales Orders")
    sale_order_count = fields.Integer(compute='_compute_sale_order_count')

    @api.depends('sale_order_ids')
    def _compute_sale_order_count(self):
        read_group = self.env['sale.order'].read_group([('project_id', 'in', self.ids)], ['project_id'], ['project_id'])
        mapped_count = {group['project_id'][0]: group['project_id_count'] for group in read_group}
        for project in self:
            project.sale_order_count = mapped_count.get(project.id, 0)

    purchase_order_ids = fields.One2many('purchase.order','project_id',string="Purchases")
    purchase_order_count = fields.Integer(compute='_compute_purchase_order_count')

    @api.depends('purchase_order_ids')
    def _compute_purchase_order_count(self):
        read_group = self.env['purchase.order'].read_group([('project_id', 'in', self.ids)], ['project_id'], ['project_id'])
        mapped_count = {group['project_id'][0]: group['project_id_count'] for group in read_group}
        for project in self:
            project.purchase_order_count = mapped_count.get(project.id, 0)


    mrp_production_ids = fields.One2many('mrp.production','project_id',string="Manufacturing Orders")
    mrp_production_count = fields.Integer(compute='_compute_mrp_order_count')

    @api.depends('mrp_production_ids')
    def _compute_mrp_order_count(self):
        read_group = self.env['mrp.production'].read_group([('project_id', 'in', self.ids)], ['project_id'], ['project_id'])
        mapped_count = {group['project_id'][0]: group['project_id_count'] for group in read_group}
        for project in self:
            project.mrp_production_count = mapped_count.get(project.id, 0)

    product_ids = fields.One2many('project.product.line','project_id',string="Product Lines")
    product_count = fields.Integer(compute='_compute_product_count')

    def _compute_product_count(self):
        for project in self:
            project.product_count = 0
            if project.product_ids:
                project.product_count = len(project.product_ids)
        

    def add_existing_products(self):
        logger = logging.getLogger("Project debug")
        active_ids = self.env.context.get('active_ids')
        logger.error("active_ids" + str(active_ids))
