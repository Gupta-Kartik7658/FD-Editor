from PySide6.QtWidgets import QLabel
from PySide6.QtGui import QPixmap, QPainter, QPen, QColor, QBrush
from PySide6.QtCore import Qt, Signal, QPoint
import numpy as np
from core.mask import MaskType


class ImageCanvas(QLabel):
    mask_created = Signal(object)
    tool_selected = Signal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(400, 400)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("border: 2px solid #aaa; background-color: #f5f5f5;")
        
        self.pixmap_data = None
        self.current_tool = None
        self.is_drawing = False
        self.start_point = None
        self.current_point = None
        self.freedraw_points = []
        self.spectrum_shape = None
        
        self.setMouseTracking(False)
    
    def set_image(self, qimage):
        if qimage is not None:
            self.pixmap_data = QPixmap.fromImage(qimage)
            self.update()
    
    def set_spectrum_shape(self, shape):
        self.spectrum_shape = shape
    
    def set_tool(self, tool_type):
        self.current_tool = tool_type
        self.setMouseTracking(tool_type == MaskType.FREEDRAW)
        self.tool_selected.emit()
    
    def paintEvent(self, event):
        super().paintEvent(event)
        
        if self.pixmap_data is None:
            return
        
        painter = QPainter(self)
        
        # Draw the image centered
        pixmap_scaled = self.pixmap_data.scaled(
            self.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        x = (self.width() - pixmap_scaled.width()) // 2
        y = (self.height() - pixmap_scaled.height()) // 2
        painter.drawPixmap(x, y, pixmap_scaled)
        
        # Draw current drawing overlay
        if self.is_drawing and self.start_point and self.current_point:
            pen = QPen(QColor(255, 0, 0), 2, Qt.SolidLine)
            painter.setPen(pen)
            
            if self.current_tool == MaskType.RECTANGLE:
                painter.drawRect(
                    self.start_point.x(),
                    self.start_point.y(),
                    self.current_point.x() - self.start_point.x(),
                    self.current_point.y() - self.start_point.y()
                )
            
            elif self.current_tool == MaskType.CIRCLE:
                radius = int(((self.current_point.x() - self.start_point.x())**2 + 
                             (self.current_point.y() - self.start_point.y())**2)**0.5)
                painter.drawEllipse(self.start_point, radius, radius)
        
        if self.current_tool == MaskType.FREEDRAW and self.freedraw_points:
            pen = QPen(QColor(255, 0, 0), 3, Qt.SolidLine)
            painter.setPen(pen)
            for i in range(len(self.freedraw_points) - 1):
                painter.drawLine(self.freedraw_points[i], self.freedraw_points[i + 1])
    
    def mousePressEvent(self, event):
        if self.current_tool is None or self.pixmap_data is None:
            return
        
        self.is_drawing = True
        self.start_point = event.pos()
        
        if self.current_tool == MaskType.FREEDRAW:
            self.freedraw_points = [event.pos()]
    
    def mouseMoveEvent(self, event):
        if not self.is_drawing:
            return
        
        self.current_point = event.pos()
        
        if self.current_tool == MaskType.FREEDRAW:
            self.freedraw_points.append(event.pos())
        
        self.update()
    
    def mouseReleaseEvent(self, event):
        if not self.is_drawing or self.current_tool is None:
            return
        
        self.is_drawing = False
        self.current_point = event.pos()
        
        # Convert screen coordinates to image coordinates
        geometry = self._get_image_coordinates()
        
        if geometry is not None:
            self.mask_created.emit(geometry)
        
        # Reset drawing state
        self.start_point = None
        self.current_point = None
        self.freedraw_points = []
        self.update()
    
    def _get_image_coordinates(self):
        if self.spectrum_shape is None:
            return None
        
        pixmap_scaled = self.pixmap_data.scaled(
            self.size(), 
            Qt.KeepAspectRatio, 
            Qt.SmoothTransformation
        )
        
        offset_x = (self.width() - pixmap_scaled.width()) // 2
        offset_y = (self.height() - pixmap_scaled.height()) // 2
        
        h, w = self.spectrum_shape
        scale_x = w / pixmap_scaled.width()
        scale_y = h / pixmap_scaled.height()
        
        if self.current_tool == MaskType.RECTANGLE:
            x1 = int((self.start_point.x() - offset_x) * scale_x)
            y1 = int((self.start_point.y() - offset_y) * scale_y)
            x2 = int((self.current_point.x() - offset_x) * scale_x)
            y2 = int((self.current_point.y() - offset_y) * scale_y)
            
            x1 = max(0, min(x1, w))
            x2 = max(0, min(x2, w))
            y1 = max(0, min(y1, h))
            y2 = max(0, min(y2, h))
            
            return (x1, y1, x2, y2)
        
        elif self.current_tool == MaskType.CIRCLE:
            cx = int((self.start_point.x() - offset_x) * scale_x)
            cy = int((self.start_point.y() - offset_y) * scale_y)
            
            dx = (self.current_point.x() - self.start_point.x()) * scale_x
            dy = (self.current_point.y() - self.start_point.y()) * scale_y
            radius = int((dx**2 + dy**2)**0.5)
            
            return (cx, cy, radius)
        
        elif self.current_tool == MaskType.FREEDRAW:
            points = []
            for point in self.freedraw_points:
                x = int((point.x() - offset_x) * scale_x)
                y = int((point.y() - offset_y) * scale_y)
                if 0 <= x < w and 0 <= y < h:
                    points.append((y, x))
            return points if points else None
        
        return None