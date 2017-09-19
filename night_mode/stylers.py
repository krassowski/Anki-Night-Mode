from PyQt5 import QtCore

import aqt
from aqt import mw, editor
from aqt.addcards import AddCards
from aqt.browser import Browser
from aqt.editcurrent import EditCurrent
from aqt.editor import Editor
from .config import ConfigValueGetter
from .internals import percent_escaped, move_args_to_kwargs
from .internals import style_tag, wraps, appends_in_night_mode, replaces_in_night_mode, css
from .styles import SharedStyles, ButtonsStyle, ImageStyle, DeckStyle, LatexStyle, DialogStyle

try:
    from_utf8 = QtCore.QString.fromUtf8
except AttributeError:
    from_utf8 = lambda s: s

from .internals import SnakeNameMixin, StylerMetaclass, abstract_property
from .styles import StyleRequiringMixin


class Styler(StyleRequiringMixin, SnakeNameMixin, metaclass=StylerMetaclass):

    def __init__(self, app):
        StyleRequiringMixin.__init__(self, app)
        self.app = app
        self.config = ConfigValueGetter(app.config)
        self.replacements = {}
        self.original_attributes = {}

    @abstract_property
    def target(self):
        return None

    def get_or_create_original(self, key):
        if key not in self.original_attributes:
            original = getattr(self.target, key)
            self.original_attributes[key] = original
        else:
            original = self.original_attributes[key]

        return original

    def replace_attributes(self):
        try:
            for key, addition in self.additions.items():
                original = self.get_or_create_original(key)
                setattr(self.target, key, original + addition.value(self))

            for key, replacement in self.replacements.items():
                self.get_or_create_original(key)
                setattr(self.target, key, replacement)
        except (AttributeError, TypeError):
            print('Failed to inject style to:', self.target, key, self.name)
            raise

    def restore_attributes(self):
        for key, original in self.original_attributes.items():
            setattr(self.target, key, original)


class ToolbarStyler(Styler):

    target = mw.toolbar
    require = {
        SharedStyles
    }

    @appends_in_night_mode
    @style_tag
    @percent_escaped
    def _body(self):
        return self.shared.top


class StyleSetter:

    def __init__(self, target):
        self.target = target

    @property
    def css(self):
        return self.target.styleSheet()

    @css.setter
    def css(self, value):
        self.target.setStyleSheet(value)


class MenuStyler(Styler):
    target = StyleSetter(mw)

    @appends_in_night_mode
    def css(self):
        return self.shared.menu


class ReviewerStyler(Styler):

    target = mw.reviewer
    require = {
        SharedStyles,
        ButtonsStyle,
        LatexStyle,
        ImageStyle
    }

    @wraps(position='around')
    def _bottomHTML(self, reviewer, _old):
        if self.config.state_on:
            return _old(reviewer) + style_tag(percent_escaped(self.bottom_css))
        else:
            return _old(reviewer)

    @property
    def bottom_css(self):
        return self.buttons.html + self.shared.colors_replacer + """
        body, #outer
        {
            background:-webkit-gradient(linear, left top, left bottom, from(#333), to(#222));
            border-top-color:#222
        }
        .stattxt
        {
            color:#ccc
        }
        /* Make the color above "Again" "Hard" "Easy" and so on buttons readable */
        .nobold
        {
            color:#ddd
        }
        """

    # TODO: it can be implemented with a nice decorator
    @wraps(position='around')
    def revHtml(self, reviewer, _old):
        if self.config.state_on:
            return _old(reviewer) + style_tag(percent_escaped(self.body))
        else:
            return _old(reviewer)

    @css
    def body(self):
        # Invert images and latex if needed

        css_body = """
        .card input
        {
            background-color:black!important;
            border-color:#444!important;
            color:#eee!important
        }
        .typeGood
        {
            color:black;
            background:#57a957
        }
        .typeBad
        {
            color:black;
            background:#c43c35
        }
        .typeMissed
        {
            color:black;
            background:#ccc
        }
        #answer
        {
            height:0;
            border:0;
            border-bottom: 2px solid #333;
            border-top: 2px solid black
        }
        img#star
        {
            -webkit-filter:invert(0%)!important
        }
        .cloze
        {
            color:#5566ee!important
        }
        a
        {
            color:#0099CC
        }
        """

        card_color = """
        .card{
            color:""" + self.config.color_t + """!important;
            background-color:" + color_b + "!important
        }
        """

        css = css_body + card_color + self.shared.user_color_map + self.shared.body_colors

        if self.config.invert_image:
            css += self.image.invert
        if self.config.invert_latex:
            css += self.latex.invert

        return css


