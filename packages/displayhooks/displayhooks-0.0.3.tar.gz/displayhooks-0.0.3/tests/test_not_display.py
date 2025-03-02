import io
import sys
from contextlib import redirect_stdout

import pytest

from displayhooks import not_display, autorestore_displayhook


@autorestore_displayhook
def test_not_display_only_ints():
    not_display(int)

    def display_something(something):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            sys.displayhook(something)

        return buffer.getvalue()

    assert display_something(5) == ''
    assert display_something('kek') == f'{repr("kek")}\n'


@pytest.mark.parametrize(
    ['callable'],
    [
        (lambda: not_display(int, float),),
        (lambda: [not_display(int), not_display(float)],),  # type: ignore[func-returns-value]
        (lambda: not_display(float, int),),
        (lambda: [not_display(float), not_display(int)],),  # type: ignore[func-returns-value]
    ],
)
@autorestore_displayhook
def test_not_display_ints_and_floats(callable):
    callable()

    def display_something(something):
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            sys.displayhook(something)

        return buffer.getvalue()

    assert display_something(5) == ''
    assert display_something(5.5) == ''
    assert display_something('kek') == f'{repr("kek")}\n'
