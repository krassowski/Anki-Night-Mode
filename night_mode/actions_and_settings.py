from datetime import datetime

from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog

from .internals import Setting, MenuAction, alert
from .color_map import ColorMapWindow
from .mode import ModeWindow
from .selector import StylersSelectorWindow


class UserColorMap(Setting, MenuAction):
    value = {'#000000': 'white'}
    window = None
    label = 'Customise colors on cards'

    def action(self):
        from aqt import mw as main_window
        if not self.window:
            # self.value is mutable, any modifications done by ColorMapWindow
            # will be done on the value of this singleton class object
            self.window = ColorMapWindow(
                main_window,
                self.value,
                on_update=self.on_colors_changed
            )
        self.window.show()

    def on_colors_changed(self):
        self.app.refresh()


class InvertImage(Setting, MenuAction):
    """Toggles image inversion.

    To learn how images are inverted check also append_to_styles().
    """

    # setting
    value = False

    # menu action
    label = '&Invert images'
    checkable = True

    def action(self):
        self.value = not self.value
        self.app.refresh()


class InvertLatex(Setting, MenuAction):
    """Toggles latex inversion.

    Latex formulas are nothing more than images with class "latex".
    To learn how formulas are inverted check also append_to_styles().
    """
    value = False
    label = 'Invert &latex'
    checkable = True

    def action(self):
        self.value = not self.value
        self.app.refresh()


class TransparentLatex(Setting, MenuAction):
    """Toggles transparent latex generation.

    See make_latex_transparent() for details.
    """
    value = False
    label = 'Force transparent latex'
    checkable = True

    def action(self):
        self.value = not self.value
        if self.value:
            self.make_latex_transparent()

    def make_latex_transparent(self):
        """Overwrite latex generation commands to use transparent images.

        Already generated latex images won't be affected;
        delete those manually from your media folder in order
        to regenerate images in transparent version.
        """

        commands = self.get_commands()

        for command in commands:
            command[1] = [
                "dvipng",
                "-D", "200",
                "-T", "tight",
                "-bg", "Transparent",
                "-z", "9",  # use maximal PNG compression
                "tmp.dvi",
                "-o", "tmp.png"
            ]

    @staticmethod
    def get_commands():
        from anki.latex import pngCommands
        from anki.latex import svgCommands
        commands = []
        commands.extend([pngCommands, svgCommands])
        return commands

    def on_load(self):
        if self.value:
            self.make_latex_transparent()


class ColorAction(Setting, MenuAction):

    def action(self):
        qt_color_old = QColor(self.value)
        qt_color = QColorDialog.getColor(qt_color_old)

        if qt_color.isValid():
            self.value = qt_color.name()
            self.app.refresh()


class TextColor(ColorAction):
    """
    Open color picker and set chosen color to text (in content)
    """
    name = 'color_t'
    value = '#ffffff'
    label = 'Set &text color'


class BackgroundColor(ColorAction):
    """
    Open color picker and set chosen color to background (of content)
    """
    name = 'color_b'
    value = '#272828'
    label = 'Set &background color'


class AuxiliaryBackgroundColor(ColorAction):
    """
    Open color picker and set chosen color to auxiliary background (of content)
    """
    name = 'color_s'
    value = '#373838'
    label = 'Set &auxiliary background color'


# TODO: include in menu
class ActiveBackgroundColor(ColorAction):
    """
    Open color picker and set chosen color to auxiliary background (of content)
    """
    name = 'color_a'
    value = '#443477'
    label = 'Set active color'


class ResetColors(MenuAction):
    """Reset colors"""
    label = '&Reset background and text colors'

    def action(self):
        self.app.config.color_b.reset()
        self.app.config.color_t.reset()
        self.app.refresh()


class About(MenuAction):
    """Show "about" window"""
    label = '&About...'

    def action(self):
        self.app.about()


class EnableInDialogs(Setting, MenuAction):
    """Switch for night mode in dialogs"""
    value = True
    label = 'Enable in &dialogs'
    checkable = True

    def action(self):
        self.value = not self.value


class StyleScrollBars(Setting, MenuAction):
    value = True
    label = 'Dark Scroll Bars'
    checkable = True

    def action(self):
        self.value = not self.value
        self.app.refresh()


class ModeSettings(Setting, MenuAction):
    value = {
        'mode': 'manual',
        'start_at': '21:30',
        'end_at': '07:30'
    }
    window = None
    label = 'Start automatically'
    checkable = True

    @property
    def is_checked(self):
        return self.mode == 'auto'

    @property
    def mode(self):
        return self.value['mode']

    def action(self):
        from aqt import mw as main_window

        if not self.window:
            # self.value is mutable, any modifications done by ColorMapWindow
            # will be done on the value of this singleton class object
            self.window = ModeWindow(
                main_window,
                self.value,
                on_update=self.update
            )
        self.window.show()
        self.app.update_menu()

    def update(self):
        self.app.refresh()

    @property
    def is_active(self):
        current_time = datetime.now().time()
        start = self.time('start_at')
        end = self.time('end_at')
        if end > start:
            return start <= current_time <= end
        else:
            return start <= current_time or current_time <= end

    def time(self, which):
        return datetime.strptime(self.value[which], '%H:%M').time()


class EnableNightMode(Setting, MenuAction):
    """Switch night mode"""
    value = False
    label = '&Enable night mode'
    shortcut = 'Ctrl+n'
    checkable = True

    require = {
        ModeSettings,
        # 'StateSettings' (circular dependency)
    }

    def action(self):
        self.value = not self.value

        if self.mode_settings.mode != 'manual':
            alert(
                'Automatic Night Mode has been disabled. '
                '(You pressed "ctrl+n" or switched a toggle in the menu). '
                'Now you can toggle Night Mode manually '
                'or re-enable the Automatic Night Mode in the menu. '
            )
            self.mode_settings.value['mode'] = 'manual'

        success = self.app.refresh()

        if not success:
            self.value = not self.value

        self.app.config.state_on.update_state()


class StateSetting(Setting):
    """Stores the last state of application.

    The state after start-up is determined programmatically;
    the value set during configuration loading will be ignored.
    """
    name = 'state_on'
    state = None

    require = {
        ModeSettings,
        EnableNightMode
    }

    @property
    def value(self):
        if self.mode_settings.mode == 'manual':
            return self.enable_night_mode.value
        else:
            return self.mode_settings.is_active

    @value.setter
    def value(self, value):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # check the state every 60 seconds
        # (maybe a bit suboptimal, but the most reliable)
        from aqt import mw as main_window
        self.timer = QTimer(main_window)
        self.timer.setInterval(60 * 100)  # 1000 milliseconds
        self.timer.timeout.connect(self.maybe_enable_maybe_disable)

    def on_load(self):
        if self.value:
            self.app.on()

        self.update_state()
        self.timer.start()

    def on_save(self):
        self.timer.stop()

    def maybe_enable_maybe_disable(self):
        if self.value != self.state:
            self.app.refresh()
            self.update_state()

    def update_state(self):
        self.state = self.value


class DisabledStylers(Setting, MenuAction):

    value = set()
    window = None
    label = 'Choose what to style'

    def action(self):
        from aqt import mw as main_window

        if not self.window:
            self.window = StylersSelectorWindow(
                main_window,
                self.value,
                self.app.styles.stylers,
                on_update=self.update
            )
        self.window.show()

    def update(self):
        self.app.refresh(reload=True)
