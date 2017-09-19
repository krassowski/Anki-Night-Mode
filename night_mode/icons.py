from os.path import isfile


class Icons:

    paths = {}

    def __init__(self):
        where_to_look_for_arrow_icon = [
            '/usr/share/icons/Adwaita/scalable/actions/pan-down-symbolic.svg',
            '/usr/share/icons/gnome/scalable/actions/go-down-symbolic.svg',
            '/usr/share/icons/ubuntu-mobile/actions/scalable/dropdown-menu.svg',
            '/usr/share/icons/Humanity/actions/16/down.svg',
            '/usr/share/icons/Humanity/actions/16/go-down.svg',
            '/usr/share/icons/Humanity/actions/16/stock_down.svg',
            '/usr/share/icons/nuvola/16x16/actions/arrow-down.png',
            '/usr/share/icons/default.kde4/16x16/actions/arrow-down.png'
        ]

        # It's not an arrow icon,
        # but on windows systems it's better to have this, than nothing.
        arrow_path = ':/icons/gears.png'

        for path in where_to_look_for_arrow_icon:
            if isfile(path):
                arrow_path = path
                break

        self.paths['arrow'] = arrow_path

    @property
    def arrow(self):
        return self.paths['arrow']
