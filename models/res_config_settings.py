# -*- coding: utf-8 -*-

from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    round_grace_period = fields.Integer(
        string="Default Grace Period (minutes)",
        config_parameter='security_patrol.default_round_grace_period',
        default=15,
        help="Time allowed before a round is marked as late."
    )
    
    incident_notification_email = fields.Char(
        string="Incident Notification Email",
        config_parameter='security_patrol.incident_notification_email',
        help="Default email address to receive incident reports."
    )
    
    enforce_sequential_scans = fields.Boolean(
        string="Enforce Sequential Scans",
        config_parameter='security_patrol.enforce_sequential_scans',
        default=False,
        help="If enabled, checkpoints must be scanned in the exact order defined in the round."
    )

    require_selfie = fields.Boolean(
        string="Require Selfie",
        config_parameter='security_patrol.require_selfie',
        default=False,
        help="If enabled, agents must take a selfie when logging a checkpoint."
    )
    
    require_photo_place = fields.Boolean(
        string="Require Photo of Place", 
        config_parameter='security_patrol.require_photo_place',
        default=False,
        help="If enabled, agents must take a photo of the location when logging a checkpoint."
    )
    
    max_checkpoint_distance = fields.Integer(
        string="Max Checkpoint Distance (meters)",
        config_parameter='security_patrol.max_checkpoint_distance',
        default=50,
        help="Maximum allowed distance (in meters) between agent GPS and checkpoint GPS when scanning."
    )
