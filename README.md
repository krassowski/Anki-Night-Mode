# Anki-Night-Mode
[![Build Status](https://travis-ci.org/krassowski/Anki-Night-Mode.svg?branch=master)](https://travis-ci.org/krassowski/Anki-Night-Mode) [![Code Climate](https://codeclimate.com/github/krassowski/Anki-Night-Mode/badges/gpa.svg)](https://codeclimate.com/github/krassowski/Anki-Night-Mode)

This plugin adds a functionality of night mode, similar to the one implemented in AnkiDroid app.

### How it works?

It adds a "view" menu entity with options like:
- Automatic (i.e. at specified time) or manual switching of the night mode
- Inverting colors of images or latex formulas
- Defining custom color substitution rules

It provides shortcut <kbd>ctrl</kbd>+<kbd>n</kbd> to quickly switch mode and color picker to adjust some of color parameters.

After enabling the night mode, the add-on changes colors of menubar, toolbar, bottombars and content windows. Take a look at a screenshot at the bottom of this page to see an example.

### Compatibility

The add-on supports Anki in 2.1 version. While there is an older version of the add-on written for Anki 2.0, it is no longer supported as Anki 2.0 uses [well oudated and unsecure](https://github.com/krassowski/Anki-Night-Mode/issues/79#issuecomment-517806633) technology which lead to a large number of [difficult do diagnose issues](https://github.com/krassowski/Anki-Night-Mode/issues?utf8=✓&q=+label%3Aold-version+).

### How can I get it?

#### Automatic install

You can download this add-on from within the Anki app.
From menu select: `Tools >> Add-ons >> Browse && Install...` and type the following code:

```python
1496166067
```

after clicking `ok` the add-on will be downloaded and installed. You neeed to restart Anki to enable changes.

To switch into the night mode you can use <kbd>ctrl</kbd>+<kbd>n</kbd> shortcut, or use one of the new options in the menu: `View >> Night Mode >> ...`.

#### Manual installation

For the most recent updates and additions you may want to install a newer version of this addon manually.
Follow this steps:

1. Get the newest version of `night_mode` directory from GitHub
2. Run Anki, from menu select `Tools >> Add-ons >> Open Add-ons Folder...` to open add-ons directory
4. Copy downloaded directory into the directory opened in the previous step
5. Restart Anki and enjoy the latest features!

#### After installation

Please, leave any feedback on [Anki webpage](https://ankiweb.net/shared/info/1496166067) or let me know of any issues here, on GitHub.

### Preview

![Preview](https://raw.githubusercontent.com/krassowski/Anki-Night-Mode/master/preview.png)


### Tags color in the edit window

The Mac OS users might experience an issue with the tags colors in the edit window. There are couple of workarounds proposed for this, one of which is disabling the edit widow styling and another (proposed [here](https://github.com/krassowski/Anki-Night-Mode/issues/59#issuecomment-517092923)) depends on a new functionality of Mojave system:

- close Anki
- paste the following command in the Terminal:
```bash
defaults write net.ankiweb.dtop NSRequiresAquaSystemAppearance -bool no
```
- restart Anki

The application (including title bar) should be styled dark now and the tags box contrast problem should be resolved. Please let us know if it worked for you [here](https://github.com/krassowski/Anki-Night-Mode/issues/59).


### For developers & translators

Feel free to contribute, send bug reports or feature requests :)

If you can help translate the add-on to your language, please join us [at POEditor](https://poeditor.com/join/project/0waBVUY8oC).


#### Custom CSS in night mode

You may use `night_mode` class, to overwrite some of the CSS rules; sometimes usage of `important!` directive or catch-all selector (`*`) will be needed to enforce you own styling. Examples:

#### Change color of every piece of text:

```css
.night_mode * {
    color: red;
}
```

#### Change card background

```css
.night_mode.card {
    background: red !important;
}
```

#### Specifically replace a background of an element

given the HTML of your card:

```html
<div>Normal text <span style="background-color: rgb(240, 244, 198);">highlighted text</span></div>
```

```css
.night_mode span[style="background-color: rgb(240, 244, 198);"] {
    background-color: red!important;
}
```

#### Change the color of a cloze

```css
.night_mode .cloze {
    color: red!important;
}
```

### Add-ons compatibility

Add-ons which are known to work well with the night mode:
- [Anki-TouchScreen](https://github.com/krassowski/Anki-TouchScreen)
- [Anki-Zoom](https://github.com/krassowski/Anki-Zoom)

If you add-on works well Night Mode, please feel free to add your add-on on to the list above by editing this file (proposing a change)!
