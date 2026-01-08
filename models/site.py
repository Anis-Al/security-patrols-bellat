# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Site(models.Model):
    _name = 'security.site'
    _description = 'Security Site'
    _rec_name = 'name'

    name = fields.Char(string='Site Name', required=True)
    # adresse = fields.Char(string='Adresse')
    # latitude = fields.Float(string='Latitude', digits=(10, 7))
    # longitude = fields.Float(string='Longitude', digits=(10, 7))
    checkpoint_ids = fields.One2many('security.checkpoint', 'site_id', string='Checkpoints')
    checkpoint_count = fields.Integer(compute='_compute_checkpoint_count', string="Total Checkpoints")

    @api.depends('checkpoint_ids')
    def _compute_checkpoint_count(self):
        for site in self:
            site.checkpoint_count = len(site.checkpoint_ids)
