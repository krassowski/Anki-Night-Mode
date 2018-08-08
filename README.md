# Anki-Night-Mode
[![Build Status](https://travis-ci.org/krassowski/Anki-Night-Mode.svg?branch=master)](https://travis-ci.org/krassowski/Anki-Night-Mode) [![Code Climate](https://codeclimate.com/github/krassowski/Anki-Night-Mode/badges/gpa.svg)](https://codeclimate.com/github/krassowski/Anki-Night-Mode)


__[Wpis po polsku](http://michal.krassowski.info/komentarz,13)__

This plugin adds the function of night mode, similar that one implemented in AnkiDroid.

### How it works?

It adds a "view" menu entity with options like:
- Automatic (i.e. at specified time) or manual switching of the night mode
- Inverting colors of images or latex formulas
- Defining custom color substitution rules

It provides shortcut <kbd>ctrl</kbd>+<kbd>n</kbd> to quickly switch mode and color picker to adjust some of color parameters.

After enabling night mode, addon changes colors of menubar, toolbar, bottombars and content windows. Take a look at screenshot at the bottom of this page to see an example.

### How can I get it?

#### Automatic install

You can download this addon by Anki.
From menu select: `Tools >> Add-ons >> Browse && Install...` and into prompt put following code:

```python
1496166067
```

after clicking `ok` addon will be downloaded. Then you shall restart your Anki.

To switch into night mode you can use <kbd>ctrl</kbd>+<kbd>n</kbd> shortcut or make use of some new options in your menu: `View >> Night Mode >> ...`.

#### Manual installation

For newer features you may want to install newer version of this addon on your own.
Follow this steps:

1. Get the newest version of file `Night_Mode.py` from GitHub
2. Run Anki, from menu select `Tools >> Add-ons >> Open Add-ons Folder...` to open add-ons folder
4. Copy downloaded file into folder opened in previous step
5. Restart Anki
6. Enjoy

#### After installation

Don't forget to comment and grade it on [Anki webpage](https://ankiweb.net/shared/info/1496166067).


### Preview

![Preview](https://raw.githubusercontent.com/krassowski/Anki-Night-Mode/master/preview.png)

### For developers

Feel free to contribute, send bug reports or feature requests :)

#### Custom CSS in night mode

You may use `night_mode` class, to overtie some of the CSS rules; sometimes usage of `important!` directive or catch-all selector (`*`) will be needed to enforce you own styling. Example:

```css
.night_mode *{
	color: red;
}
```
