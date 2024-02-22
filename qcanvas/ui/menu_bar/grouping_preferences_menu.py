from PySide6.QtCore import Slot, Signal
from PySide6.QtWidgets import QMenu, QWidget
from qasync import asyncSlot

import qcanvas.db as db
from qcanvas.util.course_indexer import DataManager
from qcanvas.util.helpers.qaction_helper import create_qaction


class GroupingPreferencesMenu(QMenu):
    _preference_changed_private = Signal(db.GroupByPreference)
    preference_changed = Signal()

    def __init__(self, data_manager: DataManager, parent: QWidget | None = None):
        super().__init__("Group files by", parent)
        self.setEnabled(False)

        self.data_manager = data_manager
        self._selected_course: db.Course | None = None

        self.group_by_modules_action = self._make_action("Modules", db.GroupByPreference.GROUP_BY_MODULES)
        self.group_by_pages_action = self._make_action("Pages", db.GroupByPreference.GROUP_BY_PAGES)

        self.addActions([self.group_by_pages_action, self.group_by_modules_action])

        self._preference_changed_private.connect(self._on_preference_changed)

    def _make_action(self, text: str, preference_value: db.GroupByPreference):
        return create_qaction(
            name=text,
            parent=self,
            triggered=lambda: self._preference_changed_private.emit(preference_value),
            checkable=True,
            checked=False
        )

    @Slot()
    def course_changed(self, course: db.Course | None):
        if course is not None:
            self._selected_course = course
            self._update_actions()
            self.setEnabled(True)
        else:
            self._selected_course = None
            self.setEnabled(False)

    @asyncSlot()
    async def _on_preference_changed(self, preference: db.GroupByPreference):
        if self._selected_course is not None:
            self._selected_course.preferences.files_group_by_preference = preference
            self._update_actions()
            # todo not sure if this should go in main_ui or here...
            await self.data_manager.update_item(self._selected_course.preferences)

            self.preference_changed.emit()

    def _update_actions(self):
        preference = self._selected_course.preferences.files_group_by_preference

        self.group_by_pages_action.setChecked(preference == db.GroupByPreference.GROUP_BY_PAGES)
        self.group_by_modules_action.setChecked(preference == db.GroupByPreference.GROUP_BY_MODULES)
