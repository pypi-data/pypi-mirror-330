"""Routings to normalize an ActivityPub activity"""

import logging

from uuid6 import uuid7
from bovine.activitystreams.utils import id_for_object

from .types import Activity, Object
from .utils import list_from_value, sanitize_html
from .attachment import normalize_attachments
from .content import normalize_content

logger = logging.getLogger(__name__)


def normalize_to(value, actor):
    """Normalizes the to value

    ```pycon
    >>> normalize_to(None, "http://actor.example")
    ['http://actor.example']

    >>> normalize_to("http://to.example", None)
    ['http://to.example']

    >>> normalize_to(["http://alice.example", "http://bob.example"], None)
    ['http://alice.example', 'http://bob.example']

    ```
    """
    if value is None:
        return [actor]
    return list_from_value(value)


def normalize_id(activity):
    """
    Creates a normalized id

    ```pycon
    >>> normalize_id({"id": "http://id.example"})
    'http://id.example'

    >>> normalize_id({})
    Traceback (most recent call last):
        ...
    ValueError: Cannot fake id if actor is not present

    ```
    """
    result = activity.get("id")
    if result is not None:
        return result
    actor_id = id_for_object(activity.get("actor"))

    if actor_id is None:
        raise ValueError("Cannot fake id if actor is not present")

    return f"{actor_id}#fake_id" + str(uuid7())


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


def normalize_url(url):
    if url is None:
        return
    if isinstance(url, str):
        url = {"type": "Link", "href": url}

    return list_from_value(url)


def normalize_to_id(attributed_to) -> str | None:
    if isinstance(attributed_to, list) and len(attributed_to) == 1:
        attributed_to = attributed_to[0]

    return id_for_object(attributed_to)  # type: ignore


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
            "attachment": normalize_attachments(obj.get("attachment")),
            "sensitive": obj.get("sensitive"),
            "summary": sanitize_html(obj.get("summary")),
            "tag": list_from_value(obj.get("tag")),
            "url": normalize_url(obj.get("url")),
            "inReplyTo": normalize_to_id(obj.get("inReplyTo")),
        }
    )
