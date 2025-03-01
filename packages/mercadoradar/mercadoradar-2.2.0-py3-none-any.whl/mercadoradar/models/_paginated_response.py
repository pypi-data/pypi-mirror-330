from typing import Generic, TypeVar, List, Optional

from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class PaginatedResponse(BaseModel, Generic[T]):
    count: int
    next: Optional[str]
    previous: Optional[str]
    results: List[T]

    def to_str(self) -> str:
        items = []
        for item in self.results:
            item_repr = repr(item)
            item_lines = item_repr.split('\n')

            item_indented = "\n        ".join(item_lines)
            items.append(item_indented)

        items_str = ",\n        ".join(items)

        return (
            f"<PaginatedResponse\n"
            f"    count={self.count}\n"
            f"    next={self.next}\n"
            f"    previous={self.previous}\n"
            f"    results=[\n        {items_str}\n"
            f"    ]\n"
            f">"
        )

    def __str__(self) -> str:
        return self.to_str()

    def __repr__(self) -> str:
        return self.to_str()
