from .types import Actor

from .attachment import normalize_attachment
from .utils import sanitize_html, list_from_value, remove_html

from .types.actor import PropertyValue


def normalize_actor(data: dict) -> Actor | None:
    """Normalizes an ActivityPub actor"""

    actor_type = data.get("type")

    if actor_type not in ["Person", "Service", "Application", "Group"]:
        return None

    avatar = data.get("icon")
    if avatar:
        avatar = normalize_attachment(avatar)

    attachments = list_from_value(data.get("attachment"))
    if attachments:
        attachments = [
            normalize_property_value(attachment) for attachment in attachments
        ]

    return Actor.model_validate(
        {
            "@context": data.get("@context"),
            "type": actor_type,
            "id": data.get("id"),
            "inbox": data.get("inbox"),
            "outbox": data.get("outbox"),
            "icon": avatar,
            "summary": sanitize_html(data.get("summary")),
            "name": data.get("name"),
            "alsoKnownAs": list_from_value(data.get("alsoKnownAs")),
            "attachments": attachments,
        }
    )


def normalize_property_value(data: dict) -> PropertyValue | dict:
    if data.get("type") == "PropertyValue":
        return PropertyValue.model_validate(
            {
                "name": remove_html(data.get("name")),
                "value": remove_html(data.get("value")),
            }
        )
    return data
