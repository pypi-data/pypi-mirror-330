from typing import Any

from typing_extensions import _AnnotatedAlias

from classiq.interface.exceptions import ClassiqValueError
from classiq.interface.generator.functions.port_declaration import (
    PortDeclarationDirection,
)

annotation_map: dict[PortDeclarationDirection, str] = {
    PortDeclarationDirection.Input: PortDeclarationDirection.Input.name,
    PortDeclarationDirection.Output: PortDeclarationDirection.Output.name,
}


def validate_annotation(type_hint: Any) -> None:
    if not isinstance(type_hint, _AnnotatedAlias):
        return
    directions: list[PortDeclarationDirection] = [
        direction
        for direction in type_hint.__metadata__
        if isinstance(direction, PortDeclarationDirection)
    ]
    if len(directions) <= 1:
        return
    raise ClassiqValueError(
        f"Multiple directions are not allowed in a single type hint: "
        f"[{', '.join(annotation_map[direction] for direction in reversed(directions))}]\n"
    )
