import sys

import pytest
import full_match

from displayhooks import autorestore_displayhook


def test_restore():
    hook_before_declaration = sys.displayhook
    @autorestore_displayhook
    def do_something():
        sys.displayhook = 5

    hook_before_calling = sys.displayhook

    do_something()

    assert hook_before_declaration is sys.displayhook
    assert hook_before_calling is sys.displayhook


def test_restore_after_exception():
    hook_before_declaration = sys.displayhook
    @autorestore_displayhook
    def do_something():
        sys.displayhook = 5
        raise ValueError('message')

    hook_before_calling = sys.displayhook

    with pytest.raises(ValueError, match=full_match('message')):
        do_something()

    assert hook_before_declaration is sys.displayhook
    assert hook_before_calling is sys.displayhook
