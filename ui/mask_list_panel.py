from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel


class MaskListPanel(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        
        title = QLabel("Masks")
        title.setStyleSheet("font-weight: bold;")
        self.layout.addItem(title)