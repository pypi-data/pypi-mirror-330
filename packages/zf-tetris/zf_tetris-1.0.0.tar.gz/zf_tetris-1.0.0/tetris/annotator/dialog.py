from PyQt5.QtCore import QRect
from PyQt5.QtWidgets import (
    QButtonGroup,
    QColorDialog,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QRadioButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from tetris.models import models


class AnnotationInputDialog(QDialog):
    def __init__(self, parent=None, zone: models.Zone | None = None):
        super().__init__(parent)
        self.setWindowTitle("Annotation Input")
        self.setMinimumWidth(400)
        layout = QVBoxLayout(self)

        # Zone type selection
        self.zone_type_group = QButtonGroup(self)
        self.text_zone_radio = QRadioButton("Text Zone")
        self.image_zone_radio = QRadioButton("Image Zone")
        self.zone_type_group.addButton(self.text_zone_radio)
        self.zone_type_group.addButton(self.image_zone_radio)
        self.text_zone_radio.setChecked(True)

        zone_type_layout = QHBoxLayout()
        zone_type_layout.addWidget(self.text_zone_radio)
        zone_type_layout.addWidget(self.image_zone_radio)
        layout.addLayout(zone_type_layout)

        form_layout = QFormLayout()

        self.title_input = QLineEdit(self)
        self.title_input.setMinimumWidth(350)
        form_layout.addRow("Title:", self.title_input)

        self.description_input = QTextEdit(self)
        self.description_input.setMinimumWidth(350)
        self.description_input.setMinimumHeight(100)
        form_layout.addRow("Description:", self.description_input)

        # Text Zone specific inputs
        self.font_family_input = QComboBox(self)
        self.font_family_input.addItems(
            ["Arial", "Helvetica", "Impact", "Times New Roman", "Courier", "Verdana"]
        )
        self.font_family_input.setCurrentText("Arial")
        form_layout.addRow("Font Family:", self.font_family_input)

        self.font_size_input = QComboBox(self)
        self.font_size_input.addItems([str(i) for i in range(8, 73, 2)])
        self.font_size_input.setCurrentText("32")
        form_layout.addRow("Font Size:", self.font_size_input)

        self.font_color_button = QPushButton("Select Color")
        self.font_color_button.clicked.connect(self.select_color)
        self.font_color = "#000000"
        self.font_color_button.setStyleSheet(f"background-color: {self.font_color};")
        form_layout.addRow("Font Color:", self.font_color_button)

        layout.addLayout(form_layout)

        examples_layout = QVBoxLayout()
        examples_label = QLabel("Examples:")
        examples_layout.addWidget(examples_label)

        self.examples_list = QListWidget(self)
        self.examples_list.setMinimumWidth(350)
        self.examples_list.setMinimumHeight(100)
        examples_layout.addWidget(self.examples_list)

        example_input_layout = QHBoxLayout()
        self.example_input = QLineEdit(self)
        example_input_layout.addWidget(self.example_input)
        add_example_button = QPushButton("Add")
        add_example_button.clicked.connect(self.add_example)
        example_input_layout.addWidget(add_example_button)
        examples_layout.addLayout(example_input_layout)

        layout.addLayout(examples_layout)

        if zone:
            self.title_input.setText(zone.title)
            self.description_input.setText(zone.description)

            for example in zone.examples:
                self.add_example_to_list(example)

            if isinstance(zone, models.TextZone):
                self.text_zone_radio.setChecked(True)

                self.font_family_input.setCurrentText(zone.font_family)
                self.font_size_input.setCurrentText(str(zone.font_size))
                self.font_color = zone.font_color
                self.font_color_button.setStyleSheet(
                    f"background-color: {self.font_color};"
                )
            else:
                self.image_zone_radio.setChecked(True)

        # Connect radio buttons to update UI
        self.text_zone_radio.toggled.connect(self.update_ui)
        self.image_zone_radio.toggled.connect(self.update_ui)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, self)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)
        self.update_ui()

    def update_ui(self):
        is_text_zone = self.text_zone_radio.isChecked()
        self.font_family_input.setVisible(is_text_zone)
        self.font_size_input.setVisible(is_text_zone)
        self.font_color_button.setVisible(is_text_zone)

    def add_example(self):
        example = self.example_input.text().strip()
        if example:
            self.add_example_to_list(example)
            self.example_input.clear()

    def add_example_to_list(self, example):
        item = QListWidgetItem(self.examples_list)
        self.examples_list.addItem(item)

        widget = QWidget()
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(example)
        layout.addWidget(label)

        delete_button = QPushButton("Delete")
        delete_button.clicked.connect(lambda: self.delete_example(item))
        layout.addWidget(delete_button)

        widget.setLayout(layout)

        item.setSizeHint(widget.sizeHint())
        self.examples_list.setItemWidget(item, widget)

    def delete_example(self, item):
        row = self.examples_list.row(item)
        self.examples_list.takeItem(row)

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.font_color = color.name()
            self.font_color_button.setStyleSheet(
                f"background-color: {self.font_color};"
            )

    def make_new_zone(
        self, rect: QRect | None = None, zone: models.Zone | None = None
    ) -> models.Zone:
        if not rect and not zone:
            raise ValueError("Either rect or zone must be provided")

        examples = []
        for i in range(self.examples_list.count()):
            item = self.examples_list.item(i)
            widget = self.examples_list.itemWidget(item)
            label = widget.layout().itemAt(0).widget()
            examples.append(label.text())

        zone_type = (
            models.ZoneType.TextZone
            if self.text_zone_radio.isChecked()
            else models.ZoneType.ImageZone
        )

        bbox = (rect.x(), rect.y(), rect.width(), rect.height()) if rect else zone.bbox

        if zone_type == models.ZoneType.TextZone:
            return models.TextZone(
                type=zone_type,
                bbox=bbox,
                title=self.title_input.text(),
                description=self.description_input.toPlainText(),
                examples=examples,
                angle=0,
                font_family=self.font_family_input.currentText(),
                font_size=int(self.font_size_input.currentText()),
                font_color=self.font_color,
            )
        else:
            return models.ImageZone(
                type=zone_type,
                bbox=bbox,
                title=self.title_input.text(),
                description=self.description_input.toPlainText(),
                examples=examples,
                angle=0,
            )