class DeckBrowserStyler(Styler):

    target = mw.deckBrowser
    require = {
        SharedStyles,
        DeckStyle
    }

    @appends_in_night_mode
    @style_tag
    @percent_escaped
    def _body(self):
        return self.deck.style + self.shared.body_colors


class DeckBrowserBottomStyler(Styler):

    target = mw.deckBrowser.bottom
    require = {
        DeckStyle
    }

    @appends_in_night_mode
    @style_tag
    @percent_escaped
    def _centerBody(self):
        return self.deck.bottom


class OverviewStyler(Styler):

    target = mw.overview
    require = {
        SharedStyles,
        ButtonsStyle
    }

    @appends_in_night_mode
    @style_tag
    @percent_escaped
    def _body(self):
        return self.css

    @css
    def css(self):
        return f"""
        {self.buttons.html}
        {self.shared.colors_replacer}
        {self.shared.body_colors}
        .descfont
        {{
            color: {self.config.color_t}
        }}
        """


class OverviewBottomStyler(Styler):

    target = mw.overview.bottom
    require = {
        DeckStyle
    }

    @appends_in_night_mode
    @style_tag
    @percent_escaped
    def _centerBody(self):
        return self.deck.bottom


class AnkiWebViewStyler(Styler):

    target = mw.web
    require = {
        SharedStyles,
        ButtonsStyle
    }

    @wraps(position='around')
    def stdHtml(self, web, *args, **kwargs):
        old = kwargs.pop('_old')

        args, kwargs = move_args_to_kwargs(old, [web] + list(args), kwargs)

        if self.config.state_on:
            kwargs['head'] = kwargs.get('head', '') + style_tag(self.waiting_screen)

        return old(web, *args[1:], **kwargs)

    @css
    def waiting_screen(self):
        return self.buttons.html + self.shared.body_colors


class BrowserPackageStyler(Styler):

    target = aqt.browser

    @replaces_in_night_mode
    def COLOUR_MARKED(self):
        return '#735083'

    @replaces_in_night_mode
    def COLOUR_SUSPENDED(self):
        return '#777750'


class BrowserStyler(Styler):

    target = Browser
    require = {
        SharedStyles,
        ButtonsStyle,
    }

    @wraps
    def init(self, browser, mw):

        if self.config.state_on and self.config.enable_in_dialogs:

            basic_css = browser.styleSheet()
            global_style = '#' + browser.form.centralwidget.objectName() + '{' + self.shared.colors + '}'
            browser.setStyleSheet(self.shared.menu + self.style + basic_css + global_style)

            browser.form.tableView.setStyleSheet(self.table)
            browser.form.tableView.horizontalHeader().setStyleSheet(self.table_header)

            browser.form.searchEdit.setStyleSheet(self.search_box)
            browser.form.searchButton.setStyleSheet(self.buttons.qt)
            browser.form.previewButton.setStyleSheet(self.buttons.qt)

    # TODO: test this
    #@wraps
    def _renderPreview(self, browser, cardChanged=False):
        if browser._previewWindow:
            self.app.take_care_of_night_class(web_object=browser._previewWeb)

    @wraps(position='around')
    def _cardInfoData(self, browser, _old):

        rep, cs = _old(browser)

        if self.config.state_on and self.config.enable_in_dialogs:
            rep += style_tag("""
                *
                {
                    """ + self.shared.colors + """
                }
                div
                {
                    border-color:#fff!important
                }
                """ + self.shared.colors_replacer + """
                """)
        return rep, cs

    @css
    def style(self):
        return """
        QSplitter::handle
        {
            background:#000
        }
        #""" + from_utf8("widget") + """, QTreeView
        {
            """ + self.shared.colors + """
        }
        QTreeView::item:selected:active, QTreeView::branch:selected:active
        {
            background:""" + self.config.color_a + """
        }
        QTreeView::item:selected:!active, QTreeView::branch:selected:!active
        {
            background:""" + self.config.color_a + """
        }
        """

    @css
    def table(self):
        return f"""
            QTableView
            {{
                alternate-background-color: {self.config.color_s};
                gridline-color: {self.config.color_s};
                {self.shared.colors}
                selection-background-color: {self.config.color_a}
            }}
            """

    @css
    def table_header(self):
        return """
            QHeaderView, QHeaderView::section
            {
                """ + self.shared.colors + """
                border:1px solid """ + self.config.color_s + """
            }
            """

    @css
    def search_box(self):
        return """
        QComboBox
        {
            border:1px solid """ + self.config.color_s + """;
            border-radius:3px;
            padding:0px 4px;
            """ + self.shared.colors + """
        }

        QComboBox:!editable
        {
            background:""" + self.config.color_a + """
        }

        QComboBox QAbstractItemView
        {
            border:1px solid #111;
            """ + self.shared.colors + """
            background:#444
        }

        QComboBox::drop-down, QComboBox::drop-down:editable
        {
            """ + self.shared.colors + """
            width:24px;
            border-left:1px solid #444;
            border-top-right-radius:3px;
            border-bottom-right-radius:3px;
            background:qlineargradient(x1: 0.0, y1: 0.0, x2: 0.0, y2: 1.0, radius: 1, stop: 0.03 #3D4850, stop: 0.04 #313d45, stop: 1 #232B30);
        }

        QComboBox::down-arrow
        {
            top:1px;
            image: url('""" + self.app.icons.arrow + """')
        }
        """


