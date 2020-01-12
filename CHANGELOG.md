### 2.3.0
*January 12, 2020*
- Delay loading to allow for compatibility with @lovac42's (and potentially others) add-ons (thanks to @lovac42)
- Adapt styling of the browser's sidebar to the changes introduced in Anki 2.1.17 (thanks to @zjosua)

### 2.2.4
*April 20, 2019*
 - Improve styling to eliminate the white rectangle around buttons in the editor in night mode (introduced by Anki 2.1.8)

### 2.2.3
*October 24, 2018*
- Apply night_mode class to Overview and DeckBrowser for future compatibility with Review Heatmap 0.7
- Improve the white background workaround to handle text including bold elements

### 2.2.2
*September 26, 2018*
- Add German translation (by Is)
- Improve the workaround eliminating white backgrounds after using "backspace", "delete", or pasting

### 2.2.1
*September 26, 2018*
- Add Swedish translation (by Jeremias)
- Fix jumping cursor when deleting the last letter in the edit field

### 2.2.0
*September 25, 2018*
- Add Armenian (by Arman High) and Polish translations <a href="https://github.com/krassowski/Anki-Night-Mode/issues/47" rel="nofollow">#47</a>
- Workaround a bug causing white background to appear after deleting a new line <a href="https://github.com/krassowski/Anki-Night-Mode/issues/27" rel="nofollow">#27</a>
- Ensure that text in HTML/Latex edit windows are readable <a href="https://github.com/krassowski/Anki-Night-Mode/issues/44" rel="nofollow">#44</a>

### 2.1.9
*August 11, 2018*
- Invert icons in sidebar of browser <a href="https://github.com/krassowski/Anki-Night-Mode/issues/28" rel="nofollow">#28</a>
- Improve dark scrollbars appearance on Windows
- Make it possible to use arrow-down icon in browser on Windows again
- Improve horizontal splitter styling in browser

### 2.1.8
*August 8, 2018*
- Add dark styling of scrollbars <a href="https://github.com/krassowski/Anki-Night-Mode/issues/35" rel="nofollow">#35</a>
- Improve styling of CardLayout (card types) modal window
- Fix night_mode CSS class being overwritten on question side by the new, fancy Anki fade-in transition logic <a href="https://github.com/krassowski/Anki-Night-Mode/issues/41" rel="nofollow">#41</a>

### 2.1.7
*June 12, 2018*
- Allow to selectively disable reviewer card's styling in the "Choose what to style" dialog <a href="https://github.com/krassowski/Anki-Night-Mode/issues/38" rel="nofollow">#38</a>
- Sort stylers in the "Choose what to style" dialog alphabetically
- Add "check all / uncheck all" to in "Choose what to style" dialog
- Fix night_mode CSS class being applied regardless of night mode state <a href="https://github.com/krassowski/Anki-Night-Mode/issues/37" rel="nofollow">#37</a>

### 2.1.6
*February 21, 2018*
- Improve visibility of items in table in browser <a href="https://github.com/krassowski/Anki-Night-Mode/issues/28" rel="nofollow">#28</a> (thanks nathanmalloy!)
- Provide potential workaround for Qt bug causing Chinese text to be rendered black when selected

### 2.1.5
*January 21, 2017*
 - Allow to selectively disable parts of the add-on #26, #25

### 2.1.4
*January 20, 2017*
 - Add styling to "Statistics" window (when "enable in dialogs" is on) #9

### 2.1.3
*January 15, 2017*
 - Add compatibility with 2.1 beta 31 (which changed progress dialogs interface)


### 2.1.2
*September 23, 2017*
 - Use night mode colors for synchronization/backup progress pop-up dialogs.
 - Minor fix: make selected rows in card browser use night mode colors again.
 
Please note that the new options are only available in addon when running Anki 2.1.x

### 2.1
*September 22, 2017*
 - new option: "Automatic mode" (suggested by p2635: #22) - allows to set times at which the nigh mode should be automatically turned on and off.
 - new option: "Customise colors on cards" - defining custom color mappings just got easier with a new dedicated dialog window - no need to modify source files anymore!
 
Please note that the new options are only available in addon when running Anki 2.1.x
 
### 2.0
*September 19, 2017*
 - new, rewritten addon, compatible with Anki 2.1.x Beta 13+.
 
### 1.2.3
*September 6, 2017*
 - bug fix: make text over difficulty buttons easier to read
 
### 1.2.2
*August 3, 2017*
 - bug fix for Anki 2.1 beta 6
 
### 1.2.1
*August 3, 2017*
 - support for Anki 2.1 beta 6
 
### 1.2.0
*March 6, 2017*
 - initial support for Anki 2.1 (thanks to b50)
 - new option: "Force transparent latex" - assures that latex generation has '-bg transparent' option included.
 - compatibility with Again Hard Good Easy wide big buttons (thanks ankitest)
 
### 1.1.4
*March 4, 2016*
 - added display of visual indication when a button is focused
 - small improvements in the code
 
### 1.1.3
*January 29, 2016*
 - added rule for styling deck's (collapsed/expanded) indicator (+/-)
 
### 1.1.2
*December 16, 2015*
 - improved "invert" function compatibility with different systems
 - increased links visibility on cards in Night Mode - general performance improvements, especially in card editor (you may notice changes if you are using "enable in dialogs" option)
 - small code cleanings
 
### 1.1.0
*November 1, 2015*

 Improvements:
 - better styling of browser window,
 - lighter colors for filtered decks and decks descriptions in Night Mode,
 - some code refinements, allowing easy customization of constants which are not available to edit in GUI.
 
### 1.0.8
*July 8, 2015*

 New features:
 - whole browser window is now styled,
 - card information window is also styled.
 Bugfixes:
 - Rare bug: TypeError: cannot concatenate 'str' and 'function' objects should be gone.
 
### 1.0.6
*June 5, 2015*

![Dialogs preview](https://raw.githubusercontent.com/krassowski/Anki-Night-Mode/master/new_dialogs_preview.png)

 New features:
 - "add card" and "edit current card" are now styled too (if the option "Enable in dialogs" is selected in menu)
 - there is the class name "night_mode" when the night_mode is active (like in AnkiDroid)
 Bugfixes:
 - workaround for Qt error with styling function (at now night mode can be switched only outside dialogs)
 
### 1.0.2
*April 10, 201*
 - Added: dark skin for all menus in Night Mode
 
### 1.0.1
*April 8, 2015*
 - Improvement: lighter color of clozes forced in stylesheets for better readability
