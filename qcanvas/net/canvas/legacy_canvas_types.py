from typing import Any, TypeVar, Type, cast


T = TypeVar("T")


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class LegacyPage:
    published: bool
    hide_from_students: bool
    locked_for_user: bool
    body: str | None

    def __init__(self, published: bool, hide_from_students: bool, locked_for_user: bool, body: str | None) -> None:
        self.published = published
        self.hide_from_students = hide_from_students
        self.locked_for_user = locked_for_user
        self.body = body

    @staticmethod
    def from_dict(obj: Any) -> 'LegacyPage':
        assert isinstance(obj, dict)
        published = from_bool(obj.get("published"))
        hide_from_students = from_bool(obj.get("hide_from_students"))
        locked_for_user = from_bool(obj.get("locked_for_user"))
        body = None if locked_for_user else from_str(obj.get("body"))
        return LegacyPage(published, hide_from_students, locked_for_user, body)

    def to_dict(self) -> dict:
        result: dict = {}
        result["published"] = from_bool(self.published)
        result["hide_from_students"] = from_bool(self.hide_from_students)
        result["locked_for_user"] = from_bool(self.locked_for_user)
        result["body"] = from_str(self.body)
        return result


class LegacyFile:
    id: int
    uuid: str
    display_name: str
    filename: str
    url: str
    size: int
    locked: bool
    hidden: bool
    hidden_for_user: bool
    locked_for_user: bool

    def __init__(self, id: int, uuid: str, display_name: str, filename: str, url: str, size: int, locked: bool, hidden: bool, hidden_for_user: bool, locked_for_user: bool) -> None:
        self.id = id
        self.uuid = uuid
        self.display_name = display_name
        self.filename = filename
        self.url = url
        self.size = size
        self.locked = locked
        self.hidden = hidden
        self.hidden_for_user = hidden_for_user
        self.locked_for_user = locked_for_user

    @staticmethod
    def from_dict(obj: Any) -> 'LegacyFile':
        assert isinstance(obj, dict)
        id = from_int(obj.get("id"))
        uuid = from_str(obj.get("uuid"))
        display_name = from_str(obj.get("display_name"))
        filename = from_str(obj.get("filename"))
        url = from_str(obj.get("url"))
        size = from_int(obj.get("size"))
        locked = from_bool(obj.get("locked"))
        hidden = from_bool(obj.get("hidden"))
        hidden_for_user = from_bool(obj.get("hidden_for_user"))
        locked_for_user = from_bool(obj.get("locked_for_user"))
        return LegacyFile(id, uuid, display_name, filename, url, size, locked, hidden, hidden_for_user, locked_for_user)

    def to_dict(self) -> dict:
        result: dict = {}
        result["id"] = from_int(self.id)
        result["uuid"] = from_str(self.uuid)
        result["display_name"] = from_str(self.display_name)
        result["filename"] = from_str(self.filename)
        result["url"] = from_str(self.url)
        result["size"] = from_int(self.size)
        result["locked"] = from_bool(self.locked)
        result["hidden"] = from_bool(self.hidden)
        result["hidden_for_user"] = from_bool(self.hidden_for_user)
        result["locked_for_user"] = from_bool(self.locked_for_user)
        return result


def legacy_page_from_dict(s: Any) -> LegacyPage:
    return LegacyPage.from_dict(s)


def legacy_page_to_dict(x: LegacyPage) -> Any:
    return to_class(LegacyPage, x)


def legacy_file_from_dict(s: Any) -> LegacyFile:
    return LegacyFile.from_dict(s)


def legacy_file_to_dict(x: LegacyFile) -> Any:
    return to_class(LegacyFile, x)
