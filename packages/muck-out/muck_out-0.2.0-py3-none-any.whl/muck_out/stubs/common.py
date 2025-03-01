from pydantic import BaseModel, Field, BeforeValidator
from typing import Annotated

from muck_out.transform.utils import list_from_value
from muck_out.transform import transform_to


class CommonAll(BaseModel):
    """Common base for all ActivityPub objects.

    Note `@context` is normalized to be a list, i.e

    ```pycon
    >>> CommonAll.model_validate({"@context":
    ...     "https://www.w3.org/ns/activitystreams"})
    CommonAll(field_context=['https://www.w3.org/ns/activitystreams'], id=None)

    ```
    """

    field_context: Annotated[
        list[str | dict] | None, BeforeValidator(list_from_value)
    ] = Field(
        default=None,
        alias="@context",
        examples=[
            ["https://www.w3.org/ns/activitystreams"],
            ["https://www.w3.org/ns/activitystreams", {"Hashtag": "as:Hashtag"}],
        ],
        description="The Json-LD context",
    )
    id: str | None = Field(
        default=None,
        examples=["https://actor.example/some_id"],
        description="id of the activity or object, can be assumed to be globally unique. Some activities such as a Follow request will require an id to be valid. Servers may assume an id to be required. As assigning an id is 'trivial', one should assign one.",
    )


class Common(CommonAll):
    to: Annotated[list[str] | None, BeforeValidator(transform_to)] = Field(
        default=None,
        examples=[
            ["https://bob.example"],
            ["https://alice.example", "https://bob.example"],
        ],
        min_length=1,
        description="Array of actors this activity or object is addressed to. It is sane to assume that an activity is addressed to at least one person.",
    )
    cc: Annotated[list[str] | None, BeforeValidator(transform_to)] = Field(
        default=None,
        examples=[
            ["https://bob.example"],
            ["https://alice.example", "https://bob.example"],
        ],
        description="Array of actors this activity or object is carbon copied to.",
    )
    published: str | None = Field(
        default=None,
        description="Moment of this activity or object being published",
    )
    type: str | None = Field(
        default=None,
        examples=["Follow", "Accept", "Create", "Undo", "Like", "Note"],
        description="Type of the activity or activity. Side effects of this activity are determine by this type.",
    )
