# Part of OpenSPP. See LICENSE file for full copyright and licensing details.


import json

import requests

from odoo import _, fields, models
from odoo.exceptions import ValidationError

from odoo.addons.queue_job.delay import group


class OpenSPPPrintBatch(models.Model):
    _name = "spp.print.queue.batch"
    _description = "ID print Batch"

    JOBBATCH_SIZE = 20

    name = fields.Char("Batch name")

    #  We should only allow `approved` id to be added to a batch
    queued_ids = fields.One2many("spp.print.queue.id", "batch_id", string="Queued IDs")
    status = fields.Selection(
        [
            ("new", "New"),
            ("generating", "Generating"),
            ("generated", "Generated"),
            ("printing", "Printing"),
            ("printed", "Printed"),
        ],
        default="new",
    )

    id_pdf = fields.Binary("ID PASS")
    id_pdf_filename = fields.Char("ID File Name")
    merge_status = fields.Selection(
        [
            ("draft", "Draft"),
            ("sent", "Sent"),
            ("merged", "Merged"),
            ("error_sending", "Error Sending"),
            ("error_merging", "Error Merging"),
        ],
        default="draft",
    )

    def generate_batch(self):
        for rec in self:
            rec.status = "generating"
            queued_ids = []
            jobs = []
            ctr2 = 1
            max_rec = len(rec.queued_ids)
            for ctr, queued_id in enumerate(rec.queued_ids, 1):
                queued_ids.append(queued_id.id)
                if ctr2 == self.JOBBATCH_SIZE or ctr == max_rec:
                    ctr2 = 0
                    jobs.append(rec.delayable()._generate_cards(queued_ids))
                    queued_ids = []
                ctr2 += 1

            main_job = group(*jobs)
            main_job.on_done(self.delayable().mark_as_done(rec))
            main_job.delay()

    def _generate_cards(self, queue_ids):
        queued_ids = self.env["spp.print.queue.id"].search([("id", "in", queue_ids)])
        queued_ids.generate_cards()

    def mark_as_done(self, rec):
        if not rec.queued_ids.filtered(lambda x: x.status != "generated"):
            rec.status = "generated"
            rec.pass_api_param()
        else:
            raise ValidationError(_("Some IDs are not generated"))

    def retry_pass_api(self):
        for rec in self:
            rec.pass_api_param()

    def pass_api_param(self):
        for rec in self:
            batch_param = self.env["spp.id.pass"].search(
                [("id", "=", self.env.ref("spp_idqueue.id_template_batch_print").id)]
            )
            if batch_param and batch_param.auth_token and batch_param.api_url:
                token = _("Token %s", batch_param.auth_token)
                data = {
                    "batch_id": str(rec.id),
                }
                headers = {
                    "Content-Type": "application/json",
                    "Accept": "application/json",
                    "Authorization": token,
                }

                response = requests.post(
                    batch_param.api_url,
                    data=json.dumps(data),
                    headers=headers,
                )

                if response.status_code == 200:
                    rec.merge_status = "sent"
                else:
                    rec.merge_status = "error_sending"
            else:
                message = _("No Auth Token or API URL")
                raise ValidationError(message)
        return

    def print_batch(self):
        for rec in self:
            rec.status = "printing"

    def batch_printed(self):
        for rec in self:
            rec.status = "printed"
