from anki_testing import anki_running


def test_appends():

    with anki_running():
        from night_mode.stylers import Styler
        from night_mode.internals import appends_in_night_mode

        class SomeElement:

            my_css = 'css'

        class SomeElementStyler(Styler):
            target = SomeElement

            @appends_in_night_mode
            def my_css(self):
                return ' and my injection!'

        element = SomeElement()
        assert SomeElementStyler.additions['my_css'].value(element) == ' and my injection!'
