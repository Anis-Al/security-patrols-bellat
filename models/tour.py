from odoo import models, fields, api

class Tour(models.Model):
    _name = 'security.tour'
    _description = 'Security Tour'
    _order = 'date desc, start_time desc'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    site_id = fields.Many2one('security.site', string='Site', required=True)
    checkpoint_ids = fields.One2many('security.tour.line', 'tour_id', string='Checkpoints')
    
    frequency = fields.Selection([
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly')
    ], string='Frequency', default='daily', required=True)

    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    start_time = fields.Float(string='Start Time', required=True)
    end_time = fields.Float(string='End Time', required=True)
    
    agent_id = fields.Many2one('hr.employee', string='Assigned Agent', domain="[('is_agent', '=', True)]", required=True)
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('finished', 'Finished')
    ], string='Status', default='draft', required=True)
    
    grace_period = fields.Integer(string='Grace Period (min)', default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('security_patrol.default_round_grace_period', 15)))
    strict_ordering = fields.Boolean(string='Strict Ordering', default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.enforce_sequential_scans') == 'True')
    incident_email = fields.Char(string='Incident Email', default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.incident_notification_email'))
    require_selfie = fields.Boolean(string='Require Selfie', default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.require_selfie') == 'True')
    require_photo_place = fields.Boolean(string='Require Photo of Place', default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.require_photo_place') == 'True')
    
    log_ids = fields.One2many('security.tour.log', 'tour_id', string='Logs')
    
    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('security.tour') or 'New'
        return super(Tour, self).create(vals)

class TourLine(models.Model):
    _name = 'security.tour.line'
    _description = 'Tour Checkpoint Line'
    _order = 'sequence, id'

    tour_id = fields.Many2one('security.tour', string='Tour', required=True, ondelete='cascade')
    checkpoint_id = fields.Many2one('security.checkpoint', string='Checkpoint', required=True)
    sequence = fields.Integer(string='Sequence', default=1)


