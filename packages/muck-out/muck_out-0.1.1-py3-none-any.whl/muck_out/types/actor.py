from pydantic import BaseModel, Field


class PropertyValue(BaseModel):
    """
    Key value pairs in the attachment of an actor
    as used by Mastodon
    """

    type: str = Field("PropertyValue", description="""Fixed type for serialization""")

    name: str = Field(
        examples=["Pronouns"],
        description="""
    Key of the value
    """,
    )

    value: str = Field(
        examples=["They/them"],
        description="""
    Value
    """,
    )
