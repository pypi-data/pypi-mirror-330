# -*- coding: utf-8 -*-
from odoo.http import request
from odoo.addons.easy_my_coop_website.controllers.main import WebsiteSubscription
from odoo import http
from odoo.http import request
from datetime import datetime
import base64
# Only use for behavior, don't stock it
_TECHNICAL = ["view_from", "view_callback"]

_EXTRA_FIELDS = []

# Allow in description
_BLACKLIST = [
    "id",
    "create_uid",
    "create_date",
    "write_uid",
    "write_date",
    "user_id",
    "active",
]

_COOP_FORM_FIELD = [
    "email",
    "confirm_email",
    "firstname",
    "lastname",
    "birthdate",
    "iban",
    "share_product_id",
    "city",
    "zip_code",
    "country_id",
    "phone",
    "lang",
    "nb_parts",
    "total_parts",
    "error_msg",
]


class WebsiteSubscription(WebsiteSubscription):


    def fill_values(self, values, is_company, logged, load_from_user=False):
        values = super(WebsiteSubscription, self).fill_values(values, is_company, logged, load_from_user=False)
        sub_req_obj = request.env['subscription.request']
        fields_desc = sub_req_obj.sudo().fields_get(['discovery_channel'])
        company = request.env['res.company']._company_default_get()
        values.update({
            'channels': fields_desc['discovery_channel']['selection'],
            'display_sepa': company.display_sepa_approval,
            'sepa_required': company.sepa_approval_required,
            'sepa_text': company.sepa_approval_text
        })
        return values

    @http.route(
        ["/subscription/subscribe_share"],
        type="http",
        auth="public",
        website=True,
    )

    def share_subscription(self, **kwargs):
        sub_req_obj = request.env["subscription.request"]
        attach_obj = request.env["ir.attachment"]

        # List of file to add to ir_attachment once we have the ID
        post_file = []
        # Info to add after the message
        post_description = []
        values = {}

        for field_name, field_value in kwargs.items():
            if hasattr(field_value, "filename"):
                post_file.append(field_value)
            elif (
                field_name in sub_req_obj._fields
                and field_name not in _BLACKLIST
            ):
                values[field_name] = field_value
            elif field_name in _EXTRA_FIELDS and field_name not in _BLACKLIST:
                values[field_name] = field_value
            # allow to add some free fields or blacklisted field like ID
            elif field_name not in _TECHNICAL:
                post_description.append(
                    "{}: {}".format(field_name, field_value)
                )

        logged = kwargs.get("logged") == "on"
        is_company = kwargs.get("is_company") == "on"

        response = self.validation(kwargs, logged, values, post_file)
        if response is not True:
            return response

        already_coop = False
        if logged:
            partner = request.env.user.partner_id
            values["partner_id"] = partner.id
            already_coop = partner.member
        elif kwargs.get("already_cooperator") == "on":
            already_coop = True

        values["already_cooperator"] = already_coop
        values["is_company"] = is_company

        if kwargs.get("data_policy_approved", "off") == "on":
            values["data_policy_approved"] = True

        if kwargs.get("internal_rules_approved", "off") == "on":
            values["internal_rules_approved"] = True

        if kwargs.get("financial_risk_approved", "off") == "on":
            values["financial_risk_approved"] = True

        lastname = kwargs.get("lastname").upper()
        firstname = kwargs.get("firstname").title()

        values["name"] = firstname + " " + lastname
        values["lastname"] = lastname
        values["firstname"] = firstname
        values["birthdate"] = datetime.strptime(
            kwargs.get("birthdate"), "%Y-%m-%d"
        ).date()
        values["source"] = "website"

        values["share_product_id"] = self.get_selected_share(kwargs).id

        if is_company:
            if kwargs.get("company_register_number"):
                values["company_register_number"] = re.sub(
                    "[^0-9a-zA-Z]+", "", kwargs.get("company_register_number")
                )
            subscription_id = sub_req_obj.sudo().create_comp_sub_req(values)
        else:
            subscription_id = sub_req_obj.sudo().create(values)

        if subscription_id:
            for field_value in post_file:
                attachment_value = {
                    "name": field_value.filename,
                    "res_name": field_value.filename,
                    "res_model": "subscription.request",
                    "res_id": subscription_id,
                    "datas": base64.encodestring(field_value.read()),
                    "datas_fname": field_value.filename,
                }
                attach_obj.sudo().create(attachment_value)

        return self.get_subscription_response(values, kwargs)
