import logging
from pathlib import Path

from aiofile import async_open
from pydantic import BaseModel, RootModel, Field, ValidationError

from qcanvas.util import paths

_logger = logging.getLogger(__name__)


class CourseConfigData(BaseModel):
    nickname: str | None = Field(default=None)

    async def save(self) -> None:
        await course_configs.save()


_CourseConfigurations = RootModel[dict[str, CourseConfigData]]


class _CourseConfig:
    def __init__(self):
        self._root_model = self._load_root_model()

    def _load_root_model(self) -> _CourseConfigurations:
        if self._storage_path.exists():
            try:
                return _CourseConfigurations.model_validate_json(
                    self._storage_path.read_text()
                )
            except ValidationError as e:
                _logger.error("Failed to load course configs", exc_info=e)

        return _CourseConfigurations({})

    async def save(self) -> None:
        async with async_open(self._storage_path, "wt") as file:
            await file.write(self._root_model.model_dump_json(indent=4))

    @property
    def _storage_path(self) -> Path:
        return paths.config_storage() / "course_settings.json"

    def __getitem__(self, item: str) -> CourseConfigData:
        if item in self._root_model.root:
            return self._root_model.root[item]
        else:
            new_config = CourseConfigData()
            self._root_model.root[item] = new_config
            return new_config


course_configs = _CourseConfig()
