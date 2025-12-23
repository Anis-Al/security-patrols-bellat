from odoo import models, fields, api


class Incident(models.Model):
    _name = 'security.incident'
    _description = 'Security Incident'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'
    _rec_name = 'title'

    log_id = fields.Many2one('security.tour.log', string='Log Entry', required=True, ondelete='cascade')
    tour_id = fields.Many2one(related='log_id.tour_id', string='Tour', store=True, readonly=True)
    checkpoint_id = fields.Many2one(related='log_id.checkpoint_id', string='Checkpoint', store=True, readonly=True)
    site_id = fields.Many2one(related='checkpoint_id.site_id', string='Site', store=True, readonly=True)
    
    title = fields.Char(string='Title', required=True)
    description = fields.Text(string='Description')
    
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ], string='Severity', required=True, default='medium')
    
    category = fields.Selection([
        ('security', 'Security Breach'),
        ('safety', 'Safety Hazard'),
        ('maintenance', 'Maintenance Issue'),
        ('vandalism', 'Vandalism'),
        ('suspicious', 'Suspicious Activity'),
        ('other', 'Other')
    ], string='Category', required=True, default='other')
    
    photo_ids = fields.Many2many('ir.attachment', string='Photos')
    
    status = fields.Selection([
        ('reported', 'Reported'),
        ('acknowledged', 'Acknowledged'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed')
    ], string='Status', default='reported', required=True, tracking=True)
    
    reported_by = fields.Many2one(related='log_id.tour_id.agent_id', string='Reported By', store=True, readonly=True)
    reported_date = fields.Datetime(string='Reported Date', default=fields.Datetime.now, readonly=True)
    
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    resolution_notes = fields.Text(string='Resolution Notes')
    resolved_date = fields.Datetime(string='Resolved Date', readonly=True)
    
    priority = fields.Selection([
        ('0', 'Low'),
        ('1', 'Normal'),
        ('2', 'High'),
        ('3', 'Urgent')
    ], string='Priority', default='1')

    @api.onchange('status')
    def _onchange_status(self):
        if self.status == 'resolved' and not self.resolved_date:
            self.resolved_date = fields.Datetime.now()
