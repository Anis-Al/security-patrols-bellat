# -*- coding: utf-8 -*-

import uuid
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import base64
import io

try:
    import segno
except ImportError:
    segno = None


class Point(models.Model):
    _name = 'security.checkpoint'
    _description = 'Security Checkpoint'
    _order = 'id'
    _rec_name='name'

    name = fields.Char(string='Checkpoint Name', required=True)
    site_id = fields.Many2one('security.site', string='Site', required=True, ondelete='cascade')
    latitude = fields.Float(string='Latitude', digits=(10, 7))
    longitude = fields.Float(string='Longitude', digits=(10, 7))
    map=fields.Char(string="Map",readonly=True)
    instructions = fields.Text(string='Instructions')
    
    check_type = fields.Selection([
        ('qrcode', 'QR Code'),
        ('nfc', 'NFC Tag'),
        ('code', 'Unique Code')
    ], string='Check Type', required=True, default='qrcode')
    
    identifier = fields.Char(string='Identifier', copy=False, default=lambda self: str(uuid.uuid4()))
    qr_code = fields.Binary("QR Code", attachment=True, store=True,readonly=True)
    _sql_constraints = [
        ('identifier_uniq', 'unique (identifier)', 'The identifier must be unique!')
    ]
    
    
    @api.model
    def create(self, vals):
        res = super(Point, self).create(vals)
        if res.identifier and res.check_type == 'qrcode':
            res._generate_qr_code()
        return res

    def write(self, vals):
        res = super(Point, self).write(vals)
        for record in self:
            if 'identifier' in vals or 'check_type' in vals:
                if record.identifier and record.check_type == 'qrcode':
                    record._generate_qr_code()
        return res

    def _generate_qr_code(self):
        if not segno:
             raise UserError(_("Segno library is missing, please install it to generate QR codes."))
        for record in self:
            qrcode = segno.make(record.identifier, error='h')
            out = io.BytesIO()
            qrcode.save(out, kind='png', scale=5)
            record.qr_code = base64.b64encode(out.getvalue())


    def action_generate_identifier(self):
        for record in self:
            record.identifier = str(uuid.uuid4())

    def action_open_record(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'security.checkpoint',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'current',
        }

