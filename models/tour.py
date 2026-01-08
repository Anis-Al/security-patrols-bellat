# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Tour(models.Model):
    _name = 'security.tour'
    _description = 'Security Tour'
    _order = 'date asc , start_time asc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    template_id = fields.Many2one('security.tour.template', string='Template')
    site_id = fields.Many2one('security.site', string='Site', required=True)
    checkpoint_ids = fields.One2many('security.tour.line', 'tour_id', string='Checkpoints')
    
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    
    superviser_id = fields.Many2one('res.users', string='Superviser', readonly=True)
    agent_id = fields.Many2one('hr.employee', string='Assigned Agent', domain="[('is_agent', '=', True)]", readonly=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished')
    ], string='Status', default='draft', required=True, group_expand='_group_expand_states')
    
    grace_period = fields.Integer(string='Grace Period (min)', 
    default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('security_patrol.default_round_grace_period', 15)))
    
    strict_ordering = fields.Boolean(string='Strict Ordering', 
    default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.enforce_sequential_scans') == 'True')
    
    incident_email = fields.Char(string='Incident Email', 
    default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.incident_notification_email'))
    
    require_selfie = fields.Boolean(string='Require Selfie', 
    default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.require_selfie') == 'True')
    
    require_photo_place = fields.Boolean(string='Require Photo of Place', 
    default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.require_photo_place') == 'True')
    
    max_checkpoint_distance = fields.Integer(string='Max Checkpoint Distance (m)', 
    default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('security_patrol.max_checkpoint_distance', 50)))
    
    log_ids = fields.One2many('security.tour.log', 'tour_id', string='Logs')

    def _check_completion(self):
        self.ensure_one()
        if self.state != 'in_progress':
            return
        
        required_checkpoints = self.checkpoint_ids.mapped('checkpoint_id')
        logged_checkpoints = self.log_ids.mapped('checkpoint_id')
        
        if all(cp in logged_checkpoints for cp in required_checkpoints):
            self.state = 'finished'

    @api.model
    def _group_expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    @api.onchange('site_id')
    def _onchange_site_id(self):
        if not self.template_id:
            self.checkpoint_ids = [(5, 0, 0)]
    
    @api.model
    def create(self, vals):
        if not vals.get('name') or vals.get('name') == 'New':
            pass
        if not vals.get('superviser_id'):
            vals['superviser_id'] = self.env.user.id
        return super(Tour, self).create(vals)

class TourLine(models.Model):
    _name = 'security.tour.line'
    _description = 'Tour Checkpoint Line'
    _order = 'sequence, id'

    tour_id = fields.Many2one('security.tour', string='Tour', required=True, ondelete='cascade')
    checkpoint_id = fields.Many2one('security.checkpoint', string='Checkpoint', required=True)
    sequence = fields.Integer(string='Sequence', default=1)


