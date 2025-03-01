from m3_ext.ui.all_components import (
    ExtButton,
)
from objectpack.ui import (
    BaseListWindow,
)

from educommon.utils.ui import (
    append_template_globals,
)


class TransferredEntityListWindow(BaseListWindow):
    """Окно реестра сущностей для сбора и экспорта данных."""

    def _init_components(self):
        """Инициализация компонентов окна."""
        super()._init_components()

        self.export_off_button = ExtButton(
            text='Отключить экспорт', handler='offExport'
        )
        self.export_on_button = ExtButton(
            text='Включить экспорт', handler='onExport'
        )

    def _do_layout(self):
        """Размещение компонентов окна на форме."""
        super()._do_layout()

        self.grid.top_bar.items.extend((self.export_off_button, self.export_on_button))

    def set_params(self, params, *args, **kwargs):
        """Настройка окна."""
        super().set_params(params, *args, **kwargs)

        append_template_globals(self, 'ui-js/transferred-entity-list.js')
        self.export_change_action_url = (
            params['pack'].export_change_action.get_absolute_url()
        )
        self.pack = params['pack']
