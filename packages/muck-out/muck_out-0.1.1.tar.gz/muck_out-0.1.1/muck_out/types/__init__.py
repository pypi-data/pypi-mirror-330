from pydantic import Field
from typing import List, Any, Dict

from .actor import PropertyValue
from .common import Common, CommonAll


class Object(Common):
    attributedTo: str = Field(
        examples=["https://actor.example/"],
        description="""
    id of the actor that authored this object
    """,
    )
    content: str = Field(
        description="""
    The content of the object
    """
    )
    summary: str | None = Field(
        None,
        description="""
    The summary of the object
    """,
    )
    name: str | None = Field(
        None,
        description="""
    The name of the object
    """,
    )
    attachment: List[Dict[str, Any]] | None = Field(
        None,
        description="""
    A list of objects that are attached to the original object
    """,
    )
    tag: List[Dict[str, Any]] | None = Field(
        None,
        description="""
    A list of objects that expand on the content of the object
    """,
    )
    url: List[Dict[str, Any] | str] | None = Field(
        None,
        description="""
    A list of urls that expand on the content of the object
    """,
    )
    sensitive: bool | None = Field(
        None,
        description="""
    Marks the object as sensitive. Currently, used by everyone, a better way would be an element of the tag list that labels the object as sensitive due a reason
    """,
    )
    inReplyTo: str | None = Field(
        None,
        description="""
    The object being replied to. Currently a string. Not sure if this is what I want.
    """,
    )
    id: str = Field(
        ...,
        examples=["https://actor.example/some_id"],
        description="""
    id of the activity, can be assumed to be globally unique. Some activities such as a Follow request will require an id to be valid. Servers may assume an id to be required. As assigning an id is 'trivial', one should assign one.
    """,
    )
    type: str = Field(
        ...,
        examples=["Follow", "Accept", "Create", "Undo", "Like"],
        description="""
    Type of the activity. Side effects of this activity are determine by this type.
    """,
    )
    to: List[str] = Field(
        ...,
        examples=[
            ["https://bob.example"],
            ["https://alice.example", "https://bob.example"],
        ],
        min_length=1,
        description="""
    Array of actors this activity is addressed to. It is sane to assume that an activity is addressed to at least one person.
    """,
    )


class Activity(Common):
    """
    This represents a first draft of a json-schema that every activities exchanged between servers MUST satisfy and be able to parse. Here 'being able to parse' means making it to the point, where depending on the type, you decide what side effects to perform.

    Generally, the fields actor, to, and cc (and maybe bcc --- not transported) represent how the message is being delivered. The fields actor, type, object, target, content represent how the message is processed by the server.
    """

    actor: str = Field(
        ...,
        examples=["https://actor.example/"],
        description="""
    id of the actor performing this activity. One can assume that the activity is signed by this actor (in some form).
    """,
    )
    object: str | Object | None = Field(None)
    target: str | Dict[str, Any] | None = Field(
        None,
        examples=[
            "https://other.example/target_id",
            {"type": "Note", "content": "meow"},
        ],
        description="""
    The target, not sure if needed, included for completeness
    """,
    )
    content: str | None = Field(
        None,
        examples=["🐮", "❤️"],
        description="""
    The content used for example to represent the Emote for a like
    """,
    )
    id: str = Field(
        ...,
        examples=["https://actor.example/some_id"],
        description="""
    id of the activity, can be assumed to be globally unique. Some activities such as a Follow request will require an id to be valid. Servers may assume an id to be required. As assigning an id is 'trivial', one should assign one.
    """,
    )
    type: str = Field(
        ...,
        examples=["Follow", "Accept", "Create", "Undo", "Like"],
        description="""
    Type of the activity. Side effects of this activity are determine by this type.
    """,
    )
    to: List[str] = Field(
        ...,
        examples=[
            ["https://bob.example"],
            ["https://alice.example", "https://bob.example"],
        ],
        min_length=1,
        description="""
    Array of actors this activity is addressed to. It is sane to assume that an activity is addressed to at least one person.
    """,
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

    also_known_as: List[str] | None = Field(
        None,
        examples=[["https://alice.example", "https://alice.example/profile"]],
        alias="alsoKnownAs",
        description="""
    Other uris associated with the actor
    """,
    )

    attachments: List[dict | PropertyValue] | None = Field(
        None, description="""attachments ... currently used for property values"""
    )


class Collection(CommonAll):
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

    items: List[str] | None = Field(None, description="""The items""")

    next: str | None = Field(None)
    prev: str | None = Field(None)
    first: str | None = Field(None)
    last: str | None = Field(None)
    count: int | None = Field(None)
