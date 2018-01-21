# -*- coding: utf-8 -*-
# Copyright: Michal Krassowski <krassowski.michal@gmail.com>
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
"""
This plugin adds the function of night mode, similar that one implemented in AnkiDroid.

It adds a "view" menu entity (if it doesn't exist) with options like:

    switching night mode
    inverting colors of images or latex formulas
    modifying some of the colors

It provides shortcut ctrl+n to quickly switch mode and color picker to adjust some of color parameters.

After enabling night mode, add-on changes colors of menubar, toolbar, bottombars and content windows.

If you want to contribute visit GitHub page: https://github.com/krassowski/Anki-Night-Mode
Also, feel free to send me bug reports or feature requests.

Copyright: Michal Krassowski <krassowski.michal@gmail.com>
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html

Special thanks to contributors: [github nickname (reason)]

- b50 (initial compatibility with 2.1),
- ankitest (compatibility with 1508882486),
- omega3 (useful bug reports and suggestions)
- colchizin
- JulyMorning
"""
import traceback

from anki.hooks import addHook
from aqt import appVersion
from aqt import mw

from PyQt5.QtWidgets import QMessageBox

from .actions_and_settings import *
from .internals import alert
from .config import Config, ConfigValueGetter
from .icons import Icons
from .menu import get_or_create_menu, Menu
from .stylers import Styler
from .styles import Style, MessageBoxStyle

__addon_name__ = 'Night Mode'
__version__ = '2.1.5'
__anki_version__ = '2.1'


if not appVersion.startswith(__anki_version__):
    print(
        (
            'Unsupported version of Anki. '
            'Anki-Night-Mode 2.0 requires %s to work properly. '
            'For older versions of Anki use Night-Mode 1.x'
        ) % __anki_version__
    )


# Add here you color replacements mapping - old: new, comma separated


class StylingManager:
    def __init__(self, app):
        self.styles = Style.members
        self.stylers = [
            styler(app)
            for styler in Styler.members
        ]
        self.config = ConfigValueGetter(app.config)

    @property
    def active_stylers(self):
        return [
            styler
            for styler in self.stylers
            if styler.name not in self.config.disabled_stylers
        ]

    def replace(self):
        print(self.active_stylers)
        for styler in self.active_stylers:
            styler.replace_attributes()

    def restore(self):
        for styler in self.stylers:
            styler.restore_attributes()


class NightMode:

    menu_layout = [
        EnableNightMode,
        EnableInDialogs,
        '-',
        InvertImage,
        InvertLatex,
        TransparentLatex,
        '-',
        BackgroundColor,
        TextColor,
        ResetColors,
        '-',
        ModeSettings,
        UserColorMap,
        DisabledStylers,
        '-',
        About
    ]

    def __init__(self):
        self.profile_loaded = False
        self.config = Config(self, prefix='nm_')
        self.config.init_settings()
        self.icons = Icons()
        self.styles = StylingManager(self)

        view_menu = get_or_create_menu('addon_view_menu', '&View')
        self.menu = Menu(
            self,
            '&Night Mode',
            self.menu_layout,
            attach_to=view_menu
        )

        addHook('unloadProfile', self.save)
        addHook('profileLoaded', self.load)
        addHook('showQuestion', self.take_care_of_night_class)
        addHook('showAnswer', self.take_care_of_night_class)

    def load(self):
        """
        Load configuration from profile, set states of checkable menu objects
        and turn on night mode if it were enabled on previous session.
        """
        self.config.load()
        self.profile_loaded = True

        self.refresh()
        self.update_menu()

    def update_menu(self):
        self.menu.update_checkboxes(self.config.settings)

    def save(self):
        self.config.save()

    def on(self):
        """Turn on night mode."""
        self.styles.replace()

    def off(self):
        """Turn off night mode."""
        self.styles.restore()

    def refresh(self, reload=False):
        """
        Refresh display by re-enabling night or normal mode,
        regenerate customizable css strings.
        """
        state = self.config.state_on.value

        if not self.profile_loaded:
            alert(ERROR_NO_PROFILE)
            return

        try:
            if state:
                if reload:
                    self.off()
                self.on()
            else:
                self.off()
        except Exception:
            alert(ERROR_SWITCH % traceback.format_exc())
            return

        # Reload current screen.
        if mw.state == 'review':
            mw.moveToState('overview')
            mw.moveToState('review')
        if mw.state == 'deckBrowser':
            mw.deckBrowser.refresh()
        if mw.state == 'overview':
            mw.overview.refresh()

        # Redraw toolbar (should be always visible).
        mw.toolbar.draw()
        self.update_menu()
        return True

    def about(self):
        about_box = self.message_box()
        about_box.setText(__addon_name__ + ' ' + __version__ + __doc__)
        about_box.setGeometry(300, 300, 250, 150)
        about_box.setWindowTitle('About ' + __addon_name__ + ' ' + __version__)

        about_box.exec_()

    def message_box(self):
        box = QMessageBox()
        if self.config.state_on:
            box_style = MessageBoxStyle(self)
            box.setStyleSheet(box_style.style)
        return box

    def take_care_of_night_class(self, web_object=None):

        if not web_object:
            web_object = mw.reviewer.web

        if self.config.state_on:
            javascript = """
            current_classes = document.body.className;
            if(current_classes.indexOf("night_mode") == -1)
            {
                document.body.className += " night_mode";
            }
            """
        else:
            javascript = """
            current_classes = document.body.className;
            if(current_classes.indexOf("night_mode") != -1)
            {
                document.body.className = current_classes.replace("night_mode","");
            }
            """

        web_object.eval(javascript)


ERROR_NO_PROFILE = """Switching night mode failed: The profile is not loaded yet.
Probably it's a bug of Anki or you tried to switch mode to quickly."""

ERROR_SWITCH = """Switching night mode failed: Something went really really wrong.
Contact add-on author to get help.

Please provide following traceback when reporting the issue:
%s
"""
