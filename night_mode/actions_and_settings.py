from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QColorDialog

from .internals import Setting, MenuAction
from .color_map import ColorMapWindow


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


class EnableNightMode(Setting, MenuAction):
    """Switch night mode"""
    value = False
    name = 'state_on'
    label = '&Enable night mode'
    shortcut = 'Ctrl+n'
    checkable = True

    def action(self):
        self.value = not self.value
        success = self.app.refresh()
        if not success:
            self.value = not self.value

    def on_load(self):
        if self.value:
            self.app.on()
