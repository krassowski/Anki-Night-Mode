from .config import ConfigValueGetter
from .internals import css, snake_case, SingletonMetaclass, RequiringMixin


class Style(RequiringMixin, metaclass=SingletonMetaclass):

    @property
    def name(self):
        return snake_case(self.__class__.__name__).split('_')[0]

    def __init__(self, app):
        RequiringMixin.__init__(self, app)
        self.app = app
        self.config = ConfigValueGetter(app.config)


class SharedStyles(Style):

    def __init__(self, app):
        super().__init__(app)
        self.build_styles()

    def refresh(self):
        self.build_styles()

    def build_styles(self):
        # TODO
        pass

    @css
    def top(self):
        return """
        html, #header
        {
            background:-webkit-gradient(linear, left top, left bottom, from(#333), to(#444));
            color:#eee
        }
        body, #header
        {
            border-bottom-color:#222
        }
        .hitem
        {
            color:#ddd
        }
        """

    @css
    def menu(self):
        return """
        QMenuBar,QMenu
        {
            background-color:#444!important;
            color:#eee!important
        }
        QMenuBar::item
        {
            background-color:transparent
        }
        QMenuBar::item:selected
        {
            background-color:""" + self.config.color_a + """!important;
            border-top-left-radius:6px;
            border-top-right-radius:6px
        }
        QMenu
        {
            border:1px solid #111
        }
        QMenu::item::selected
        {
            background-color:""" + self.config.color_a + """;
        }
        QMenu::item
        {
            padding:3px 25px 3px 25px;
            border:1px solid transparent
        }
        """

    @css
    def colors(self):
        return f'color: {self.config.color_t}; background-color: {self.config.color_b};'

    @css
    def colors_replacer(self):
        return """
        font[color="#007700"],span[style="color:#070"]
        {
            color:#00CC00!important
        }
        font[color="#000099"],span[style="color:#00F"]
        {
            color:#00BBFF!important
        }
        font[color="#C35617"],span[style="color:#c00"]
        {
            color:#D46728!important
        }
        font[color="#00a"]
        {
            color:#00BBFF
        }
        """

    @css
    def body_colors(self):
        """Generate and return CSS style of class "card"."""
        return (" body {    color:" + self.config.color_t + "!important;" +
                "background-color:" + self.config.color_b + "!important}")

    @css
    def user_color_map(self):
        style = ''
        for old, new in self.config.user_color_map.items():
            if old and new:
                style += f'font[color="{old}"]{{color: {new}!important}}'
        return style


class ButtonsStyle(Style):

    # Styling inspired by devgrow.com/dark-button-navigation-using-css3/ (thanks!)
    idle = """
        color:#AFB9C1;
        margin-top:0;
        position:relative;
        top:0;
        padding:3px 8px;
        border:1px solid #3E474D;
        border-top-color:#1c252b;
        border-left-color:#2d363c;
    """

    hover = 'color: #fff;'
    active = 'color: #fff;'

    @css
    def qt(self):
        return self.advanced_qt() + (self.qt_scrollbars if self.config.style_scroll_bars else '')

    def advanced_qt(self, restrict_to_parent='', restrict_to=''):
        return """
        """ + restrict_to_parent + """ QPushButton""" + restrict_to + """
        {
            background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #3D4850, stop: 0.04 #313d45, stop: 1 #232B30);
            border-radius: 3px;
            """ + self.idle + """
        }
        """ + restrict_to_parent + """ QPushButton""" + restrict_to + """:hover
        {
            """ + self.hover + """
            background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #4C5A64, stop: 0.04 #404F5A, stop: 1 #2E3940);
        }
        """ + restrict_to_parent + """ QPushButton""" + restrict_to + """:pressed
        {
            """ + self.active + """
            background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #20282D, stop: 0.51 #252E34, stop: 1 #222A30);
        }
        """ + restrict_to_parent + """ QPushButton""" + restrict_to + """:disabled
        {
            """ + self.active + """
            background: qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #20282D, stop: 0.51 #252E34, stop: 1 #222A30);
        }
        """ + restrict_to_parent + """ QPushButton""" + restrict_to + """:focus
        {
            outline: 1px dotted #4a90d9
        }
        """

    scrollbar_size = 15
    scrollbar_background = '#313d45'
    scrollbar_color = '#515d71'

    @css
    def qt_scrollbars(self):
        return f"""
        QScrollBar:horizontal, QScrollBar:vertical {{
            background: {self.scrollbar_background};
        }}
        QScrollBar:add-page, QScrollBar:sub-page{{
            background: {self.scrollbar_background};
        }}
        QScrollBar::handle:horizontal, QScrollBar::handle:vertical {{
            background: {self.scrollbar_color};
        }}
        QScrollBar {{
            margin: 0
        }}
        QScrollBar:vertical {{
            width: {self.scrollbar_size}px;
        }}
        QScrollBar:horizontal {{
            height: {self.scrollbar_size}px;
        }}
        QScrollBar::handle {{
            margin: 4px;
            border-radius: 3px
        }}
        QScrollBar::handle:vertical {{
            min-height: 20px;
        }}
        QScrollBar::handle:horizontal {{
            min-width: 20px;
        }}
        QScrollBar::add-line, QScrollBar::sub-line {{
            border: none;
            background: none;
        }}
        QScrollBar:left-arrow, QScrollBar::right-arrow, QScrollBar:up-arrow, QScrollBar::down-arrow {{
            border: none;
            background: none;
            color: none
        }}
        """

    @css
    def scrollbars(self):
        return f"""
        ::-webkit-scrollbar{{
            width: {self.scrollbar_size - 8}px;
        }}
        ::-webkit-scrollbar:horizontal {{
            height: {self.scrollbar_size - 8}px;
        }}
        ::-webkit-scrollbar-track {{
            background: {self.scrollbar_background};
        }}
        ::-webkit-scrollbar-thumb {{
            background: {self.scrollbar_color};
            border-radius: 4px;
        }}
        """

    @css
    def html(self):
        return f"""
        button
        {{
            { self.idle }
            text-shadow:1px 1px #1f272b;
            display: inline-block;
            background: #313d45;
            background: gradient(linear, left top, left bottom, color-stop(3%,#3D4850), color-stop(4%,#313d45), color-stop(100%,#232B30));
            box-shadow: 1px 1px 1px rgba(0,0,0,0.1);
            border-radius: 3px
        }}
        button:hover
        {{
            { self.hover }
            background: #404F5A);
            background: gradient(linear, left top, left bottom, color-stop(3%,#4C5A64), color-stop(4%,#404F5A), color-stop(100%,#2E3940));
        }}
        button:active
        {{
            { self.active }
            background: #252E34;
            background: gradient(linear, left top, left bottom, color-stop(3%,#20282D), color-stop(51%,#252E34), color-stop(100%,#222A30));
            box-shadow: 1px 1px 1px rgba(255,255,255,0.1);
        }}
        """ + (self.scrollbars if self.config.style_scroll_bars else '')


