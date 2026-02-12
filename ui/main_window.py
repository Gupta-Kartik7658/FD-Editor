from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QFileDialog, QSlider, QLabel)
from PySide6.QtCore import Qt
from .image_canvas import ImageCanvas
from .mask_list_panel import MaskListPanel
from core.fft_engine import FFTEngine
from core.mask_manager import MaskManager
from utils.image_utils import load_image_as_grayscale, numpy_to_qimage, normalize_for_display


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fourier Domain Image Editor")
        self.setGeometry(100, 100, 1200, 700)
        
        self.fft_engine = FFTEngine()
        self.mask_manager = MaskManager()
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        left_panel = QVBoxLayout()
        
        self.load_button = QPushButton("Load Image")
        self.load_button.clicked.connect(self.load_image)
        left_panel.addWidget(self.load_button)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.clicked.connect(self.reset_image)
        self.reset_button.setEnabled(False)
        left_panel.addWidget(self.reset_button)
        
        left_panel.addStretch()
        
        image_layout = QHBoxLayout()
        
        spatial_container = QVBoxLayout()
        spatial_container.addWidget(QLabel("Spatial Domain"))
        self.spatial_canvas = ImageCanvas()
        spatial_container.addWidget(self.spatial_canvas)
        
        freq_container = QVBoxLayout()
        freq_container.addWidget(QLabel("Frequency Domain"))
        self.freq_canvas = ImageCanvas()
        freq_container.addWidget(self.freq_canvas)
        
        image_layout.addLayout(spatial_container)
        image_layout.addLayout(freq_container)
        
        main_layout.addLayout(left_panel, 1)
        main_layout.addLayout(image_layout, 4)
    
    def load_image(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.bmp)"
        )
        if not filepath:
            return
        
        image = load_image_as_grayscale(filepath)
        self.fft_engine.compute_fft(image)
        
        self.update_displays()
        self.reset_button.setEnabled(True)
    
    def update_displays(self):
        spatial_img = normalize_for_display(self.fft_engine.original_image)
        self.spatial_canvas.set_image(numpy_to_qimage(spatial_img))
        
        log_spectrum = self.fft_engine.get_log_magnitude_spectrum()
        freq_img = normalize_for_display(log_spectrum)
        self.freq_canvas.set_image(numpy_to_qimage(freq_img))
    
    def reset_image(self):
        if self.fft_engine.original_image is not None:
            self.mask_manager.clear_all()
            self.update_displays()