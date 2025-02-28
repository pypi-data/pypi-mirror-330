import pytest
from pydantic import ValidationError

from .types import Activity, Object
from .normalize import normalize_activity, normalize_object


@pytest.mark.parametrize("activity", [{}])
def test_normalize_activity_invalid(activity):
    with pytest.raises(ValueError):
        normalize_activity(activity)


@pytest.mark.parametrize("obj", [{}])
def test_normalize_object_invalid(obj):
    with pytest.raises(ValidationError):
        normalize_object(obj)


def activity_with_default_context(**kwargs):
    return Activity.model_validate(
        {"@context": "https://www.w3.org/ns/activitystreams", **kwargs}
    )


@pytest.mark.parametrize(
    ["activity", "expected"],
    [
        (
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": "http://remote.test/activity_id",
                "type": "Activity",
                "actor": "http://remote.test/actor",
                "to": "http://actor.example",
                "object": "http://actor.example/object",
            },
            activity_with_default_context(
                id="http://remote.test/activity_id",
                type="Activity",
                actor="http://remote.test/actor",
                to=["http://actor.example"],
                object="http://actor.example/object",
            ),
        ),
        (
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": "http://remote.test/activity_id",
                "type": "Activity",
                "actor": "http://remote.test/actor",
                "to": "http://actor.example",
                "cc": "http://other.example",
                "object": "http://actor.example/object",
                "published": "2024-09-26T18:35:42Z",
                "target": "http://actor.example/target",
                "content": "moo",
            },
            activity_with_default_context(
                id="http://remote.test/activity_id",
                type="Activity",
                actor="http://remote.test/actor",
                to=["http://actor.example"],
                cc=["http://other.example"],
                object="http://actor.example/object",
                published="2024-09-26T18:35:42Z",
                target="http://actor.example/target",
                content="moo",
            ),
        ),
        (
            {
                "@context": "https://www.w3.org/ns/activitystreams",
                "id": "http://remote.test/activity_id",
                "type": "Activity",
                "actor": {"type": "Person", "id": "http://remote.test/actor"},
                "to": "http://actor.example",
                "object": "http://actor.example/object",
            },
            activity_with_default_context(
                id="http://remote.test/activity_id",
                type="Activity",
                actor="http://remote.test/actor",
                to=["http://actor.example"],
                object="http://actor.example/object",
            ),
        ),
    ],
)
def test_normalize_activity_valid(activity, expected):
    result = normalize_activity(activity)

    assert result == expected


@pytest.mark.parametrize(
    ["new_values", "new_expected"],
    [
        ({}, {}),
        (
            {"attachment": {"href": "https://funfedi.dev", "type": "Link"}},
            {"attachment": [{"href": "https://funfedi.dev", "type": "Link"}]},
        ),
        ({"sensitive": True}, {"sensitive": True}),
        ({"content": "<b>bold</b>"}, {"content": "<b>bold</b>"}),
        ({"summary": "test"}, {"summary": "test"}),
        (
            {"summary": "test <script>alert('hi')</script>"},
            {"summary": "test "},
        ),
        (
            {"tag": {"type": "Hashtag", "name": "#test"}},
            {"tag": [{"type": "Hashtag", "name": "#test"}]},
        ),
        (
            {"url": "https://remote.test/"},
            {"url": [{"type": "Link", "href": "https://remote.test/"}]},
        ),
        (
            {"inReplyTo": {"id": "https://remote.test/to_reply", "type": "Note"}},
            {"inReplyTo": "https://remote.test/to_reply"},
        ),
    ],
)
def test_normalize_object(new_values, new_expected):
    obj = {
        "@context": "https://www.w3.org/ns/activitystreams",
        "id": "http://remote.test/object_id",
        "type": "Activity",
        "attributedTo": "http://remote.test/actor",
        "to": "http://actor.example",
        "content": "text",
        **new_values,
    }
    expected = Object.model_validate(
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": "http://remote.test/object_id",
            "type": "Activity",
            "attributedTo": "http://remote.test/actor",
            "to": ["http://actor.example"],
            "content": "text",
            **new_expected,
        }
    )

    result = normalize_object(obj)

    assert result == expected


@pytest.mark.parametrize(
    "example",
    [
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": "http://mastodon/users/hippo#rejects/follows/1",
            "type": "Reject",
            "actor": "http://mastodon/users/hippo",
            "object": {
                "id": "http://abel/actor/Ahua3T7U2umku3O4U3wrqg#1.8q4hyllt5j",
                "type": "Follow",
                "actor": "http://abel/actor/Ahua3T7U2umku3O4U3wrqg",
                "object": "http://mastodon/users/hippo",
            },
        },
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "id": "http://mastodon/users/hippo#accepts/follows/",
            "type": "Accept",
            "actor": "http://mastodon/users/hippo",
            "object": {
                "id": "http://abel/actor/lTS2tmsmXuLqcFBWYBjnbQ#1.8huk5ukb1i",
                "type": "Follow",
                "actor": "http://abel/actor/lTS2tmsmXuLqcFBWYBjnbQ",
                "object": "http://mastodon/users/hippo",
            },
        },
        {
            "@context": "https://www.w3.org/ns/activitystreams",
            "type": "Accept",
            "actor": "http://abel/actor/u4Kq-wez2koDZsLQfZKN5g",
            "to": ["http://banach/actor/T27aBR0fkpFwEkgzVTlFdg"],
            "published": "2024-11-07T14:50:28Z",
            "object": "follow:405205da-1723-4099-a69f-6d63b4937b34",
        },
    ],
)
def test_normalize_activity_examples(example):
    normalize_activity(example, actor="http://abel/actor/Ahua3T7U2umku3O4U3wrqg")
