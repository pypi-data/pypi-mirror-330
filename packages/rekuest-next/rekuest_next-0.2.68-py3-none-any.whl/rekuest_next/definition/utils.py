from rekuest_next.agents.context import is_context
from rekuest_next.state.predicate import is_state


try:
    from typing import Annotated, get_type_hints, Any, get_origin

    annot_type = type(Annotated[int, "spam"])

    def is_annotated(obj: Any) -> bool:
        """Checks if a hint is an Annotated type

        Args:
            hint (Any): The typehint to check
            annot_type (_type_, optional): _description_. Defaults to annot_type.

        Returns:
            bool: _description_
        """
        return get_origin(obj) is Annotated

except ImportError:
    Annotated = None
    from typing import get_type_hints as _get_type_hints, Any

    def get_type_hints(obj: Any, include_extras=False, **kwargs):
        return _get_type_hints(obj, **kwargs)

    def is_annotated(obj: Any) -> bool:
        """Checks if a hint is an Annotated type

        Args:
            hint (Any): The typehint to check
            annot_type (_type_, optional): _description_. Defaults to annot_type.

        Returns:
            bool: _description_
        """
        return False


def is_local_var(type):
    return is_context(type) or is_state(type)
