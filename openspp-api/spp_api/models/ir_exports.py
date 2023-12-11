# Copyright 2018 Ivan Yelizariev <https://it-projects.info/team/yelizariev>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import models


class IrExports(models.Model):
    _inherit = "ir.exports"

    # @api.constrains("resource", "export_fields")
    # def _check_fields(self):
    #     # this exports record used in openapi.access
    #     if (
    #         not self.env["openapi.access"]
    #         .sudo()
    #         .search_count(
    #             ["|", ("read_one_id", "=", self.id), ("read_many_id", "=", self.id)]
    #         )
    #     ):
    #         return True

    #     # TODO: remove this constrain? It extends base functionality that is not related to openapi module

    #     fields = self.export_fields.mapped("name")
    #     for field in fields:
    #         field_count = fields.count(field)
    #         if field_count > 1:
    #             self.export_fields.search(
    #                 [("name", "=", field)], limit=field_count - 1
    #             ).unlink()

    #     fields.sort()
    #     for i in range(len(fields) - 1):
    #         if fields[i + 1].startswith(fields[i]) and "/" in fields[i + 1].replace(
    #             fields[i], ""
    #         ):
    #             raise exceptions.ValidationError(
    #                 _(
    #                     'You must delete the "%(field1)s" field or "%(field2)s" field',
    #                     {"field1": fields[i], "field2": fields[i + 1]},
    #                 )
    #             )
