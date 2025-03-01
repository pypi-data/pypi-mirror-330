from loguru import logger
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QToolButton,
    QWidget,
)

from tetris.models import models

from .icons import Icons

def get_zone_type_short_name(zone_type: str) -> str:
    return "TZ" if zone_type == "TextZone" else "IZ"

class ZonesView(QListWidget):
    zoneEdited = pyqtSignal(models.Zone)
    zoneDeleted = pyqtSignal(models.Zone)
    zoneDuplicated = pyqtSignal(models.Zone)
    fontSizeChanged = pyqtSignal(models.Zone, int)
    fontColorFlipped = pyqtSignal(models.Zone)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(400)
        self.zones_map = {}

    def set_zones(self, zones: list[models.Zone]):
        self.zones_map = {zone.title: zone for zone in zones}
        self.refresh_view()

    def add_zone(self, zone: models.Zone):
        self.zones_map[zone.title] = zone
        self.add_zone_item(zone)

    def remove_zone(self, zone: models.Zone):
        del self.zones_map[zone.title]
        self.refresh_view()

    def update_zone(self, old_zone: models.Zone, new_zone: models.Zone):
        if old_zone.title in self.zones_map:
            del self.zones_map[old_zone.title]

        self.zones_map[new_zone.title] = new_zone
        self.refresh_view()

    def refresh_view(self):
        self.clear()

        logger.info(f"Displaying zones: {self.zones_map}")

        for zone in self.zones_map.values():
            self.add_zone_item(zone)

    def add_zone_item(self, zone: models.Zone):
        item = QListWidgetItem()
        self.addItem(item)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(f"[{get_zone_type_short_name(zone.type)}] {zone.title}")
        layout.addWidget(label)

        if isinstance(zone, models.TextZone):
            flip_black_white_color_button = QToolButton()
            flip_black_white_color_button.setIcon(Icons["paintbrush"])
            flip_black_white_color_button.clicked.connect(
                lambda: self.fontColorFlipped.emit(zone)
            )
            layout.addWidget(flip_black_white_color_button)

            increase_font_button = QToolButton()
            increase_font_button.setText("+")
            increase_font_button.clicked.connect(
                lambda: self.fontSizeChanged.emit(zone, 2)
            )
            layout.addWidget(increase_font_button)

            decrease_font_button = QToolButton()
            decrease_font_button.setText("-")
            decrease_font_button.clicked.connect(
                lambda: self.fontSizeChanged.emit(zone, -2)
            )
            layout.addWidget(decrease_font_button)

        duplicate_button = QToolButton()
        duplicate_button.setIcon(Icons["copy-plus"])
        duplicate_button.clicked.connect(lambda: self.zoneDuplicated.emit(zone))
        layout.addWidget(duplicate_button)

        edit_button = QToolButton()
        edit_button.setIcon(Icons["pencil"])
        edit_button.clicked.connect(lambda: self.zoneEdited.emit(zone))
        layout.addWidget(edit_button)

        delete_button = QToolButton()
        delete_button.setIcon(Icons["X"])
        delete_button.clicked.connect(lambda: self.zoneDeleted.emit(zone))
        layout.addWidget(delete_button)

        widget.setLayout(layout)

        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)

    def clear_zones(self):
        self.zones_map.clear()
        self.clear()
