from loguru import logger
from pydantic import BaseModel
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QListWidget, QListWidgetItem, QWidget


class ImageInfo(BaseModel):
    original_width: int
    original_height: int
    width: int
    height: int
    scale_factor: float


class InfoView(QListWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumWidth(400)
        self.setMaximumHeight(100)
        self.info = None

    def update_info(self, info: ImageInfo):
        self.info = info
        self.refresh_view()

    def refresh_view(self):
        self.clear()

        logger.info(f"Displaying info: {self.info}")

        if self.info is None:
            return

        self.add_info_item("Original Image:", f"{self.info.original_width}x{self.info.original_height} pixels")
        self.add_info_item("Display Image:", f"{self.info.width}x{self.info.height} pixels")
        self.add_info_item("Scale Factor:", f"{self.info.scale_factor}x")

    def add_info_item(self, label: str, value: str):
        item = QListWidgetItem()
        self.addItem(item)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(QLabel(label))
        layout.addWidget(QLabel(value))

        widget.setLayout(layout)

        item.setSizeHint(widget.sizeHint())
        self.setItemWidget(item, widget)

    def clear_info(self):
        self.info = None
        self.clear()
