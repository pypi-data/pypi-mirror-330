from .utils import list_from_value


def normalize_attachment(attachment: dict) -> dict:
    """Normalizes an attachment"""

    if attachment.get("type") != "Document":
        return attachment

    media_type = attachment.get("mediaType")
    if media_type is None:
        return attachment

    if media_type.startswith("image/"):
        attachment["type"] = "Image"
    if media_type.startswith("audio/"):
        attachment["type"] = "Audio"
    if media_type.startswith("video/"):
        attachment["type"] = "Video"

    return attachment


def normalize_attachments(attachments) -> list[dict] | None:
    list_of_attachments = list_from_value(attachments)
    if list_of_attachments is None:
        return None

    return [normalize_attachment(attachment) for attachment in list_of_attachments]
