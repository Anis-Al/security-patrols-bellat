from odoo import models, fields, api, _
from datetime import timedelta

class TourTemplate(models.Model):
    _name = 'security.tour.template'
    _inherit = ['security.tour.config.mixin']
    _description = 'Security Tour Template'

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    title = fields.Char(string='Title', required=True)
    site_id = fields.Many2one('security.site', string='Site', required=True)
    superviser_id = fields.Many2one('res.users', string='Superviser', readonly=True)
    agent_id = fields.Many2one('hr.employee', string='Assigned Agent', domain="[('is_agent', '=', True)]")
    checkpoint_ids = fields.One2many('security.tour.template.line', 'template_id', string='Checkpoints')
    
    frequency = fields.Selection([
        ('manual', 'Manual'),
        ('daily', 'Daily'),
        ('weekly', 'Weekly')
    ], string='Frequency', default='daily', required=True)

    start_date = fields.Date(string='Start Date', default=fields.Date.context_today)
    end_date = fields.Date(string='End Date')

    start_time = fields.Float(string='Expected Start Time')
    end_time = fields.Float(string='Expected End Time')

    active = fields.Boolean(default=True)
    tour_count = fields.Integer(string='Tour Count', default=0, copy=False)

    @api.onchange('site_id')
    def _onchange_site_id(self):
        self.checkpoint_ids = [(5, 0, 0)]

    def action_load_all_checkpoints(self):
        self.ensure_one()
        if not self.site_id:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Warning'),
                    'message': _('Please select a site first.'),
                    'type': 'warning',
                    'sticky': False,
                }
            }
        
        checkpoints = self.env['security.checkpoint'].search([('site_id', '=', self.site_id.id)], order='id')
        
        if not checkpoints:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('Info'),
                    'message': _('No checkpoints found for this site.'),
                    'type': 'info',
                    'sticky': False,
                }
            }
        
        checkpoint_lines = [(5, 0, 0)]
        for sequence, checkpoint in enumerate(checkpoints, start=1):
            checkpoint_lines.append((0, 0, {
                'checkpoint_id': checkpoint.id,
                'sequence': sequence
            }))
        
        self.checkpoint_ids = checkpoint_lines
        
        return True

    def action_generate_tour(self):
        self.ensure_one()
        if not self.start_date or not self.end_date:
            return
        
        current_date = self.start_date
        tours = self.env['security.tour']
        
        while current_date <= self.end_date:
            self.tour_count += 1
            tour_vals = {
                'name': "%s/%03d" % (self.name, self.tour_count),
                'template_id': self.id,
                'site_id': self.site_id.id,
                'superviser_id': self.superviser_id.id if self.superviser_id else False,
                'agent_id': self.agent_id.id if self.agent_id else False,
                'date': current_date,
                'start_time': self.start_time,
                'end_time': self.end_time,
                'grace_period': self.grace_period,
                'strict_ordering': self.strict_ordering,
                'require_selfie': self.require_selfie,
                'require_photo_place': self.require_photo_place,
                'state': 'planned',
                'checkpoint_ids': [(0, 0, {
                    'checkpoint_id': line.checkpoint_id.id,
                    'sequence': line.sequence
                }) for line in self.checkpoint_ids]
            }
            tours |= self.env['security.tour'].create(tour_vals)
            
            if self.frequency == 'daily':
                current_date += timedelta(days=1)
            elif self.frequency == 'weekly':
                current_date += timedelta(weeks=1)
            else:
                break
                
        if len(tours) == 1:
            return {
                'name': _('Generated Tour'),
                'type': 'ir.actions.act_window',
                'res_model': 'security.tour',
                'res_id': tours.id,
                'view_mode': 'form',
                'target': 'current',
            }
        else:
            return {
                'name': _('Generated Tours'),
                'type': 'ir.actions.act_window',
                'res_model': 'security.tour',
                'view_mode': 'tree,form',
                'domain': [('id', 'in', tours.ids)],
                'target': 'current',
            }

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('security.tour.template') or 'New'
        if not vals.get('superviser_id'):
            vals['superviser_id'] = self.env.user.id
        return super(TourTemplate, self).create(vals)

    def name_get(self):
        result = []
        for record in self:
            name = "[%s] %s" % (record.name, record.title)
            result.append((record.id, name))
        return result

class TourTemplateLine(models.Model):
    _name = 'security.tour.template.line'
    _description = 'Tour Template Checkpoint Line'
    _order = 'sequence, id'

    template_id = fields.Many2one('security.tour.template', string='Template', required=True, ondelete='cascade')
    checkpoint_id = fields.Many2one('security.checkpoint', string='Checkpoint', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
