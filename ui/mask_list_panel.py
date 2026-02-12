from PySide6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, 
                               QListWidgetItem, QHBoxLayout, QPushButton, QCheckBox)
from PySide6.QtCore import Signal, Qt


class MaskListPanel(QWidget):
    mask_selected = Signal(object)
    mask_toggled = Signal(object, bool)
    mask_deleted = Signal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.masks = []
        self.item_widgets = {}
        
        layout = QVBoxLayout(self)
        layout.setSpacing(5)
        
        title = QLabel("Mask Layers")
        title.setStyleSheet("font-weight: bold; font-size: 14px; padding: 5px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        self.list_widget = QListWidget()
        self.list_widget.itemClicked.connect(self.on_item_clicked)
        layout.addWidget(self.list_widget)
        
        info_label = QLabel("Click to select\nUncheck to disable")
        info_label.setStyleSheet("color: #666; font-size: 10px;")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
    
    def add_mask(self, mask):
        self.masks.append(mask)
        
        item = QListWidgetItem()
        widget = self._create_mask_item_widget(mask)
        item.setSizeHint(widget.sizeHint())
        
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)
        
        self.item_widgets[mask] = (item, widget)
    
    def remove_mask(self, mask):
        if mask in self.masks:
            index = self.masks.index(mask)
            self.masks.remove(mask)
            self.list_widget.takeItem(index)
            if mask in self.item_widgets:
                del self.item_widgets[mask]
    
    def clear_masks(self):
        self.masks.clear()
        self.list_widget.clear()
        self.item_widgets.clear()
    
    def update_mask_display(self, mask):
        if mask in self.item_widgets:
            item, old_widget = self.item_widgets[mask]
            new_widget = self._create_mask_item_widget(mask)
            self.list_widget.setItemWidget(item, new_widget)
            self.item_widgets[mask] = (item, new_widget)
    
    def _create_mask_item_widget(self, mask):
        widget = QWidget()
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(5, 2, 5, 2)
        
        checkbox = QCheckBox()
        checkbox.setChecked(mask.enabled)
        checkbox.stateChanged.connect(lambda state: self.mask_toggled.emit(mask, state == Qt.Checked))
        layout.addWidget(checkbox)
        
        mode_indicator = "🔴" if mask.mode.value == "Remove" else "🟢"
        label = QLabel(f"{mode_indicator} {mask.mask_type.value}")
        layout.addWidget(label)
        
        layout.addStretch()
        
        delete_btn = QPushButton("✕")
        delete_btn.setMaximumWidth(25)
        delete_btn.setStyleSheet("color: red; font-weight: bold;")
        delete_btn.clicked.connect(lambda: self.mask_deleted.emit(mask))
        layout.addWidget(delete_btn)
        
        return widget
    
    def on_item_clicked(self, item):
        index = self.list_widget.row(item)
        if 0 <= index < len(self.masks):
            self.mask_selected.emit(self.masks[index])