from PyQt5.QtCore import Qt, pyqtSlot as slot, QTime
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QHBoxLayout, QVBoxLayout, QTimeEdit

from .gui import create_button, AddonDialog, iterate_widgets


class TimeEdit(QWidget):

    def __init__(self, parent, initial_time, label, on_update=lambda x: x):
        """

        Args:
            parent: ColorMapWindow instance
        """
        QWidget.__init__(self, parent)
        self.parent = parent
        self.on_update = on_update
        self.label = QLabel(label)
        self.qt_time = QTime.fromString(initial_time)
        self.time_edit = QTimeEdit(self.qt_time)
        self.time_edit.timeChanged.connect(self.update)
        self.grid = QGridLayout()
        self.fill_layout()
        self.setLayout(self.grid)

    @property
    def time(self):
        return self.qt_time.toPyTime().strftime('%H:%M')

    def fill_layout(self):
        grid = self.grid
        grid.addWidget(self.label, 0, 0)
        grid.addWidget(self.time_edit, 1, 0)

    @slot()
    def update(self):
        self.qt_time = self.time_edit.time()
        self.on_update(self.time)

    def update_constraint(self, min_time, max_time):
        pass


class ModeWindow(AddonDialog):

    def __init__(self, parent, settings, title='Manage Night Mode', on_update=lambda x: x):
        super().__init__(self, parent, Qt.Window)
        self.on_update = on_update
        self.settings = settings

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
            'If you choose an automatic (scheduled) mode '
            'the "ctrl+n" shortcut and menu checkbox for '
            'quick toggle will switch between the manual '
            'and automatic mode (when used for the first '
            'time).'
        )
        header.setWordWrap(True)

        mode_switches = QHBoxLayout()
        mode_switches.addWidget(QLabel('Mode:'))
        self.manual = create_button('Manual', self.on_set_manual)
        self.auto = create_button('Automatic', self.on_set_automatic)
        mode_switches.addWidget(self.manual)
        mode_switches.addWidget(self.auto)

        time_controls = QHBoxLayout()
        time_controls.setAlignment(Qt.AlignTop)

        start_at = TimeEdit(self, self.settings['start_at'], 'From', self.start_update)
        end_at = TimeEdit(self, self.settings['end_at'], 'To', self.end_update)
        time_controls.addWidget(start_at)
        time_controls.addWidget(end_at)

        self.time_controls = time_controls

        self.set_mode(self.settings['mode'], False)

        body.addWidget(header)
        body.addStretch(1)
        body.addLayout(mode_switches)
        body.addLayout(time_controls)
        body.addStretch(1)
        body.addLayout(buttons)
        self.setLayout(body)

        self.setGeometry(300, 300, 470, 255)
        self.show()

    def start_update(self, time):
        self.set_time('start_at', time)

    def end_update(self, time):
        self.set_time('end_at', time)

    def set_time(self, which, time):
        self.settings[which] = time
        self.on_update()

    @slot()
    def on_set_manual(self):
        self.set_mode('manual')

    @slot()
    def on_set_automatic(self):
        self.set_mode('auto')

    def switch_buttons(self, auto):
        self.auto.setEnabled(not auto)
        self.manual.setEnabled(auto)
        self.auto.setChecked(auto)
        self.manual.setChecked(not auto)

    def set_mode(self, mode, run_callback=True):
        auto = mode == 'auto'
        self.settings['mode'] = mode
        # time controls are needed only in the 'auto' mode
        for widget in iterate_widgets(self.time_controls):
            widget.setEnabled(auto)
        self.switch_buttons(auto)
        if run_callback:
            self.on_update()
