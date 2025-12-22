from odoo import api, fields, models

class Agent(models.Model):
    _inherit = 'hr.employee'
    _description = 'Security Agent'
    
    is_agent = fields.Boolean(string="Agent ?", default=False)
    status = fields.Selection(selection=[('actif','Actif'),
                                        ('inactif','Inactif')],
                                        string='Status', required=True, default='actif')
    