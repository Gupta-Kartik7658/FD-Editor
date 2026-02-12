from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor
from PySide6.QtCore import Qt, Signal
import numpy as np


class ImageCanvas(QLabel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 1px solid #ccc;")
        self.pixmap_data = None
    
    def set_image(self, qimage):
        if qimage is not None:
            self.pixmap_data = QPixmap.fromImage(qimage)
            self.setPixmap(self.pixmap_data.scaled(
                self.size(), 
                Qt.KeepAspectRatio, 
                Qt.SmoothTransformation
            ))