from typing import List
from bovine.activitystreams.utils import id_for_object

from .types import Collection


def convert_items(items: List[dict | str]) -> List[str]:
    """Converts a list of items to a list of ids

    ```pycon
    >>> convert_items([{"id": "https://site.example/1"}, "https://site.example/2"])
    ['https://site.example/1', 'https://site.example/2']

    ```
    """
    return [x for x in (id_for_object(item) for item in items) if x]


def normalize_collection(collection: dict) -> Collection | None:
    """Normalizes a collection"""

    type = collection.get("type")
    if type is None or type not in (
        "Collection",
        "OrderedCollection",
        "CollectionPage",
        "OrderedCollectionPage",
    ):
        return None
    count = collection.get("totalItems")
    items = collection.get("orderedItems")
    if items is None:
        items = collection.get("items")

    data = {
        "id": collection.get("id"),
        "type": type,
        "count": count,
        "first": collection.get("first"),
        "last": collection.get("last"),
        "next": collection.get("next"),
        "prev": collection.get("prev"),
        "items": items,
    }

    if isinstance(data.get("first"), dict):
        data["next"] = data["first"].get("next")
        data["items"] = data["first"].get("items")
        data["first"] = None

    if data["items"]:
        data["items"] = convert_items(data["items"])

    return Collection.model_validate(data)
