# Copyright 2023 OpenSynergy Indonesia
# Copyright 2023 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _name = "helpdesk_ticket"
    _inherit = [
        "helpdesk_ticket",
    ]

    odoo_implementation_id = fields.Many2one(
        string="# Odoo Implementation",
        comodel_name="odoo_implementation",
    )
    odoo_version_id = fields.Many2one(
        string="Odoo Version",
        comodel_name="odoo_version",
        related="odoo_implementation_id.version_id",
        store=True,
    )
    odoo_feature_id = fields.Many2one(
        string="Related Feature",
        comodel_name="odoo_feature",
    )
    odoo_feature_issue_id = fields.Many2one(
        string="Related Issue",
        comodel_name="odoo_feature_issue",
    )

    @api.onchange(
        "commercial_partner_id",
    )
    def onchange_odoo_implementation_id(self):
        self.odoo_implementation_id = False

    @api.onchange(
        "odoo_feature_id",
    )
    def onchange_odoo_feature_issue_id(self):
        self.odoo_feature_issue_id = False

    @api.onchange(
        "odoo_feature_issue_id",
    )
    def onchange_task_ids(self):
        self.task_ids = False
        if self.odoo_feature_issue_id:
            self.task_ids = self.odoo_feature_issue_id.task_ids
