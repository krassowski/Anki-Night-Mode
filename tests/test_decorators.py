from anki_testing import anki_running


def test_property_descriptor():
    with anki_running():
        from night_mode.internals import PropertyDescriptor

        class Test:

            @PropertyDescriptor
            def test(self):
                return 'x'

        t = Test()

        assert t.test == 'x'
        assert getattr(t, 'test') == 'x'


def test_appends_in_night_mode():
    pass
