from os import makedirs
from os.path import isfile, dirname, abspath, join
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QStyle


def inverted_icon(icon, width=32, height=32, as_image=False):
    pixmap = icon.pixmap(width, height)
    image = pixmap.toImage()
    image.invertPixels()
    if as_image:
        return image
    new_icon = QIcon(QPixmap.fromImage(image))
    return new_icon


class Icons:

    paths = {}

    def __init__(self, mw):

        add_on_path = dirname(abspath(__file__))
        add_on_resources = join(add_on_path, 'user_files')
        icons_path = join(add_on_resources, 'icons')
        makedirs(icons_path, exist_ok=True)

        icon_path = join(icons_path, 'arrow.png')

        if not isfile(icon_path):
            down_arrow_icon = mw.style().standardIcon(QStyle.SP_ArrowDown)
            image = inverted_icon(down_arrow_icon, width=16, height=16, as_image=True)
            image.save(icon_path)

        arrow_path = icon_path.replace('\\', '/')

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

        for path in where_to_look_for_arrow_icon:
            if isfile(path):
                arrow_path = path
                break

        self.paths['arrow'] = arrow_path

    @property
    def arrow(self):
        return self.paths['arrow']
