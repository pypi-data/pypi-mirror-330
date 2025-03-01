from pydantic import Field, BeforeValidator
from typing import Any, Annotated
from bovine.activitystreams.utils import id_for_object


from muck_out.transform import transform_url
from muck_out.transform.attachment import transform_attachments
from muck_out.transform.utils import sanitize_html

from .common import Common, CommonAll

HtmlStringOrNone = Annotated[str | None, BeforeValidator(sanitize_html)]
"""Used for strings, which may contain html"""

IdFieldOrNone = Annotated[str | None, BeforeValidator(id_for_object)]


class ObjectStub(Common):
    """Stub object"""

    attributedTo: IdFieldOrNone = Field(
        default=None,
        examples=["https://actor.example/"],
        description="id of the actor that authored this object",
    )
    content: HtmlStringOrNone = Field(
        default=None, description="The content of the object"
    )
    summary: HtmlStringOrNone = Field(
        default=None,
        description="The summary of the object",
    )
    name: HtmlStringOrNone = Field(
        default=None,
        description="The name of the object",
    )
    attachment: Annotated[
        list[dict[str, Any]] | None, BeforeValidator(transform_attachments)
    ] = Field(
        default=None,
        description="A list of objects that are attached to the original object",
    )
    tag: list[dict[str, Any]] | None = Field(
        default=None,
        description="A list of objects that expand on the content of the object",
    )
    url: Annotated[list[dict[str, Any]] | None, BeforeValidator(transform_url)] = Field(
        default=None,
        description="A list of urls that expand on the content of the object",
    )
    sensitive: bool | None = Field(
        None,
        description="""
    Marks the object as sensitive. Currently, used by everyone, a better way would be an element of the tag list that labels the object as sensitive due a reason
    """,
    )
    inReplyTo: IdFieldOrNone = Field(
        None,
        description="""
    The object being replied to. Currently a string. Not sure if this is what I want.
    """,
    )


class Activity(Common):
    """
    This represents a first draft of a json-schema that every activities exchanged between servers MUST satisfy and be able to parse. Here 'being able to parse' means making it to the point, where depending on the type, you decide what side effects to perform.

    Generally, the fields actor, to, and cc (and maybe bcc --- not transported) represent how the message is being delivered. The fields actor, type, object, target, content represent how the message is processed by the server.
    """

    actor: IdFieldOrNone = Field(
        default=None,
        examples=["https://actor.example/"],
        description="id of the actor performing this activity. One can assume that the activity is signed by this actor (in some form).",
    )
    object: str | ObjectStub | None = Field(
        default=None, description="The object of the activity"
    )
    target: str | dict[str, Any] | None = Field(
        default=None,
        examples=[
            "https://other.example/target_id",
            {"type": "Note", "content": "meow"},
        ],
        description="The target, not sure if needed, included for completeness",
    )
    content: HtmlStringOrNone = Field(
        default=None,
        examples=["🐮", "❤️"],
        description="The content used for example to represent the Emote for a like",
    )


class Actor(CommonAll):
    """Describes an ActivityPub actor"""

    type: str = Field(
        examples=["Person", "Service", "Application"],
        description="""The type of Actor""",
    )

    inbox: str | None = Field(
        None,
        examples=["https://actor.example/inbox"],
        description="""
    The inbox of the actor
    """,
    )

    outbox: str | None = Field(
        None,
        examples=["https://actor.example/outbox"],
        description="""
    The outbox of the actor
    """,
    )

    icon: dict | None = Field(
        None,
        examples=[{"type": "Image", "url": "https://actor.example/icon.png"}],
        description="""
    The avatar of the actor
    """,
    )

    summary: str | None = Field(
        None,
        examples=["My Fediverse account"],
        description="""
    Description of the actor
    """,
    )

    name: str | None = Field(
        None,
        examples=["Alice"],
        description="""
    Display name of the actor
    """,
    )

    also_known_as: list[str] | None = Field(
        None,
        examples=[["https://alice.example", "https://alice.example/profile"]],
        alias="alsoKnownAs",
        description="""
    Other uris associated with the actor
    """,
    )

    # attachments: list[dict | PropertyValue] | None = Field(
    #     None, description="""attachments ... currently used for property values"""
    # )


class CollectionStub(CommonAll):
    """Abstracts all the ActivityPub collection concepts"""

    type: str = Field(
        examples=[
            "Collection",
            "OrderedCollection",
            "CollectionPage",
            "OrdererCollectionPage",
        ],
        description="""Type of object""",
    )

    items: list[str] | None = Field(None, description="""The items""")

    next: str | None = Field(None)
    prev: str | None = Field(None)
    first: str | None = Field(None)
    last: str | None = Field(None)
    count: int | None = Field(None)
