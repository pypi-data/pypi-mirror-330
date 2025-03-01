from bovine.activitystreams.utils import id_for_object

from .utils import list_from_value


def transform_url_part(url_part):
    if isinstance(url_part, str):
        url_part = {"type": "Link", "href": url_part}
    return url_part


def transform_url(url) -> list[dict] | None:
    url_list = list_from_value(url)
    if url_list is None:
        return

    return [transform_url_part(url_part) for url_part in url_list]


def transform_to(to) -> list[str] | None:
    to_list = list_from_value(to)
    if to_list is None:
        return

    return [x for x in (id_for_object(to) for to in to_list) if x]
