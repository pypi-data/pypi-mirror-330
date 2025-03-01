# -*- coding: utf-8 -*-
#
# Copyright (C) 2024-2025 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Customizations for the ``rdm-curation`` requests from ``Invenio-Curations``."""

from invenio_curations.notifications.builders import (
    CurationRequestActionNotificationBuilder,
)
from invenio_curations.requests.curation import (
    CurationCreateAndSubmitAction,
    CurationRequest,
    CurationResubmitAction,
    CurationSubmitAction,
)
from invenio_notifications.services.uow import NotificationOp
from invenio_users_resources.notifications.filters import UserPreferencesRecipientFilter
from invenio_users_resources.notifications.generators import UserRecipient

from ..notifications import TUWTaskOp
from .tasks import auto_review_curation_request


class TUWCurationRequestUploaderResubmitNotificationBuilder(
    CurationRequestActionNotificationBuilder
):
    """Notification builder for the request creator on resubmit."""

    type = f"{CurationRequestActionNotificationBuilder.type}.resubmit-creator"
    recipients = [UserRecipient("request.created_by")]
    recipient_filters = [UserPreferencesRecipientFilter()]


class TUWCurationResubmitAction(CurationResubmitAction):
    """Notify both uploader and reviewer on resubmit, and auto-review."""

    def execute(self, identity, uow):
        """Notify uploader when the record gets resubmitted for review."""
        uow.register(
            NotificationOp(
                TUWCurationRequestUploaderResubmitNotificationBuilder.build(
                    identity=identity, request=self.request
                )
            )
        )
        uow.register(
            TUWTaskOp(auto_review_curation_request, str(self.request.id), countdown=15)
        )
        return super().execute(identity, uow)


class TUWCurationSubmitAction(CurationSubmitAction):
    """Submit action with a hook for automatic reviews.

    Note: It looks like this isn't really being used, in favor of "create & submit".
    """

    def execute(self, identity, uow):
        """Register auto-review task and perform the submit action."""
        uow.register(
            TUWTaskOp(auto_review_curation_request, str(self.request.id), countdown=15)
        )

        return super().execute(identity, uow)


class TUWCurationCreateAndSubmitAction(CurationCreateAndSubmitAction):
    """'Create & submit' action with a hook for automatic reviews."""

    def execute(self, identity, uow):
        """Register auto-review task and perform the 'create & submit' action."""
        uow.register(
            TUWTaskOp(auto_review_curation_request, str(self.request.id), countdown=15)
        )

        return super().execute(identity, uow)


class TUWCurationRequest(CurationRequest):
    """Customized curation request class with modified resubmit action."""

    available_actions = {
        **CurationRequest.available_actions,
        "create": TUWCurationCreateAndSubmitAction,
        "submit": TUWCurationSubmitAction,
        "resubmit": TUWCurationResubmitAction,
    }
