from typing import Sequence, Any

from sqlalchemy.orm import Mapped, mapped_column


class HasColumnData:
    def get_column_data(self, column: int, role : int) -> str | None:
        raise NotImplementedError()


class HasText:
    @property
    def text(self) -> str:
        raise NotImplementedError()


class HasParent:
    @property
    def parent(self) -> Any:
        raise NotImplementedError()

    @property
    def index_of_self(self) -> int:
        raise NotImplementedError()


class HasChildren:
    @property
    def collapsed(self) -> bool:
        raise NotImplementedError()

    @collapsed.setter
    def collapsed(self, value: bool):
        raise NotImplementedError()

    @property
    def children(self) -> Sequence[HasColumnData]:
        raise NotImplementedError()
