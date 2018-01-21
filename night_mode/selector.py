from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QHBoxLayout, QVBoxLayout, QCheckBox

from .gui import create_button, AddonDialog


class StylerCheckButton(QCheckBox):

    def __init__(self, parent, styler):
        QCheckBox.__init__(self, styler.friendly_name, parent)
        self.styler = styler
        if styler.is_active:
            self.toggle()
        self.stateChanged.connect(self.switch_state)
        self.parent = parent

    def switch_state(self, state):
        self.parent.update(self.styler, state)


class StylersSelectorWindow(AddonDialog):

    def __init__(self, parent, disabled_stylers: set, all_stylers, title='Choose what to style', on_update=None):
        super().__init__(self, parent, Qt.Window)
        self.on_update = on_update
        self.disabled_stylers = disabled_stylers
        self.all_stylers = all_stylers

        self.init_ui(title)

    def init_ui(self, title):
        self.setWindowTitle(title)

        btn_close = create_button('Close', self.close)

        buttons = QHBoxLayout()

        buttons.addWidget(btn_close)
        buttons.setAlignment(Qt.AlignBottom)

        body = QVBoxLayout()
        body.setAlignment(Qt.AlignTop)

        header = QLabel(
            'Select which parts of Anki should be displayed '
            'in eye-friendly, dark colors.'
        )
        header.setAlignment(Qt.AlignCenter)

        stylers = QVBoxLayout()
        stylers.setAlignment(Qt.AlignTop)

        for styler in self.all_stylers:
            styler_checkbox = StylerCheckButton(self, styler)
            stylers.addWidget(styler_checkbox)

        self.stylers_checkboxes = stylers

        body.addWidget(header)
        body.addLayout(stylers)
        body.addStretch(1)
        body.addLayout(buttons)
        self.setLayout(body)

        self.setGeometry(300, 300, 350, 300)
        self.show()

    def update(self, styler, value):
        if value:
            self.disabled_stylers.remove(styler.name)
        else:
            self.disabled_stylers.add(styler.name)

        if self.on_update:
            self.on_update()
