import pytest

from .content import normalize_content


@pytest.mark.parametrize(
    "input,output",
    [({}, None), ({"content": "moo"}, "moo"), ({"contentMap": {"en": "moo"}}, "moo")],
)
def test_basic_content(input, output):
    result = normalize_content(input)

    assert result == output
