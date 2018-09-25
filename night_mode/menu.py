from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QAction, QMenu

from aqt import mw

from .languages import _


def get_or_create_menu(attribute_name, label):

    if not hasattr(mw, attribute_name):
        menu = QMenu(_(label), mw)
        setattr(mw, attribute_name, menu)

        mw.form.menubar.insertMenu(
            mw.form.menuTools.menuAction(),
            menu
        )
    else:
        menu = getattr(mw, attribute_name)
        menu.setTitle(_(label))

    return menu


class Menu:

    actions = {
        # action name => action
    }

    connections = {
        # action => callback
    }

    def __init__(self, app, menu_name, layout, attach_to=None):
        self.menu = QMenu(_(menu_name), mw)

        if attach_to:
            attach_to.addMenu(self.menu)

        layout = [
            entry(app) if hasattr(entry, 'action') else entry
            for entry in layout
        ]

        self.raw_actions = {
            entry.name: entry
            for entry in layout
            if hasattr(entry, 'action')
        }

        for action in self.raw_actions.values():

            self.create_action(
                action.name,
                _(action.label),
                action.action,
                checkable=action.checkable,
                shortcut=action.shortcut
            )

        self.setup_layout(layout)
        self.setup_connections()

    def create_action(self, name, text, callback, checkable=False, shortcut=None):
        action = QAction(_(text), mw, checkable=checkable)

        if shortcut:
            toggle = QKeySequence(shortcut)
            action.setShortcut(toggle)

        if name in self.actions:
            message = 'Action {0} already exists'.format(name)
            raise Exception(message)

        self.actions[name] = action
        self.connections[action] = callback

    def set_checked(self, name, value=True):
        self.actions[name].setChecked(value)

    def setup_layout(self, layout):
        for entry in layout:
            if entry == '-':
                self.menu.addSeparator()
            else:
                action = self.actions[entry.name]
                self.menu.addAction(action)

    def setup_connections(self):
        for menu_entry, connection in self.connections.items():
            self.connect(menu_entry, connection)

    def connect(self, action, callback):
        action.triggered.connect(callback)

    def update_checkboxes(self, settings):
        for name, setting in settings.items():
            if name in self.actions and self.raw_actions[name].checkable:
                self.set_checked(name, setting.is_checked)
