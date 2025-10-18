from odoo import models,fields,api

class AccountMoveInherit(models.Model):
    _inherit="account.move"

    project_id = fields.Many2one('project.project', string="Project", store=True,)