class DeckStyle(Style):
    require = {
        SharedStyles,
        ButtonsStyle
    }

    @css
    def bottom(self):
        return self.buttons.html + """
        #header
        {
            color:#ccc!important;
            background:-webkit-gradient(linear, left top, left bottom, from(#333), to(#222));
            border-top-color:#000;
            height:40px
        }
        """

    @css
    def style(self):
        return self.buttons.html + self.shared.colors_replacer + """
        a
        {
            color:#0099CC
        }
        .current
        {
            background-color:rgba(0,0,0,0.5)
        }
        a.deck, .collapse
        {
            color:#efe
        }
        tr.deck td
        {
            height:35px;
            border-bottom-color:#333
        }
        tr.deck font[color="#007700"]
        {
            color:#00CC00
        }
        tr.deck font[color="#000099"]
        {
            color:#00BBFF
        }
        .filtered
        {
            color:#00AAEE!important
        }
        .gears
        {
            filter: invert(1)
        }
        """


class MessageBoxStyle(Style):

    require = {
        ButtonsStyle
    }

    @css
    def style(self):
        """
        Generate and return CSS style of class QMessageBox,
        using global color declarations
        """
        return f"""
        QMessageBox,QLabel
        {{
            color: { self.config.color_t };
            background-color: { self.config.color_b }
        }}
        { self.buttons.qt }
        QPushButton
        {{
            min-width: 70px
        }}
        """


class ImageStyle(Style):

    @css
    def invert(self):
        return """
        img
        {
            filter:invert(1);
            -webkit-filter:invert(1)
        }
        """


class LatexStyle(Style):

    @css
    def invert(self):
        return """
        .latex
        {
            filter:invert(1);
            -webkit-filter:invert(1)
        }
        """


class DialogStyle(Style):

    require = {
        SharedStyles,
        ButtonsStyle
    }

    @css
    def style(self):
        return """
            QDialog,QLabel,QListWidget,QFontComboBox,QCheckBox,QSpinBox,QRadioButton,QHBoxLayout
            {
            """ + self.shared.colors + """
            }
            QFontComboBox::drop-down{border: 0px; border-left: 1px solid #555; width: 30px;}
            QFontComboBox::down-arrow{width:12px; height:8px;
                top:1px;
                image:url('""" + self.app.icons.arrow + """')
            }
            QFontComboBox, QSpinBox{border: 1px solid #555}

            QTabWidget QWidget
            {
                color:""" + self.config.color_t + """;
                background-color:#222;
                border-color:#555
            }
            QTabWidget QLabel {
                position:relative
            }
            QTabWidget QTabBar
            {
                color:#000
            }
            QTabWidget QTextEdit
            {
                border-color:#555
            }
            QTabWidget QGroupBox::title
            {
                subcontrol-origin: margin;
                subcontrol-position:top left;
                margin-top:-7px
            }
            """ + self.buttons.advanced_qt("QTabWidget")
