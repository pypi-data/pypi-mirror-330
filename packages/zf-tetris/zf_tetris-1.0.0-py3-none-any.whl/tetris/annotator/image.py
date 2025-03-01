import os
from json import load as json_load
from os import path as os_path

from loguru import logger
from PyQt5.QtCore import QLineF, QPoint, QPointF, QRect, QRectF, QSizeF, Qt, pyqtSignal
from PyQt5.QtGui import QColor, QFont, QKeySequence, QPainter, QPen, QPixmap, QTransform
from PyQt5.QtWidgets import (
    QDialog,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QShortcut,
    QSplitter,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from ..models import models
from .dialog import AnnotationInputDialog
from .zones import ZonesView
from .info import ImageInfo, InfoView


class ImageAnnotationTool(QMainWindow):
    annotationSaved = pyqtSignal(object)
    refreshed = pyqtSignal(object)

    def __init__(
        self,
        image_source: models.FileSource | None = None,
        image_description: str = "",
        zones: list[models.Zone] | None = None,
    ):
        super().__init__()
        self.initUI(image_source, image_description, zones)
        self.setup_shortcuts()

        self.resize_handle = None
        self.resizing_index = -1
        self.dragging_index = -1
        self.rotating_index = -1
        self.drag_start_pos = None
        self.scale_factor = 1.0

    def initUI(
        self,
        image_source: models.FileSource | None = None,
        image_description: str = "",
        zones: list[models.Zone] | None = None,
    ):
        self.image_source = image_source
        self.image_description = image_description

        self.scale_factor = 1.0

        self.original_image = None
        self.image = None  # scaled

        self.cached_description: str = ""
        self.description: str = ""

        # original zones
        self.original_zones: list[models.Zone] = zones or []

        # scaled zones
        self.zones: list[models.Zone] = [
            tz * self.scale_factor for tz in self.original_zones
        ]

        self.unsaved_changes = False

        self.start_point = None
        self.current_rect = None

        self.setWindowTitle(
            f"Image Annotation Tool ({self.image_source.beautify_name()})"
        )
        self.setGeometry(100, 100, 1200, 600)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)

        self.description_text_area = QTextEdit()
        self.description_text_area.setPlaceholderText("Enter meme description here...")
        self.description_text_area.setMaximumHeight(100)
        self.description_text_area.setText(self.image_description)
        main_layout.addWidget(self.description_text_area)

        image_and_annotations_layout = QHBoxLayout()
        main_layout.addLayout(image_and_annotations_layout)

        left_widget = QWidget()
        left_layout = QVBoxLayout()
        left_widget.setLayout(left_layout)

        self.image_label = QLabel()
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setFixedHeight(768)
        left_layout.addWidget(self.image_label)

        button_layout = QHBoxLayout()
        load_button = QPushButton("Load Image")
        load_button.clicked.connect(self.load_image)
        button_layout.addWidget(load_button)

        self.save_button = QPushButton("Save Annotations")
        self.save_button.clicked.connect(self.save_annotations)
        button_layout.addWidget(self.save_button)

        left_layout.addLayout(button_layout)

        right_widget = QWidget()
        right_layout = QVBoxLayout()
        right_widget.setLayout(right_layout)

        # Image info
        self.info_view = InfoView()
        right_layout.addWidget(QLabel("Image Info:"))
        right_layout.addWidget(self.info_view)

        # Annotations
        self.zones_view = ZonesView()
        self.zones_view.zoneEdited.connect(self.edit_zone)
        self.zones_view.zoneDeleted.connect(self.delete_zone)
        self.zones_view.zoneDuplicated.connect(self.duplicate_zone)
        self.zones_view.fontSizeChanged.connect(self.change_font_size)
        self.zones_view.fontColorFlipped.connect(self.flip_black_white_font_color)

        right_layout.addWidget(QLabel("Annotations:"))
        right_layout.addWidget(self.zones_view)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        splitter.setSizes([700, 300])

        image_and_annotations_layout.addWidget(splitter)

        if image_source:
            self.load_image_from_file_source(image_source.path)

        if self.image:
            self.display_image_and_zones()

    def load_image_from_file_source(self, image_path: str):
        if not os.path.exists(image_path):
            logger.error(f"File not found: {image_path}")
            return

        self.original_image = QPixmap(image_path)
        if self.original_image.isNull():
            logger.error(f"Failed to load image from {image_path}")
            return

        self.image_source = models.FileSource.from_filepath(image_path)
        logger.info(f"Successfully loaded image from {image_path}")

        self.load_and_scale_image()
        self.load_and_scale_zones()

        self.display_image_and_zones()

        self.zones_view.set_zones(self.zones)

    def load_and_scale_image(self):
        if self.original_image.height() > 768:
            self.scale_factor = 768 / self.original_image.height()

            new_width = int(self.original_image.width() * self.scale_factor)
            self.image = self.original_image.scaled(
                new_width, 768, Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
        else:
            self.scale_factor = 1.0
            self.image = QPixmap(self.original_image)

        self.image_label.setFixedSize(self.image.width(), self.image.height())

        logger.info(
            f"Original image size: {self.original_image.width()}x{self.original_image.height()}"
        )
        logger.info(f"Scaled image size: {self.image.width()}x{self.image.height()}")
        logger.info(
            f"Image label size: {self.image_label.width()}x{self.image_label.height()}"
        )
        logger.info(f"Scale factor: {self.scale_factor}")

        self.display_image_and_zones()
        self.info_view.update_info(
            ImageInfo(
                original_width=self.original_image.width(),
                original_height=self.original_image.height(),
                width=self.image.width(),
                height=self.image.height(),
                scale_factor=self.scale_factor,
            )
        )

    def load_and_scale_zones(self):
        templates_path = f"{self.image_source.dir}/templates.json"

        if not self.original_zones:
            self.original_zones = []

            if os_path.exists(templates_path):
                with open(templates_path, "r") as f:
                    templates = json_load(f)

                    if self.image_source.name in templates:
                        meme_data = templates[self.image_source.name]

                        if "text_zones" in meme_data:
                            self.original_zones.extend(
                                [
                                    models.TextZone(**tz)
                                    for tz in meme_data["text_zones"]
                                ]
                            )

                        if "image_zones" in meme_data:
                            self.original_zones.extend(
                                [
                                    models.ImageZone(**iz)
                                    for iz in meme_data["image_zones"]
                                ]
                            )
        else:
            logger.info(
                f"Annotations already loaded for {self.image_source.name}, scaling..."
            )

        self.zones = [tz * self.scale_factor for tz in self.original_zones]

    def add_new_zone(self, rect: QRect):
        dialog = AnnotationInputDialog(parent=self)

        if dialog.exec_() == QDialog.Accepted:
            new_zone = dialog.make_new_zone(rect=rect)
            new_zone.angle = 0

            self.zones.append(new_zone)
            self.zones_view.add_zone(new_zone)

            self.draw_image_with_annotations()
            self.save_annotations(autosave=True)

    def duplicate_zone(self, zone: models.Zone):
        new_zone = zone.__class__(
            bbox=(
                zone.bbox[0] + 10,
                zone.bbox[1] + 10,
                zone.bbox[2],
                zone.bbox[3],
            ),
            title=f"{zone.title} (Copy)",
            description=zone.description,
            examples=zone.examples,
            **zone.extra_attributes(),
        )
        self.zones.append(new_zone)
        self.zones_view.add_zone(new_zone)
        self.draw_image_with_annotations()
        self.save_annotations(autosave=True)

    def edit_zone(self, zone: models.Zone):
        dialog = AnnotationInputDialog(parent=self, zone=zone)

        if dialog.exec_() == QDialog.Accepted:
            new_zone = dialog.make_new_zone(zone=zone)

            self.zones[self.zones.index(zone)] = new_zone
            self.zones_view.update_zone(zone, new_zone)

            self.draw_image_with_annotations()
            self.save_annotations(autosave=True)

    def delete_zone(self, zone: models.Zone):
        self.zones.remove(zone)
        self.zones_view.remove_zone(zone)

        self.draw_image_with_annotations()
        self.save_annotations(autosave=True)

    def display_image_and_zones(self):
        if self.image and not self.image.isNull():
            self.draw_image_with_annotations()
        else:
            logger.warning("Attempted to display null or non-existent image")

    def draw_image_with_annotations(self):
        """Draw the image with annotations on the image label using the scaled image and scaled zones"""
        if self.image:
            pixmap = QPixmap(self.image)
            painter = QPainter(pixmap)

            for zone in self.zones:
                rect = QRect(*zone.bbox)
                center = rect.center()

                transform = QTransform()
                transform.translate(center.x(), center.y())
                transform.rotate(zone.angle)
                transform.translate(-center.x(), -center.y())

                painter.setTransform(transform)

                painter.setPen(QColor("red"))
                painter.drawRect(rect)

                self.draw_resize_handles(painter, rect)
                self.draw_rotation_handle(painter, rect)

                if isinstance(zone, models.TextZone):
                    font = QFont(
                        zone.font_family, int(zone.font_size * self.scale_factor)
                    )
                    painter.setFont(font)
                    painter.setPen(QColor(zone.font_color))
                    painter.drawText(rect, Qt.AlignCenter, zone.title)
                elif isinstance(zone, models.ImageZone):
                    painter.drawText(rect, Qt.AlignCenter, "Image Zone")

                painter.resetTransform()

            if self.current_rect:
                painter.setPen(QPen(QColor(255, 0, 0), 2))
                painter.drawRect(self.current_rect)

            painter.end()
            self.image_label.setPixmap(pixmap)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image File", "", "Images (*.png )"
        )

        if file_name:
            self.load_image_from_file_source(file_name)

    def update_save_button(self):
        if self.unsaved_changes:
            self.save_button.setStyleSheet(
                "QPushButton { background-color: #4CAF50; color: white; }"
            )
            self.save_button.setText("Save Annotations*")
        else:
            self.save_button.setStyleSheet("")
            self.save_button.setText("Save Annotations")

    def save_annotations(self, autosave=False):
        if not self.zones:
            logger.error("No annotations to save")
            return

        scale_factor = self.image.height() / self.original_image.height()
        zones = [tz / scale_factor for tz in self.zones]
        description = self.description_text_area.toPlainText()

        self.annotationSaved.emit((self.image_source, zones, description, not autosave))

        self.unsaved_changes = False
        self.update_save_button()

        if not autosave:
            logger.info("Annotations saved successfully")

    def mousePressEvent(self, event):
        if self.image and event.button() == Qt.LeftButton:
            pos = self.get_image_pos(event.pos())

            self.resize_handle, self.resizing_index = self.get_resize_handle(pos)
            self.rotating_index = self.get_rotating_annotation(pos)

            logger.info(
                f"resize_handle: {self.resize_handle}, resizing_index: {self.resizing_index}, rotating_index: {self.rotating_index}, dragging_index: {self.dragging_index}"
            )

            if self.resize_handle is None and self.rotating_index == -1:
                self.dragging_index = self.get_dragging_annotation(pos)

                if self.dragging_index != -1:
                    self.drag_start_pos = pos
                else:
                    self.start_point = pos
                    self.current_rect = None
            else:
                self.start_point = pos

            self.draw_image_with_annotations()

    def mouseMoveEvent(self, event):
        if (
            not self.start_point
            and self.dragging_index == -1
            and self.rotating_index == -1
        ):
            return

        pos = self.get_image_pos(event.pos())

        if self.resize_handle is not None:
            self.resize_annotation(pos)
        elif self.rotating_index != -1:
            self.rotate_annotation(pos)
        elif self.dragging_index != -1:
            self.drag_annotation(pos)
        else:
            self.current_rect = QRect(self.start_point, pos).normalized()

        self.draw_image_with_annotations()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and (
            self.start_point or self.dragging_index != -1 or self.rotating_index != -1
        ):
            end_point = self.get_image_pos(event.pos())

            if self.resize_handle is not None:
                self.resize_handle = None
                self.resizing_index = -1
                self.unsaved_changes = True
            elif self.rotating_index != -1:
                self.rotating_index = -1
                self.unsaved_changes = True
            elif self.dragging_index != -1:
                self.dragging_index = -1
                self.drag_start_pos = None
                self.unsaved_changes = True
            else:
                rect = QRect(self.start_point, end_point).normalized()
                if rect.width() > 10 and rect.height() > 10:
                    self.add_new_zone(rect)

            self.start_point = None
            self.current_rect = None
            self.draw_image_with_annotations()
            self.update_save_button()

    def get_resize_handle(self, pos):
        handle_size = 10

        for i, zone in enumerate(self.zones):
            rect = QRectF(*zone.bbox)
            center = rect.center()

            transform = QTransform()
            transform.translate(center.x(), center.y())
            transform.rotate(zone.angle)
            transform.translate(-center.x(), -center.y())

            handles = [
                QRectF(rect.topLeft(), QSizeF(handle_size, handle_size)),
                QRectF(rect.topRight().x() - handle_size, rect.topRight().y(), handle_size, handle_size),
                QRectF(rect.bottomLeft().x(), rect.bottomLeft().y() - handle_size, handle_size, handle_size),
                QRectF(rect.bottomRight().x() - handle_size, rect.bottomRight().y() - handle_size, handle_size, handle_size),
            ]

            for j, handle in enumerate(handles):
                transformed_handle = transform.mapRect(handle)
                if transformed_handle.contains(pos):
                    return j, i

        return None, -1

    def resize_annotation(self, pos):
        if 0 <= self.resizing_index < len(self.zones):
            text_zone = self.zones[self.resizing_index]

            rect = QRectF(*text_zone.bbox)

            if self.resize_handle == 0:
                rect.setTopLeft(pos)
            elif self.resize_handle == 1:
                rect.setTopRight(pos)
            elif self.resize_handle == 2:
                rect.setBottomLeft(pos)
            elif self.resize_handle == 3:
                rect.setBottomRight(pos)

            self.zones[self.resizing_index].bbox = (
                int(rect.x()),
                int(rect.y()),
                int(rect.width()),
                int(rect.height()),
            )

            self.draw_image_with_annotations()

    def draw_resize_handles(self, painter, rect):
        handle_size = 10

        original_brush = painter.brush()  # Save the original brush
        original_pen = painter.pen()  # Save the original pen

        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(Qt.NoPen)  # No outline for the handles

        painter.drawRect(
            rect.topLeft().x(), rect.topLeft().y(), handle_size, handle_size
        )
        painter.drawRect(
            rect.topRight().x() - handle_size,
            rect.topRight().y(),
            handle_size,
            handle_size,
        )
        painter.drawRect(
            rect.bottomLeft().x(),
            rect.bottomLeft().y() - handle_size,
            handle_size,
            handle_size,
        )
        painter.drawRect(
            rect.bottomRight().x() - handle_size,
            rect.bottomRight().y() - handle_size,
            handle_size,
            handle_size,
        )

        painter.setBrush(original_brush)
        painter.setPen(original_pen)

    def refresh(self):
        self.refreshed.emit(None)

    def save(self):
        self.save_annotations(autosave=True)

    def closeEvent(self, event):
        self.save_annotations(autosave=True)
        super().closeEvent(event)

    def get_dragging_annotation(self, pos):
        for i, zone in enumerate(self.zones):
            rect = QRectF(*zone.bbox)
            if rect.contains(pos):
                return i
        return -1

    def drag_annotation(self, pos):
        if 0 <= self.dragging_index < len(self.zones):
            zone = self.zones[self.dragging_index]
            dx = pos.x() - self.drag_start_pos.x()
            dy = pos.y() - self.drag_start_pos.y()

            new_x = zone.bbox[0] + dx
            new_y = zone.bbox[1] + dy

            self.zones[self.dragging_index].bbox = (
                int(new_x),
                int(new_y),
                zone.bbox[2],
                zone.bbox[3],
            )

            self.drag_start_pos = pos

    def setup_shortcuts(self):
        refresh_shortcut = QShortcut(QKeySequence("Ctrl+R"), self)
        refresh_shortcut.activated.connect(self.refresh)

        close_shortcut = QShortcut(QKeySequence("Ctrl+W"), self)
        close_shortcut.activated.connect(self.close)

        save_shortcut = QShortcut(QKeySequence("Ctrl+S"), self)
        save_shortcut.activated.connect(self.save)

    def change_font_size(self, zone, delta):
        if isinstance(zone, models.TextZone):
            new_size = max(1, zone.font_size + delta)
            zone.font_size = new_size
            self.zones_view.update_zone(zone, zone)
            self.draw_image_with_annotations()
            self.save_annotations(autosave=True)

    def flip_black_white_font_color(self, zone):
        if isinstance(zone, models.TextZone):
            if zone.font_color == "#000000":
                zone.font_color = "#FFFFFF"
            else:
                zone.font_color = "#000000"
            self.zones_view.update_zone(zone, zone)
            self.draw_image_with_annotations()
            self.save_annotations(autosave=True)

    def draw_rotation_handle(self, painter, rect):
        handle_size = 20
        center = rect.center()
        top_center = QPointF(center.x(), rect.top() - handle_size)

        painter.setPen(QPen(QColor(0, 255, 0), 2))
        painter.drawLine(QLineF(center, top_center))
        painter.drawEllipse(top_center, 5, 5)

    def get_rotating_annotation(self, pos):
        for i, zone in enumerate(self.zones):
            rect = QRectF(*zone.bbox)
            center = rect.center()
            top_center = QPointF(center.x(), rect.top() - 20)

            rotation_handle = QRectF(top_center.x() - 5, top_center.y() - 5, 10, 10)

            transform = QTransform()
            transform.translate(center.x(), center.y())
            transform.rotate(zone.angle)
            transform.translate(-center.x(), -center.y())

            if transform.mapRect(rotation_handle).contains(pos):
                return i
        return -1

    def rotate_annotation(self, pos):
        if 0 <= self.rotating_index < len(self.zones):
            zone = self.zones[self.rotating_index]
            rect = QRectF(*zone.bbox)
            center = rect.center()

            start_vector = QLineF(center, QPointF(center.x(), rect.top() - 20))
            current_vector = QLineF(center, pos)

            angle = current_vector.angleTo(start_vector)
            zone.angle = angle

            self.zones_view.update_zone(zone, zone)

    def get_image_pos(self, pos):
        label_pos = self.image_label.mapFrom(self, pos)
        image_rect = self.image_label.contentsRect()

        if image_rect.contains(label_pos):
            return QPoint(
                label_pos.x() - image_rect.x(), label_pos.y() - image_rect.y()
            )

        return pos
