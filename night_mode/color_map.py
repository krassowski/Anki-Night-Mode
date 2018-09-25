from PyQt5.QtCore import Qt, pyqtSlot as slot
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QLabel, QGridLayout, QPushButton, QColorDialog, QHBoxLayout, QVBoxLayout

from .internals import alert
from .gui import create_button, remove_layout, AddonDialog
from .languages import _


class ColorSwatch(QPushButton):

    def __init__(self, parent, color=None, on_color_change=None, name='Color', verify_colors=False):
        """

        Args:
            parent: a parent Qt instance
            color: the color name or hexadecimal code (in form of a string)
            on_color_change: a function or method taking old color and a new one
            verify_colors: should the parent be asked if the color is acceptable?
                to verify a color parent.is_acceptable(color) will be invoked
        """
        QPushButton.__init__(self, color, parent)
        self.verify_colors = verify_colors
        self.parent = parent
        self.color = color
        self.name = name
        self.callback = on_color_change

        if color:
            self.set_color(color)
        else:
            self.setText(_('(Not specified)'))

        self.clicked.connect(self.pick_color)

    def set_color(self, color):
        self.color = color
        self.setText(color)
        self.setStyleSheet(f'background-color: {self.color}; color: {self.text_color}')

    @property
    def text_color(self):
        return 'black' if self.qt_color.lightness() > 127 else 'white'

    @property
    def qt_color(self):
        return QColor(self.color)

    @slot()
    def pick_color(self, qt_color=None):
        if not qt_color:
            qt_color = self.qt_color

        old_color = self.color
        qt_color = QColorDialog.getColor(
            qt_color,
            parent=self,
            title=_('Select %s') % _(self.name)
        )

        if qt_color.isValid():
            color = qt_color.name()
            if self.verify_colors and not self.parent.is_acceptable(color):
                alert(_('This color (%s) is already mapped. Please select a different one.') % color)
                return self.pick_color(qt_color=qt_color)

            self.set_color(color)
            self.callback(old_color, self.color)


class ColorMapping(QWidget):

    def __init__(self, parent, normal_color, night_color):
        """

        Args:
            parent: ColorMapWindow instance
            normal_color: name or code of code to use in normal mode
            night_color: name or code of code to use in night mode
        """
        QWidget.__init__(self, parent)
        self.parent = parent
        self.normal = ColorSwatch(self, normal_color, self.update_normal, 'Normal Mode Color', verify_colors=True)
        self.night = ColorSwatch(self, night_color, self.update_night, 'Night Mode Color')
        self.grid = QGridLayout()
        self.fill_layout()
        self.setLayout(self.grid)

    def fill_layout(self):
        remove = create_button('Remove', self.remove)
        grid = self.grid
        grid.addWidget(self.normal, 0, 1, 1, 3)
        arrow = QLabel('→')
        arrow.setAlignment(Qt.AlignCenter)
        grid.addWidget(arrow, 0, 4)
        grid.addWidget(self.night, 0, 5, 1, 3)
        grid.addWidget(remove, 0, 8)

    @slot()
    def remove(self):
        self.parent.update(self.normal.color, None, None)
        remove_layout(self.grid)
        self.parent.mappings.removeWidget(self)
        self.deleteLater()

    def update_normal(self, old, new):
        night = self.night.color
        self.parent.update(old, new, night)

    def update_night(self, old, new):
        normal = self.normal.color
        self.parent.update(normal, normal, new)

    def is_acceptable(self, color):
        return self.parent.is_acceptable(color)


class ColorMapWindow(AddonDialog):

    def __init__(self, parent, color_map, title='Customise colors swapping', on_update=None):
        super().__init__(self, parent, Qt.Window)
        self.on_update = on_update
        self.color_map = color_map

        self.init_ui(title)

    def init_ui(self, title):
        self.setWindowTitle(_(title))

        btn_add_mapping = create_button('+ Add colors mapping', self.on_add)
        btn_close = create_button('Close', self.close)

        buttons = QHBoxLayout()

        buttons.addWidget(btn_close)
        buttons.addWidget(btn_add_mapping)
        buttons.setAlignment(Qt.AlignBottom)

        body = QVBoxLayout()
        body.setAlignment(Qt.AlignTop)

        header = QLabel(_(
            'Specify how particular colors on your cards '
            'should be swapped when the night mode is on.'
        ))
        header.setAlignment(Qt.AlignCenter)

        mappings = QVBoxLayout()
        mappings.setAlignment(Qt.AlignTop)

        for normal_color, night_color in self.color_map.items():
            mapping = ColorMapping(self, normal_color, night_color)
            mappings.addWidget(mapping)

        self.mappings = mappings

        body.addWidget(header)
        body.addLayout(mappings)
        body.addStretch(1)
        body.addLayout(buttons)
        self.setLayout(body)

        self.setGeometry(300, 300, 350, 300)
        self.show()

    @slot()
    def on_add(self):
        mapping = ColorMapping(self, None, None)
        self.mappings.addWidget(mapping)
        mapping.normal.pick_color()
        mapping.night.pick_color()

    def is_acceptable(self, color):
        return color not in self.color_map

    def update(self, old_key, new_key, new_value):
        if old_key:
            del self.color_map[old_key]
        if new_key:
            self.color_map[new_key] = new_value
        if self.on_update:
            self.on_update()
