from dataclasses import dataclass
from typing import Type, Iterable, Generator


def get_dataclass_fields(cls: Type[dataclass], *, exclude_fields: Iterable[str] = ()) -> Generator[str, None, None]:
    for field in cls.__annotations__.keys():
        if field in exclude_fields:
            continue
        yield field
