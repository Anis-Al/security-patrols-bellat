# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class TourLog(models.Model):
    _name = 'security.tour.log'
    _description = 'Security Tour Log'
    _order = 'time desc'

    tour_id = fields.Many2one('security.tour', string='Tour', required=True, ondelete='cascade')
    checkpoint_id = fields.Many2one('security.checkpoint', string='Checkpoint', required=True)
    
    time = fields.Datetime(string='Time of Passage', default=fields.Datetime.now, required=True)
    latitude = fields.Float(string='Latitude', digits=(10, 7))
    longitude = fields.Float(string='Longitude', digits=(10, 7))
    
    require_selfie = fields.Boolean(related='tour_id.require_selfie', string='Require Selfie')
    require_photo_place = fields.Boolean(related='tour_id.require_photo_place', string='Require Photo of Place')

    photo_selfie = fields.Binary(string='Selfie', attachment=True)
    photo_place = fields.Binary(string='Photo of Place', attachment=True)
    
    comment = fields.Text(string='Comment')
    
    status = fields.Selection([
        ('ok', 'OK'),
        ('incident', 'Incident')
    ], string='Status', default='ok', required=True)
    
    incident_ids = fields.One2many('security.incident', 'log_id', string='Incidents')

    @api.constrains('tour_id', 'checkpoint_id')
    def _check_unique_checkpoint_per_tour(self):
        for record in self:
            duplicate = self.search([
                ('tour_id', '=', record.tour_id.id),
                ('checkpoint_id', '=', record.checkpoint_id.id),
                ('id', '!=', record.id)
            ])
            if duplicate:
                raise ValidationError(_("This checkpoint has already been scanned for this tour."))

    @api.model
    def create(self, vals):
        res = super(TourLog, self).create(vals)
        if res.tour_id.state == 'planned':
            res.tour_id.state = 'in_progress'
        res.tour_id._check_completion()
        return res

    def action_view_incidents(self):
        self.ensure_one()
        return {
            'name': _('Incidents'),
            'type': 'ir.actions.act_window',
            'res_model': 'security.incident',
            'view_mode': 'tree,form',
            'domain': [('log_id', '=', self.id)],
            'context': {
                'default_log_id': self.id,
                'default_title': 'Incident at %s' % self.checkpoint_id.name,
            },
            'target': 'current',
        }