class AddCardsStyler(Styler):

    target = AddCards
    require = {
        SharedStyles,
        ButtonsStyle,
    }

    @wraps
    def init(self, add_cards, mw):
        if self.config.state_on and self.config.enable_in_dialogs:

            # style add/history button
            add_cards.form.buttonBox.setStyleSheet(self.buttons.qt)

            self.set_style_to_objects_inside(add_cards.form.horizontalLayout, self.buttons.qt)

            # style the single line which has some bright color
            add_cards.form.line.setStyleSheet('#' + from_utf8('line') + '{border: 0px solid #333}')

            add_cards.form.fieldsArea.setAutoFillBackground(False)

    @staticmethod
    def set_style_to_objects_inside(layout, style):
        for i in range(layout .count()):
            layout.itemAt(i).widget().setStyleSheet(style)


class EditCurrentStyler(Styler):

    target = EditCurrent
    require = {
        ButtonsStyle,
    }

    @wraps
    def init(self, edit_current, mw):
        if self.config.state_on and self.config.enable_in_dialogs:
            # style close button
            edit_current.form.buttonBox.setStyleSheet(self.buttons.qt)


class EditorStyler(Styler):

    target = Editor

    require = {
        SharedStyles,
        DialogStyle,
        ButtonsStyle
    }

    # TODO: this would make more sense if we add some styling to .editor-btn
    def _addButton(self, editor, icon, command, *args, **kwargs):
        original_function = kwargs.pop('_old')
        button = original_function(editor, icon, command, *args, **kwargs)
        return button.replace('<button>', '<button class="editor-btn">')

    @wraps
    def init(self, editor, mw, widget, parentWindow, addMode=False):

        if self.config.state_on and self.config.enable_in_dialogs:

            editor_css = self.dialog.style + self.buttons.qt

            editor_css += '#' + widget.objectName() + '{' + self.shared.colors + '}'

            editor.parentWindow.setStyleSheet(editor_css)

            editor.tags.completer.popup().setStyleSheet(self.completer)

            widget.setStyleSheet(
                self.qt_mid_buttons +
                self.buttons.advanced_qt(restrict_to='#' + self.encode_class_name('fields')) +
                self.buttons.advanced_qt(restrict_to='#' + self.encode_class_name('layout'))
            )

    @staticmethod
    def encode_class_name(string):
        return "ID"+"".join(map(str, map(ord, string)))

    @css
    def completer(self):
        return """
            background-color:black;
            border-color:#444;
            color:#eee;
        """

    @css
    def qt_mid_buttons(self):
        return f"""
        QLineEdit
        {{
            {self.completer}
        }}
        """


class EditorWebViewStyler(Styler):

    target = editor
    require = {
        ButtonsStyle,
        ImageStyle,
        LatexStyle
    }

    # TODO: currently restart is required for this to take effect after configuration change
    @appends_in_night_mode
    @style_tag
    @percent_escaped
    def _html(self):
        if self.config.enable_in_dialogs:

            custom_css = f"""
            #topbuts {self.buttons.html}
            #topbutsright button
            {{
                padding: inherit;
                margin-left: 1px
            }}
            #topbuts img
            {{
                filter: invert(1);
                -webkit-filter: invert(1)
            }}
            a
            {{
                color: 00BBFF
            }}
            html, body, #topbuts, .field, .fname
            {{
                color: {self.config.color_t}!important;
                background: {self.config.color_b}!important
            }}
            """

            if self.config.invert_image:
                custom_css += ".field " + self.image.invert
            if self.config.invert_latex:
                custom_css += ".field " + self.latex.invert

            return custom_css
        return ''
