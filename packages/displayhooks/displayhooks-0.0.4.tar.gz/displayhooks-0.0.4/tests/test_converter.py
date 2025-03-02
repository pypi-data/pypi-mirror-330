import io
import sys
from contextlib import redirect_stdout
from typing import Any

import pytest

from displayhooks import converted_displayhook, autorestore_displayhook


@pytest.mark.parametrize(
    ['value'],
    [
        ('kek',),
        ('lol',),
        (1,),
        (1.5,),
    ],
)
@autorestore_displayhook
def test_empty_convert(value):
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:
        return value

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(value)

    output = buffer.getvalue()

    assert output == f'{repr(value)}\n'


@autorestore_displayhook
def test_empty_convert_with_none():
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:
        return value

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(None)

    output = buffer.getvalue()

    assert output == ''


@pytest.mark.parametrize(
    ['value'],
    [
        ('kek',),
        ('lol',),
        (1,),
        (1.5,),
    ],
)
@autorestore_displayhook
def test_elliminating_convertion(value):
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:
        return None

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(value)

    output = buffer.getvalue()

    assert output == ''


@autorestore_displayhook
def test_elliminating_convertion_with_none():
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:
        return None

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(None)

    output = buffer.getvalue()

    assert output == ''


@pytest.mark.parametrize(
    ['value'],
    [
        ('kek',),
        ('lol',),
        (1,),
        (1.5,),
    ],
)
@autorestore_displayhook
def test_real_convertion(value):
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:
        return 'cheburek'

    buffer = io.StringIO()
    with redirect_stdout(buffer):
        sys.displayhook(value)

    output = buffer.getvalue()

    assert output == f'{repr("cheburek")}\n'
