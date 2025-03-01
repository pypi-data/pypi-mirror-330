import pytest

from . import ObjectStub


@pytest.mark.parametrize(
    "url,expected",
    [
        ("http://remote.test", [{"type": "Link", "href": "http://remote.test"}]),
        (["http://remote.test"], [{"type": "Link", "href": "http://remote.test"}]),
        (
            [{"type": "Link", "href": "http://remote.test"}],
            [{"type": "Link", "href": "http://remote.test"}],
        ),
        (
            {"type": "Link", "href": "http://remote.test"},
            [{"type": "Link", "href": "http://remote.test"}],
        ),
        (
            ["http://one.test", {"type": "Link", "href": "http://two.test"}],
            [
                {"type": "Link", "href": "http://one.test"},
                {"type": "Link", "href": "http://two.test"},
            ],
        ),
    ],
)
def test_object_stub_url(url, expected):
    stub = ObjectStub(url=url)  # type:ignore

    assert stub.url == expected


def test_object_sub_content():
    stub = ObjectStub(content="content")  # type:ignore

    assert stub.content == "content"
