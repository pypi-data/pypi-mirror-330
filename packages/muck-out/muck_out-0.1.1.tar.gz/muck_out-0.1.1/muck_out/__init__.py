"""
This package contains tools to turn ActivityPub messages
into something cleaner. Its takes include

- Normalization
- Validation


"""

from pydantic import BaseModel, Field

from .types import Activity, Object, Actor, Collection

from .normalize import normalize_activity, normalize_object
from .actor import normalize_actor
from .collection import normalize_collection


class NormalizationResult(BaseModel):
    object: Object | None
    activity: Activity | None
    embedded_object: Object | None = Field(None, serialization_alias="embeddedObject")
    actor: Actor | None
    collection: Collection | None


def normalize(data: dict):
    def result_or_none(func):
        try:
            return func(data)
        except Exception:
            return None

    activity = result_or_none(normalize_activity)

    if activity and isinstance(activity.object, Object):
        embedded_object = activity.object
        activity.object = embedded_object.id
    else:
        embedded_object = None

    return NormalizationResult(
        object=result_or_none(normalize_object),
        activity=activity,
        embedded_object=embedded_object,
        actor=result_or_none(normalize_actor),
        collection=result_or_none(normalize_collection),
    )
