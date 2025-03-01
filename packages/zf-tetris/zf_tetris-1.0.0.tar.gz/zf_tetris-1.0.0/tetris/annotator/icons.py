from glob import glob
from os import path as os_path

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPainter, QPixmap
from PyQt5.QtSvg import QSvgRenderer


class IconsManager:
    def __init__(self):
        self.icon_path = os_path.join(os_path.dirname(__file__), "icons")
        self.svgs = glob(os_path.join(self.icon_path, "*.svg"))
        self.icons = {}

    def load_icons(self):
        for svg in self.svgs:
            icon_name = os_path.basename(svg).split(".")[0]
            self.icons[icon_name] = self._load_icon_(svg)

    def _load_icon_(self, icon_path, size=24):
        if not os_path.exists(icon_path):
            raise FileNotFoundError(f"Icon not found: {icon_path}")

        renderer = QSvgRenderer(icon_path)
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.transparent)
        painter = QPainter(pixmap)
        renderer.render(painter)
        painter.end()
        return QIcon(pixmap)  # Return QIcon instead of QPixmap

    def __getitem__(self, icon_name):
        if icon_name not in self.icons:
            self.icons[icon_name] = self._load_icon_(os_path.join(self.icon_path, f"{icon_name}.svg"))
        return self.icons[icon_name]


Icons = IconsManager()
