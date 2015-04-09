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
"""

__addon_name__ = "Night Mode"
__version__ = "1.0.2"

from aqt import mw

from anki.lang import _
from anki.hooks import addHook

from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QAction, QKeySequence, QMenu, \
						QColorDialog, QMessageBox, QColor


# This declarations are there only to be sure that in case of troubles
# with "profileLoaded" hook everything will work.

nm_state_on = False
nm_invert_image = False
nm_invert_latex = False

nm_color_b = "#272828"
nm_color_t = "#ffffff"


# Save orginal values for further use.
nm_default_css_menu = mw.styleSheet()

nm_default_css_top = mw.toolbar._css
nm_default_css_body = mw.reviewer._css
nm_default_css_bottom = mw.reviewer._bottomCSS

nm_default_css_decks = mw.deckBrowser._css
nm_default_css_decks_bottom = mw.deckBrowser.bottom._css

nm_default_css_overview = mw.overview._css
nm_default_css_overview_bottom = mw.overview.bottom._css
# sharedCSS is only used for "Waiting for editing to finish." screen.
nm_default_css_waiting_screen = mw.sharedCSS


def nm_iimage():
	"""
	Toggles image inversion.
	To learn how images are inverted check also nm_append_to_styles().
	"""
	global nm_invert_image
	nm_invert_image = not nm_invert_image
	nm_refresh()


def nm_ilatex():
	"""
	Toggles latex inversion.
	Latex formulas are nothing more than images with class "latex".
	To learn how formulas are inverted check also nm_append_to_styles().
	"""
	global nm_invert_latex
	nm_invert_latex = not nm_invert_latex
	nm_refresh()


def nm_color_t():
	"""
	Open color picker and set chosen color to text (in content)
	"""
	global nm_color_t
	nm_qcolor_old = QColor(nm_color_t)
	nm_qcolor = QColorDialog.getColor(nm_qcolor_old)
	if nm_qcolor.isValid():
		nm_color_t = nm_qcolor.name()
		nm_refresh()


def nm_color_b():
	"""
	Open color picker and set chosen color to background (of content)
	"""
	global nm_color_b
	nm_qcolor_old = QColor(nm_color_b)
	nm_qcolor = QColorDialog.getColor(nm_qcolor_old)
	if nm_qcolor.isValid():
		nm_color_b = nm_qcolor.name()
		nm_refresh()


def nm_color_reset():
	"""
	Reset colors.
	"""
	global nm_color_b, nm_color_t
	nm_color_b = "#272828"
	nm_color_t = "#ffffff"
	nm_refresh()


def nm_about():
	"""
	Show "about" window.
	"""
	nm_about_box = QMessageBox()
	nm_about_box.setText(__addon_name__ + " " + __version__ + __doc__)
	nm_about_box.setGeometry(300, 300, 250, 150)
	nm_about_box.setWindowTitle("About " + __addon_name__ + " " + __version__)
	nm_about_box.exec_()


def nm_save():
	"""
	Saves configurable variables into profile, so they can
	be used to restore previous state after Anki restart.
	"""
	mw.pm.profile['nm_state_on'] = nm_state_on
	mw.pm.profile['nm_invert_image'] = nm_invert_image
	mw.pm.profile['nm_invert_latex'] = nm_invert_latex
	mw.pm.profile['nm_color_b'] = nm_color_b
	mw.pm.profile['nm_color_t'] = nm_color_t


def nm_load():
	"""
	Load configuration from profile, set states of checkable menu objects
	and turn on night mode if it were enabled on previous session.
	"""
	global nm_menu_iimage, nm_menu_ilatex, nm_state_on, \
		nm_invert_image, nm_invert_latex, nm_color_b, nm_color_t

	try:
		nm_state_on = mw.pm.profile['nm_state_on']
		nm_invert_image = mw.pm.profile['nm_invert_image']
		nm_invert_latex = mw.pm.profile['nm_invert_latex']
		nm_color_b = mw.pm.profile['nm_color_b']
		nm_color_t = mw.pm.profile['nm_color_t']
	except KeyError:
		nm_state_on = False
		nm_invert_image = False
		nm_invert_latex = False
		nm_color_b = "#272828"
		nm_color_t = "#ffffff"

	if nm_state_on:
		nm_on()

	if nm_invert_image:
		nm_menu_iimage.setChecked(True)

	if nm_invert_latex:
		nm_menu_ilatex.setChecked(True)


def nm_onload():
	"""
	Add hooks and initialize menu.
	Call to this function is placed on the end of this file.
	"""
	addHook("unloadProfile", nm_save)
	addHook("profileLoaded", nm_load)

	nm_setup_menu()


def nm_append_to_styles(bottom='', body='', top='', decks='',
						other_bottoms='', overview='', menu='',
						waiting_screen=''):
	"""
	This function changes CSS style of most objects. In basic use,
	it only reloads original styles and refreshes interface.

	All arguments are expected to be strings with CSS styles.
	"""
	# Invert images and latex if needed
	if nm_invert_image:
		body += nm_css_iimage
	if nm_invert_latex:
		body += nm_css_ilatex

	# Apply styles to Python objects or by Qt functions.

	mw.setStyleSheet(nm_default_css_menu + menu)
	mw.toolbar._css = nm_default_css_top + top
	mw.reviewer._bottomCSS = nm_default_css_bottom + bottom
	mw.reviewer._css = nm_default_css_body + body
	mw.deckBrowser._css = nm_default_css_decks + decks
	mw.deckBrowser.bottom._css = nm_default_css_decks_bottom + other_bottoms
	mw.overview._css = nm_default_css_overview + overview
	mw.overview.bottom._css = nm_default_css_overview_bottom + other_bottoms
	mw.sharedCSS = nm_default_css_waiting_screen + waiting_screen

	# Reload current screen.
	if mw.state == "review":
		mw.reviewer._initWeb()
	if mw.state == "deckBrowser":
		mw.deckBrowser.refresh()
	if mw.state == "overview":
		mw.overview.refresh()

	# Redraw toolbar (should be always visible).
	mw.toolbar.draw()


def nm_on():
	"""
	Turn on night mode.
	"""
	global nm_state_on
	nm_state_on = True
	nm_append_to_styles(nm_css_bottom,
						nm_css_body + nm_card_color_css(),
						nm_css_top,
						nm_css_decks + nm_body_color_css(),
						nm_css_other_bottoms,
						nm_css_overview + nm_body_color_css(),
						nm_css_menu,
						nm_css_buttons + nm_body_color_css())
	nm_menu_switch.setChecked(True)


def nm_off():
	"""
	Turn off night mode.
	"""
	global nm_state_on
	nm_state_on = False
	nm_append_to_styles()
	nm_menu_switch.setChecked(False)


def nm_switch():
	"""
	Switch night mode.
	"""
	if nm_state_on:
		nm_off()
	else:
		nm_on()


def nm_refresh():
	"""
	Refresh display by reenabling night or normal mode.
	"""
	if nm_state_on:
		nm_on()
	else:
		nm_off()


def nm_setup_menu():
	"""
	Initialize menu. If there is an entity "View" in top level menu
	(shared with other plugins, like "Zoom" of R. Sieker) options of
	Night Mode will be putted there. In other case it creates that menu.
	"""
	global nm_menu_switch, nm_menu_iimage, nm_menu_ilatex

	try:
		mw.addon_view_menu
	except AttributeError:
		mw.addon_view_menu = QMenu(_(u"&View"), mw)
		mw.form.menubar.insertMenu(mw.form.menuTools.menuAction(),
									mw.addon_view_menu)

	mw.nm_menu = QMenu(_('&Night Mode'), mw)

	mw.addon_view_menu.addMenu(mw.nm_menu)

	nm_menu_switch = QAction(_('&Enable night mode'), mw, checkable=True)
	nm_menu_iimage = QAction(_('&Invert images'), mw, checkable=True)
	nm_menu_ilatex = QAction(_('Invert &latex'), mw, checkable=True)
	nm_menu_color_b = QAction(_('Set &background color'), mw)
	nm_menu_color_t = QAction(_('Set &text color'), mw)
	nm_menu_color_r = QAction(_('&Reset colors'), mw)
	nm_menu_about = QAction(_('&About...'), mw)

	mw_toggle_seq = QKeySequence("Ctrl+n")
	nm_menu_switch.setShortcut(mw_toggle_seq)

	mw.nm_menu.addAction(nm_menu_switch)
	mw.nm_menu.addSeparator()
	mw.nm_menu.addAction(nm_menu_iimage)
	mw.nm_menu.addAction(nm_menu_ilatex)
	mw.nm_menu.addSeparator()
	mw.nm_menu.addAction(nm_menu_color_b)
	mw.nm_menu.addAction(nm_menu_color_t)
	mw.nm_menu.addAction(nm_menu_color_r)
	mw.nm_menu.addSeparator()
	mw.nm_menu.addAction(nm_menu_about)

	s = SIGNAL("triggered()")
	mw.connect(nm_menu_switch, s, nm_switch)
	mw.connect(nm_menu_iimage, s, nm_iimage)
	mw.connect(nm_menu_ilatex, s, nm_ilatex)
	mw.connect(nm_menu_color_b, s, nm_color_b)
	mw.connect(nm_menu_color_t, s, nm_color_t)
	mw.connect(nm_menu_color_r, s, nm_color_reset)
	mw.connect(nm_menu_about, s, nm_about)


def nm_card_color_css():
	"""
	Generate and return CSS style of class "card",
	using global color declarations
	"""
	return (".card {	color:" + nm_color_t + "!important;" +
			"background-color:" + nm_color_b + "!important}")


def nm_body_color_css():
	"""
	Generate and return CSS style of class "card",
	using global color declarations
	"""
	return (" body {	color:" + nm_color_t + "!important;" +
			"background-color:" + nm_color_b + "!important}")

#
# GLOBAL CSS STYLES SECTION
#

# Thanks to http://devgrow.com/dark-button-navigation-using-css3/
nm_css_buttons = """
button
{
    color: #AFB9C1;
    text-shadow: 1px 1px #1f272b;
	margin-top: 0;
	position:relative;
	top: 0;
	outline: 0;
    padding: 3px 8px;
    display: inline-block;
    border: 1px solid #3E474D;
    border-top-color: #1c252b;
    border-left-color: #2d363c;
    background: -webkit-gradient(linear, left top, left bottom, color-stop(3%,#3D4850), color-stop(4%,#313d45), color-stop(100%,#232B30));
    -webkit-box-shadow: 1px 1px 1px rgba(0,0,0,0.1);
    -webkit-border-radius: 3px;
}
button:hover
{
    color: #fff;
    background: -webkit-gradient(linear, left top, left bottom, color-stop(3%,#4C5A64), color-stop(4%,#404F5A), color-stop(100%,#2E3940));
}
button:active
{
    color: #fff;
    background: -webkit-gradient(linear, left top, left bottom, color-stop(3%,#20282D), color-stop(51%,#252E34), color-stop(100%,#222A30));
    -webkit-box-shadow: 1px 1px 1px rgba(255,255,255,0.1);
}
"""

nm_css_color_replacer = """
font[color="#007700"]
{
	color:#00CC00
}
font[color="#000099"]
{
	color:#00BBFF
}
font[color="#C35617"]
{
	color:#D46728
}
font[color="#00a"]
{
	color:#00BBFF
}
"""

nm_css_bottom =  nm_css_buttons + nm_css_color_replacer + """
body
{
	background: -webkit-gradient(linear, left top, left bottom, from(#333), to(#222));
	border-top-color: #000;
}
button
{
	min-width: 70px;
}
.hitem
{
	margin-top: -20px;
}
.stat
{
	padding-top: 0;
}
.stat2
{
	padding-top: 0;
}
.stattxt
{
	height: 6px;
	display:block;
}
.stattxt
{
	color:#ccc
}
.nobold
{
	display: block;
	padding-top: 0;
	height: 7px;
	color:#ddd
}
.spacer
{
	position:relative;
	top:-8px;
}
.spacer2
{
	position:relative;
	top:-8px;
}
button
{
	top:-6px
}
button:active
{
	top:-7px
}
"""

nm_css_top = """
html
{
	background: -webkit-gradient(linear, left top, left bottom, from(#333), to(#444));
	color:#eee;
}
body
{
	border-bottom-color:#111;
}
.hitem
{
	color: #ddd;
}
"""

nm_css_ilatex = """
.latex
{
	-webkit-filter: invert(100%);
}
"""

nm_css_iimage = """
img
{
	-webkit-filter: invert(100%);
}
"""


nm_css_body = """
.card input
{
	background-color:black!important;
	border-color:#444!important;
	color:#eee!important;
}
.typeGood
{
	color:black;
	background:#57a957;
}
.typeBad
{
	color:black;
	background:#c43c35;
}
.typeMissed
{
	color:black;
	background:#ccc;
}
#answer
{
	height: 0;
	border: 0;
	border-bottom: 2px solid #333;
	border-top: 2px solid black;
}
img#star
{
	-webkit-filter: invert(0%)!important;
}
.cloze
{
	color: #5566ee!important;
}
"""

nm_css_decks = nm_css_buttons +  nm_css_color_replacer + """
.current
{
	background-color: rgba(0,0,0,0.5);
}
a.deck
{
	color: #efe
}
tr.deck td
{
	height:35px;
	border-bottom-color:#333
}
tr.deck button img
{
	-webkit-filter: invert(20%);
}
tr.deck font[color="#007700"]
{
	color:#00CC00
}
tr.deck font[color="#000099"]
{
	color:#00BBFF
}
"""

nm_css_other_bottoms = nm_css_buttons + """
#header
{
	color:#ccc!important;
	background: -webkit-gradient(linear, left top, left bottom, from(#333), to(#222));
	border-top-color: #000;
	height:40px;
}
"""

nm_css_overview = nm_css_buttons + nm_css_color_replacer

nm_css_menu = """
QMenuBar,QMenu
{
    background-color: #444;
    color: #eee;
}
QMenuBar::item
{
    background-color: transparent;
}
QMenuBar::item:selected
{
    background-color: rgb(30,30,30)!important;
	border-top-left-radius: 6px;
	border-top-right-radius: 6px;
}
QMenu
{
    border: 1px solid #111;
}
QMenu::item::selected
{
    background-color: rgb(30,30,30);
}
QMenu::item
{
     padding: 3px 25px 3px 25px;
     border: 1px solid transparent;
}
"""


#
# ONLOAD SECTION
#

nm_onload()
