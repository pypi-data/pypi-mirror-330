# -*- coding: utf-8 -*-
#
# Copyright (C) 2024 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or
# modify it under the terms of the MIT License; see LICENSE file for more
# details.


"""Overrides for core services."""

from invenio_curations.services.components import (
    CurationComponent as BaseCurationComponent,
)
from invenio_drafts_resources.services.records.components import ServiceComponent
from invenio_pidstore.models import PIDStatus
from invenio_rdm_records.services.components import DefaultRecordsComponents
from invenio_records_resources.services.uow import TaskOp

from .proxies import current_config_tuw
from .tasks import send_publication_notification


class ParentAccessSettingsComponent(ServiceComponent):
    """Service component that allows access requests per default."""

    def create(self, identity, record, **kwargs):
        """Set the parent access settings to allow access requests."""
        settings = record.parent.access.settings
        settings.allow_guest_requests = True
        settings.allow_user_requests = True
        settings.secret_link_expiration = 30


class PublicationNotificationComponent(ServiceComponent):
    """Component for notifying users about the publication of their record."""

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Register a task to send off the notification email."""
        # the first time the record gets published, the PID's status
        # gets set to "R" but that won't have been transferred to the
        # record's data until the `record.commit()` from the unit of work
        has_been_published = (
            draft.pid.status == draft["pid"]["status"] == PIDStatus.REGISTERED
        )

        if not has_been_published:
            self.uow.register(
                TaskOp(send_publication_notification, record.pid.pid_value)
            )


class CurationComponent(BaseCurationComponent):
    """Curation component that only activates if curations are enabled."""

    def publish(self, identity, draft=None, record=None, **kwargs):
        """Check if record curation request has been accepted."""
        if current_config_tuw.curations_enabled:
            return super().publish(identity, draft=draft, record=record, **kwargs)

    def delete_draft(self, identity, draft=None, record=None, force=False):
        """Delete a draft."""
        if current_config_tuw.curations_enabled:
            return super().delete_draft(
                identity, draft=draft, record=record, force=force
            )

    def update_draft(self, identity, data=None, record=None, errors=None):
        """Update draft handler."""
        if current_config_tuw.curations_enabled:
            value = super().update_draft(
                identity, data=data, record=record, errors=errors
            )

            # suppress the "missing field: rdm-curation" error as that is more
            # confusing than helpful
            errors = errors or []
            curation_field_errors = [
                e for e in errors if e.get("field") == "custom_fields.rdm-curation"
            ]
            for e in curation_field_errors:
                errors.remove(e)

            return value


TUWRecordsComponents = [
    *DefaultRecordsComponents,
    ParentAccessSettingsComponent,
    PublicationNotificationComponent,
    CurationComponent,
]
