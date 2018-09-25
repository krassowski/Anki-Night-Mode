from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QCheckBox

from .gui import create_button, AddonDialog
from .languages import _


class StylerCheckButton(QCheckBox):

    def __init__(self, parent, styler):
        QCheckBox.__init__(self, _(styler.friendly_name), parent)
        self.styler = styler
        if styler.is_active:
            self.toggle()
        self.stateChanged.connect(self.switch_state)
        self.parent = parent

    def switch_state(self, state):
        self.parent.update(self.styler, state)


class StylersSelectorWindow(AddonDialog):

    def __init__(self, parent, disabled_stylers: set, all_stylers, title=_('Choose what to style'), on_update=None):
        super().__init__(self, parent, Qt.Window)
        self.on_update = on_update
        self.disabled_stylers = disabled_stylers
        self.all_stylers = all_stylers

        self.stylers_checkboxes = []
        self.stylers_layout = None
        self.init_ui(title)

    def init_ui(self, title):
        self.setWindowTitle(title)

        btn_close = create_button('Close', self.close)

        buttons = QHBoxLayout()

        buttons.addWidget(btn_close)
        buttons.setAlignment(Qt.AlignBottom)

        body = QVBoxLayout()
        body.setAlignment(Qt.AlignTop)

        header = QLabel(_(
            'Select which parts of Anki should be displayed '
            'in eye-friendly, dark colors.\n\n'
            'To disable all dialog windows, '
            'use the "Enable in dialogs" switch which is available in menu.'
        ))
        header.setAlignment(Qt.AlignCenter)

        stylers = QVBoxLayout()
        stylers.setAlignment(Qt.AlignTop)

        for styler in sorted(self.all_stylers, key=lambda s: s.name):
            styler_checkbox = StylerCheckButton(self, styler)
            self.stylers_checkboxes.append(styler_checkbox)
            stylers.addWidget(styler_checkbox)

        self.stylers_layout = stylers

        checked_boxes = sum(1 for checkbox in self.stylers_checkboxes if checkbox.isChecked())
        check_all = QCheckBox(_('Check/uncheck all'), self)
        check_all.setChecked(checked_boxes > len(self.stylers_checkboxes) / 2)
        check_all.stateChanged.connect(self.check_uncheck_all)

        body.addWidget(header)
        body.addWidget(check_all)
        body.addLayout(stylers)
        body.addStretch(1)
        body.addLayout(buttons)
        self.setLayout(body)

        self.setGeometry(300, 300, 350, 300)
        self.show()

    def check_uncheck_all(self, state):
        for checkbox in self.stylers_checkboxes:
            checkbox.setChecked(state)

    def update(self, styler, value):
        if value:
            self.disabled_stylers.remove(styler.name)
        else:
            self.disabled_stylers.add(styler.name)

        if self.on_update:
            self.on_update()
