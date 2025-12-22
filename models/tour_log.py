from odoo import models, fields, api

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