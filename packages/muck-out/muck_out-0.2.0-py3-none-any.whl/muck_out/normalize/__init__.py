"""Routines to normalize an ActivityPub activity or object.

The routines here take a dictionary and turn them into another
one."""

import logging

from bovine.activitystreams.utils import id_for_object

from muck_out.types import Activity, Object
from muck_out.transform.utils import list_from_value, sanitize_html
from muck_out.transform.attachment import transform_attachments
from .content import normalize_content
from .base import normalize_to, normalize_id, normalize_to_id, normalize_url

logger = logging.getLogger(__name__)


def normalize_activity(activity: dict, actor: str | None = None) -> Activity:
    """
    Normalizes activities.

    :param activity: The activity being normalized
    :param actor: Actor receiving this activity
    :returns:
    """
    try:
        obj = activity.get("object")
        if isinstance(obj, dict):
            try:
                obj = normalize_object(obj)
            except Exception:
                if isinstance(obj, dict):
                    obj = obj.get("id")

        return Activity.model_validate(
            {
                "@context": activity.get("@context"),
                "id": normalize_id(activity),
                "type": activity.get("type"),
                "actor": id_for_object(activity.get("actor")),
                "object": obj,
                "to": normalize_to(activity.get("to"), actor),
                "cc": list_from_value(activity.get("cc")),
                "published": activity.get("published"),
                "target": activity.get("target"),
                "content": activity.get("content"),
            }
        )
    except Exception as e:
        logger.exception(e)
        logger.info(activity)

        raise e


def normalize_object(obj: dict) -> Object:
    """Normalizes an object

    :params obj: The object to be normalized
    :returns:
    """
    return Object.model_validate(
        {
            "@context": obj.get("@context"),
            "id": obj.get("id"),
            "type": obj.get("type"),
            "attributedTo": normalize_to_id(obj.get("attributedTo")),
            "obj": obj.get("obj"),
            "to": list_from_value(obj.get("to")),
            "cc": list_from_value(obj.get("cc")),
            "published": obj.get("published"),
            "target": obj.get("target"),
            "content": normalize_content(obj),
            "attachment": transform_attachments(obj.get("attachment")),
            "sensitive": obj.get("sensitive"),
            "summary": sanitize_html(obj.get("summary")),
            "tag": list_from_value(obj.get("tag")),
            "url": normalize_url(obj.get("url")),
            "inReplyTo": normalize_to_id(obj.get("inReplyTo")),
        }
    )
