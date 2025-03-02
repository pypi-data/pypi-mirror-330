import sys
from typing import Callable, Any
from threading import Lock
from functools import wraps


lock = Lock()

def converted_displayhook(function: Callable[[Any], Any]) -> Callable[[Any], Any]:
    with lock:
        old_displayhook = sys.displayhook

        @wraps(function)
        def new_displayhook(value: Any) -> Any:
            return old_displayhook(function(value))

        sys.displayhook = new_displayhook

    return new_displayhook
