from aqt import mw
from anki.hooks import addHook


#addons should selectively load before or after a delay of 666
NM_RESERVED_DELAY = 666

night_mode = None

def delayedLoader():
    """
        Delays loading of NM to avoid addon conflicts.
    """
    global night_mode
    from .night_mode import NightMode
    night_mode = NightMode()
    night_mode.load()

def onProfileLoaded():
    if not night_mode:
        mw.progress.timer(
            NM_RESERVED_DELAY, delayedLoader, False
        )
    else:
        night_mode.load()

addHook('profileLoaded', onProfileLoaded)
