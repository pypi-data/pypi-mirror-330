# -*- coding: utf-8 -*-
#
# Copyright (C) 2025 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Custom notification backends for TU Wien."""

from flask import current_app
from invenio_mail.tasks import send_email
from invenio_notifications.backends.email import EmailNotificationBackend
from marshmallow_utils.html import strip_html

from ..proxies import current_config_tuw


class TUWEmailNotificationBackend(EmailNotificationBackend):
    """Email notification backend extended for the use cases at TU Wien.

    Sets additional email headers that indicate the sending service.
    Also considers the user's configured secondary email address.
    """

    def send(self, notification, recipient):
        """Mail sending implementation."""
        content = self.render_template(notification, recipient)
        subject = content["subject"]

        # if a site identifier is configured, we set is as prefix for email subjects
        site_id = current_app.config.get("CONFIG_TUW_SITE_IDENTIFIER", None)
        if site_id:
            subject = f"[{site_id}] {subject}"

        secondary_email = (
            recipient.data.get("preferences", {})
            .get("notifications", {})
            .get("secondary_email", None)
        )

        resp = send_email(
            {
                "subject": subject,
                "html": content["html_body"],
                "body": strip_html(content["plain_body"]),
                "recipients": [
                    recipient.data.get("email") or recipient.data.get("email_hidden")
                ],
                "cc": [secondary_email] if secondary_email else [],
                "sender": current_app.config["MAIL_DEFAULT_SENDER"],
                "reply_to": current_app.config["MAIL_DEFAULT_REPLY_TO"],
                "extra_headers": {
                    "X-Sender": current_config_tuw.email_xsender_value,
                },
            }
        )
        return resp
