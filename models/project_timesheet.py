from odoo import models, fields, api

class ProjectTimesheet(models.Model):
    _name = 'project.timesheet'
    project_id = fields.Many2one('project.project', string="Project")
    date = fields.Date(string="Date", default=fields.Date.context_today)
    total_hours = fields.Float(string="Total Hours", compute="_compute_total_hours")
    total_employees = fields.Integer(string="Total Employees", compute="_compute_total_employees")
    timesheet_line_ids = fields.One2many('project.timesheet.line', 'timesheet_id', string="Timesheet Lines")
    description = fields.Text(string="Description")

    @api.depends('timesheet_line_ids.hours', 'timesheet_line_ids')
    def _compute_total_hours(self):
        for record in self:
            record.total_hours = sum(line.hours for line in record.timesheet_line_ids)

    @api.depends('timesheet_line_ids.employee_id', 'timesheet_line_ids')
    def _compute_total_employees(self):
        for record in self:
            record.total_employees = len(set(line.employee_id for line in record.timesheet_line_ids if line.employee_id))

class ProjectTimesheetLine(models.Model):
    _name = 'project.timesheet.line'
    date = fields.Date(string="Date", related="timesheet_id.date", store=True)
    employee_id = fields.Many2one('hr.employee', string="Employee", required=True)
    timesheet_id = fields.Many2one('project.timesheet', string="Timesheet")
    task_id = fields.Many2one('project.task', string="Task")
    hours = fields.Float(string="Hours")
    description = fields.Text(string="Description")

class Project(models.Model):
    _inherit = 'project.project'
    project_timesheet_ids = fields.One2many('project.timesheet', 'project_id', string="Timesheets")
    total_timesheet_hours = fields.Float(string="Total Timesheet Hours", compute="_compute_total_timesheet_hours")

    @api.depends('project_timesheet_ids.total_hours')
    def _compute_total_timesheet_hours(self):
        for project in self:
            project.total_timesheet_hours = sum(timesheet.total_hours for timesheet in project.project_timesheet_ids)