from typing import Sequence, Any

from sqlalchemy.orm import Mapped, mapped_column


class HasColumnData:
    def get_column_data(self, column: int) -> str | None:
        raise NotImplementedError()


class HasParent:
    def parent(self) -> Any:
        raise NotImplementedError()

    def index_of_self(self) -> int:
        raise NotImplementedError()


class HasChildren:
    collapsed: Mapped[bool] = mapped_column(default=False, init=False)

    def get_children(self) -> Sequence[HasColumnData]:
        raise NotImplementedError()
