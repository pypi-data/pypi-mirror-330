# -*- coding: utf-8 -*-
#
# Copyright (C) 2023-2025 TU Wien.
#
# Invenio-Config-TUW is free software; you can redistribute it and/or modify
# it under the terms of the MIT License; see LICENSE file for more details.

"""Celery tasks running in the background."""

from typing import Optional

from celery import shared_task
from celery.schedules import crontab
from flask import current_app, url_for
from invenio_access.permissions import system_identity
from invenio_accounts.proxies import current_datastore
from invenio_db import db
from invenio_files_rest.models import FileInstance
from invenio_notifications.tasks import broadcast_notification
from invenio_rdm_records.proxies import current_rdm_records_service as records_service

from .notifications import UserNotificationBuilder


@shared_task(ignore_result=True)
def send_publication_notification(recid: str, user_id: Optional[str] = None):
    """Send the record uploader an email about the publication of their record."""
    record = records_service.read(identity=system_identity, id_=recid)._obj
    record_title = record["metadata"]["title"]
    if user_id is not None:
        user = current_datastore.get_user(user_id)
    else:
        owner = record.parent.access.owner
        if owner is not None and owner.owner_type == "user":
            user = owner.resolve()
        else:
            current_app.logger.warn(
                f"Couldn't find owner of record '{recid}' for sending email!"
            )
            return

    # build the message
    datacite_test_mode = current_app.config["DATACITE_TEST_MODE"]
    if "identifier" in record.get("pids", {}).get("doi", {}):
        doi = record["pids"]["doi"]["identifier"]

        if datacite_test_mode:
            doi_base_url = "https://handle.test.datacite.org"
            doi_type = "DOI-like handle"
        else:
            doi_base_url = "https://doi.org"
            doi_type = "DOI"

        doi_url = f"{doi_base_url}/{doi}"
        link_line = f"It is now available under the following {doi_type}: {doi_url}"
        link_line_html = f'It is now available under the following {doi_type}: <a href="{doi_url}">{doi_url}</a>'

    else:
        landing_page_url = url_for(
            "invenio_app_rdm_records.record_detail",
            pid_value=record.pid.pid_value,
            _external=True,
        )
        link_line = f"It is now available under the following URL: {landing_page_url}"
        link_line_html = f'It is now available under the following URL: <a href="{landing_page_url}">{landing_page_url}</a>'

    publish_line = f'Your record "{record_title}" just got published!'
    edits_line = "Metadata edits for this record will *not* require another review."
    edits_line_html = (
        "Metadata edits for this record will <em>not</em> require another review."
    )

    message = "\n".join([publish_line, link_line, "", edits_line])
    html_message = "<br />".join([publish_line, link_line_html, "", edits_line_html])

    # send the notification
    notification = UserNotificationBuilder().build(
        receiver={"user": user.id},
        subject=f'Your record "{record_title}" was published',
        message=message,
        html_message=html_message,
    )
    broadcast_notification(notification.dumps())


@shared_task
def remove_dead_files():
    """Remove dead file instances (that don't have a URI) from the database.

    These files seem to be leftovers from failed uploads that don't get cleaned up
    properly.
    """
    dead_file_instances = FileInstance.query.filter(FileInstance.uri.is_(None)).all()
    for fi in dead_file_instances:
        db.session.delete(fi)
        for o in fi.objects:
            db.session.delete(o)

    db.session.commit()


CELERY_BEAT_SCHEDULE = {
    "clean-dead-files": {
        "task": "invenio_config_tuw.tasks.remove_dead_files",
        "schedule": crontab(minute=1, hour=2),
    },
}
