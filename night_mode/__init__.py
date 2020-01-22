from aqt import mw
from anki.hooks import addHook, remHook


#addons should selectively load before or after a delay of 666
NM_RESERVED_DELAY = 666


def delayedLoader():
    from .night_mode import NightMode
    night_mode = NightMode()
    night_mode.load()

def onProfileLoaded():
    remHook("profileLoaded", onProfileLoaded)
    mw.progress.timer(
        NM_RESERVED_DELAY, delayedLoader, False
    )

addHook('profileLoaded', onProfileLoaded)
