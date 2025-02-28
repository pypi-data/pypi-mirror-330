from .utils import sanitize_html


def normalize_content(data: dict) -> str | None:
    """Normalizes the content of an ActivityPub object"""
    result = data.get("content")
    if isinstance(result, str):
        return sanitize_html(result)

    content_map = data.get("contentMap")

    if isinstance(content_map, dict) and len(content_map) > 0:
        return sanitize_html(list(content_map.values())[0])

    return None
