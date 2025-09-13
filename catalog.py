# catalog.py

import os
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import QSize

from pieces.straight_road import StraightPiece
from pieces.long_straight_road import LongStraightPiece
from pieces.curve import CurvePiece
from pieces.cross import CrossPiece
from pieces.t_road import TRoadPiece

from constants import CATALOG_WIDTH

class CatalogWidget(QWidget):
    def __init__(self, game_widget, parent=None):
        super().__init__(parent)
        self.game_widget = game_widget
        self.setFixedWidth(CATALOG_WIDTH)
        
        self.layout = QVBoxLayout()
        self.label = QLabel("Catálogo")
        self.layout.addWidget(self.label)

        self.setup_buttons()

        self.layout.addStretch()
        self.setLayout(self.layout)

    def setup_buttons(self):
        catalog_items = [
            {"label": "Recta", "icon": "assets/straight_road.png", "class": StraightPiece},
            {"label": "Recta Larga", "icon": "assets/long_straight_road.png", "class": LongStraightPiece},
            {"label": "Curva", "icon": "assets/curve.png", "class": CurvePiece},
            {"label": "Cruce", "icon": "assets/cross.png", "class": CrossPiece},
            {"label": "Cruce en T", "icon": "assets/t_road.png", "class": TRoadPiece},
        ]

        for item in catalog_items:
            button = QPushButton(item["label"])
            if os.path.exists(item["icon"]):
                button.setIcon(QIcon(QPixmap(item["icon"])))
                button.setIconSize(QSize(64, 64))
            
            button.clicked.connect(lambda checked, pc=item["class"]: self.game_widget.create_piece_from_catalog(pc))
            self.layout.addWidget(button)