# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import fields, models


class OdooImplementation(models.Model):
    _name = "odoo_implementation"
    _inherit = [
        "odoo_implementation",
    ]

    ticket_ids = fields.One2many(
        string="Tickets",
        comodel_name="helpdesk_ticket",
        inverse_name="odoo_implementation_id",
    )
