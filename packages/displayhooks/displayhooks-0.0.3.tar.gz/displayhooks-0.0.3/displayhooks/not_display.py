from typing import Type, Any

from displayhooks.converter import converted_displayhook


def not_display(*some_types: Type[Any]) -> None:
    @converted_displayhook
    def new_displayhook(value: Any) -> Any:
        for some_type in some_types:
            if isinstance(value, some_type):
                return None

        return value
