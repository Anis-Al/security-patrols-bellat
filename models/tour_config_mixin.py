# -*- coding: utf-8 -*-

from odoo import models, fields


class TourConfigMixin(models.AbstractModel):
    _name = 'security.tour.config.mixin'
    _description = 'Tour Configuration Mixin'

    grace_period = fields.Integer(
        string='Grace Period (min)',
        default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('security_patrol.default_round_grace_period', 15)),
        help="Time allowed before a round is marked as late."
    )
    
    strict_ordering = fields.Boolean(
        string='Strict Ordering',
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.enforce_sequential_scans') == 'True',
        help="If enabled, checkpoints must be scanned in the exact order defined."
    )
    
    require_selfie = fields.Boolean(
        string='Require Selfie',
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.require_selfie') == 'True',
        help="If enabled, agents must take a selfie when logging a checkpoint."
    )
    
    require_photo_place = fields.Boolean(
        string='Require Photo of Place',
        default=lambda self: self.env['ir.config_parameter'].sudo().get_param('security_patrol.require_photo_place') == 'True',
        help="If enabled, agents must take a photo of the location when logging a checkpoint."
    )
    
    max_checkpoint_distance = fields.Integer(
        string='Max Checkpoint Distance (m)',
        default=lambda self: int(self.env['ir.config_parameter'].sudo().get_param('security_patrol.max_checkpoint_distance', 50)),
        help="Maximum allowed distance (in meters) between agent GPS and checkpoint GPS when scanning."
    )