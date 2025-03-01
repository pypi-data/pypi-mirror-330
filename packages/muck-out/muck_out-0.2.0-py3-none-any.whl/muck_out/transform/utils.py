from typing import List, Any
import nh3


def list_from_value(value: Any) -> List[Any] | None:
    """Transforms a list into a value

    ```pycon
    >>> list_from_value(["aaa"])
    ['aaa']

    >>> list_from_value("aaa")
    ['aaa']

    >>> list_from_value({"a": 1})
    [{'a': 1}]

    >>> list_from_value([])

    >>> list_from_value(None)

    ```


    :returns: A list or None in case of an empty list or None as argument

    """

    if isinstance(value, list):
        if len(value) == 0:
            return None
        return value
    if isinstance(value, str) or isinstance(value, dict):
        return [value]

    return None


allowed_html_tags = {
    "a",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "code",
    "em",
    "i",
    "li",
    "ol",
    "strong",
    "ul",
    "p",
    "br",
    "span",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
}
"""The currently allowed list of html tags"""


def sanitize_html(value: str | None) -> str | None:
    """Cleans html

    ```pycon
    >>> sanitize_html("<p>text</p>")
    '<p>text</p>'

    >>> sanitize_html("<script>alert('xss')</script>")
    ''

    ```
    """
    if isinstance(value, str):
        return nh3.clean(value, tags=allowed_html_tags)
    return None


def remove_html(value: str | None) -> str | None:
    """Removes html

    ```pycon
    >>> remove_html('<a href="http://location.test">location.test</p>')
    'location.test'

    ```
    """

    if isinstance(value, str):
        return nh3.clean(value, tags=set())
    return None
