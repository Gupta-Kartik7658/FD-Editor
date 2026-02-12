from PySide6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                               QPushButton, QFileDialog, QSlider, QLabel, 
                               QButtonGroup, QGroupBox, QRadioButton)
from PySide6.QtCore import Qt
from .image_canvas import ImageCanvas
from .mask_list_panel import MaskListPanel
from core.fft_engine import FFTEngine
from core.mask_manager import MaskManager
from core.mask import MaskType, MaskMode, Mask
from utils.image_utils import load_image_as_grayscale, numpy_to_qimage, normalize_for_display


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fourier Domain Image Editor")
        self.setGeometry(100, 100, 1400, 800)
        
        self.fft_engine = FFTEngine()
        self.mask_manager = MaskManager()
        self.current_tool = None
        
        self.init_ui()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        left_panel = self.create_left_panel()
        main_layout.addWidget(left_panel, 1)
        
        center_panel = self.create_center_panel()
        main_layout.addLayout(center_panel, 5)
        
        right_panel = self.create_right_panel()
        main_layout.addWidget(right_panel, 1)
    
    def create_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        
        # File Operations Group
        file_group = QGroupBox("File Operations")
        file_layout = QVBoxLayout()
        
        self.load_button = QPushButton("📁 Load Image")
        self.load_button.setMinimumHeight(40)
        self.load_button.clicked.connect(self.load_image)
        file_layout.addWidget(self.load_button)
        
        self.save_button = QPushButton("💾 Save Result")
        self.save_button.setMinimumHeight(40)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_image)
        file_layout.addWidget(self.save_button)
        
        file_group.setLayout(file_layout)
        layout.addWidget(file_group)
        
        # Mode Selection Group
        mode_group = QGroupBox("Edit Mode")
        mode_layout = QVBoxLayout()
        
        self.mode_button_group = QButtonGroup(self)
        self.mode_button_group.setExclusive(True)
        
        self.remove_mode_btn = QRadioButton("🔴 Remove Mode")
        self.remove_mode_btn.setChecked(True)
        self.remove_mode_btn.setMinimumHeight(30)
        self.mode_button_group.addButton(self.remove_mode_btn, 0)
        mode_layout.addWidget(self.remove_mode_btn)
        
        self.highlight_mode_btn = QRadioButton("🟢 Highlight Mode")
        self.highlight_mode_btn.setMinimumHeight(30)
        self.mode_button_group.addButton(self.highlight_mode_btn, 1)
        mode_layout.addWidget(self.highlight_mode_btn)
        
        self.mode_button_group.buttonClicked.connect(self.on_mode_changed)
        
        mode_info = QLabel("Remove: Reduce amplitude\nHighlight: Keep only selected")
        mode_info.setStyleSheet("color: #666; font-size: 10px;")
        mode_info.setWordWrap(True)
        mode_layout.addWidget(mode_info)
        
        mode_group.setLayout(mode_layout)
        layout.addWidget(mode_group)
        
        # Mask Tools Group
        tools_group = QGroupBox("Masking Tools")
        tools_layout = QVBoxLayout()
        
        self.tool_button_group = QButtonGroup(self)
        self.tool_button_group.setExclusive(True)
        
        self.rect_tool_btn = QPushButton("⬜ Rectangle")
        self.rect_tool_btn.setCheckable(True)
        self.rect_tool_btn.setMinimumHeight(35)
        self.tool_button_group.addButton(self.rect_tool_btn, 0)
        tools_layout.addWidget(self.rect_tool_btn)
        
        self.circle_tool_btn = QPushButton("⭕ Circle")
        self.circle_tool_btn.setCheckable(True)
        self.circle_tool_btn.setMinimumHeight(35)
        self.tool_button_group.addButton(self.circle_tool_btn, 1)
        tools_layout.addWidget(self.circle_tool_btn)
        
        self.freedraw_tool_btn = QPushButton("✏️ Free Draw")
        self.freedraw_tool_btn.setCheckable(True)
        self.freedraw_tool_btn.setMinimumHeight(35)
        self.tool_button_group.addButton(self.freedraw_tool_btn, 2)
        tools_layout.addWidget(self.freedraw_tool_btn)
        
        self.tool_button_group.buttonClicked.connect(self.on_tool_selected)
        
        tools_group.setLayout(tools_layout)
        layout.addWidget(tools_group)
        
        # Intensity Control Group (only for Remove mode)
        self.intensity_group = QGroupBox("Mask Intensity")
        intensity_layout = QVBoxLayout()
        
        self.intensity_label = QLabel("100%")
        self.intensity_label.setAlignment(Qt.AlignCenter)
        self.intensity_label.setStyleSheet("font-size: 16px; font-weight: bold;")
        intensity_layout.addWidget(self.intensity_label)
        
        self.intensity_slider = QSlider(Qt.Horizontal)
        self.intensity_slider.setMinimum(0)
        self.intensity_slider.setMaximum(200)
        self.intensity_slider.setValue(100)
        self.intensity_slider.setTickPosition(QSlider.TicksBelow)
        self.intensity_slider.setTickInterval(25)
        self.intensity_slider.setEnabled(False)
        self.intensity_slider.valueChanged.connect(self.on_intensity_changed)
        intensity_layout.addWidget(self.intensity_slider)
        
        slider_labels = QHBoxLayout()
        slider_labels.addWidget(QLabel("0%"))
        slider_labels.addStretch()
        slider_labels.addWidget(QLabel("100%"))
        slider_labels.addStretch()
        slider_labels.addWidget(QLabel("200%"))
        intensity_layout.addLayout(slider_labels)
        
        self.intensity_group.setLayout(intensity_layout)
        layout.addWidget(self.intensity_group)
        
        # Action Buttons Group
        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout()
        
        self.clear_mask_button = QPushButton("🗑️ Delete Selected Mask")
        self.clear_mask_button.setMinimumHeight(35)
        self.clear_mask_button.setEnabled(False)
        self.clear_mask_button.clicked.connect(self.clear_selected_mask)
        actions_layout.addWidget(self.clear_mask_button)
        
        self.reset_button = QPushButton("🔄 Reset All")
        self.reset_button.setMinimumHeight(35)
        self.reset_button.setEnabled(False)
        self.reset_button.clicked.connect(self.reset_image)
        actions_layout.addWidget(self.reset_button)
        
        actions_group.setLayout(actions_layout)
        layout.addWidget(actions_group)
        
        # Status Info
        status_group = QGroupBox("Status")
        status_layout = QVBoxLayout()
        
        self.status_label = QLabel("No image loaded")
        self.status_label.setWordWrap(True)
        self.status_label.setStyleSheet("color: #666; font-size: 11px;")
        status_layout.addWidget(self.status_label)
        
        status_group.setLayout(status_layout)
        layout.addWidget(status_group)
        
        layout.addStretch()
        
        panel.setMaximumWidth(280)
        return panel
    
    def create_center_panel(self):
        center_layout = QVBoxLayout()
        center_layout.setSpacing(10)
        
        title_label = QLabel("Fourier Domain Interactive Image Editor")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 18px; font-weight: bold; padding: 10px;")
        center_layout.addWidget(title_label)
        
        image_layout = QHBoxLayout()
        image_layout.setSpacing(15)
        
        spatial_container = QVBoxLayout()
        spatial_label = QLabel("Spatial Domain")
        spatial_label.setAlignment(Qt.AlignCenter)
        spatial_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        spatial_container.addWidget(spatial_label)
        
        self.spatial_canvas = ImageCanvas()
        self.spatial_canvas.setMinimumSize(450, 450)
        spatial_container.addWidget(self.spatial_canvas)
        
        freq_container = QVBoxLayout()
        freq_label = QLabel("Frequency Domain (Log Magnitude)")
        freq_label.setAlignment(Qt.AlignCenter)
        freq_label.setStyleSheet("font-size: 14px; font-weight: bold; padding: 5px;")
        freq_container.addWidget(freq_label)
        
        self.freq_canvas = ImageCanvas()
        self.freq_canvas.setMinimumSize(450, 450)
        self.freq_canvas.tool_selected.connect(self.enable_interaction)
        self.freq_canvas.mask_created.connect(self.on_mask_created)
        freq_container.addWidget(self.freq_canvas)
        
        image_layout.addLayout(spatial_container)
        image_layout.addLayout(freq_container)
        
        center_layout.addLayout(image_layout)
        
        return center_layout
    
    def create_right_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        
        self.mask_list_panel = MaskListPanel()
        self.mask_list_panel.mask_selected.connect(self.on_mask_list_selected)
        self.mask_list_panel.mask_toggled.connect(self.on_mask_toggled)
        self.mask_list_panel.mask_deleted.connect(self.on_mask_deleted)
        layout.addWidget(self.mask_list_panel)
        
        panel.setMaximumWidth(250)
        return panel
    
    def load_image(self):
        filepath, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.jpg *.bmp *.tif *.tiff)"
        )
        if not filepath:
            return
        
        try:
            image = load_image_as_grayscale(filepath)
            self.fft_engine.compute_fft(image)
            
            self.update_displays()
            self.reset_button.setEnabled(True)
            self.save_button.setEnabled(True)
            
            h, w = image.shape
            self.status_label.setText(f"Image loaded: {w}×{h} pixels\nReady to create masks")
            
        except Exception as e:
            self.status_label.setText(f"Error loading image: {str(e)}")
    
    def save_image(self):
        if self.fft_engine.original_image is None:
            return
        
        filepath, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "PNG (*.png);;JPEG (*.jpg);;BMP (*.bmp)"
        )
        if not filepath:
            return
        
        try:
            combined_mask = self.mask_manager.get_combined_mask()
            if combined_mask is not None:
                modified_amplitude = self.fft_engine.amplitude * combined_mask
                reconstructed = self.fft_engine.reconstruct_image(modified_amplitude)
            else:
                reconstructed = self.fft_engine.original_image
            
            from PIL import Image
            result_img = normalize_for_display(reconstructed)
            Image.fromarray(result_img).save(filepath)
            
            self.status_label.setText(f"Image saved successfully")
        except Exception as e:
            self.status_label.setText(f"Error saving: {str(e)}")
    
    def update_displays(self):
        combined_mask = self.mask_manager.get_combined_mask()
        if combined_mask is not None:
            modified_amplitude = self.fft_engine.amplitude * combined_mask
            reconstructed = self.fft_engine.reconstruct_image(modified_amplitude)
            spatial_img = normalize_for_display(reconstructed)
        else:
            spatial_img = normalize_for_display(self.fft_engine.original_image)
        
        self.spatial_canvas.set_image(numpy_to_qimage(spatial_img))
        
        log_spectrum = self.fft_engine.get_log_magnitude_spectrum()
        freq_img = normalize_for_display(log_spectrum)
        self.freq_canvas.set_image(numpy_to_qimage(freq_img))
        self.freq_canvas.set_spectrum_shape(self.fft_engine.amplitude.shape)
        self.freq_canvas.set_masks(self.mask_manager.masks)
    
    def reset_image(self):
        if self.fft_engine.original_image is not None:
            self.mask_manager.clear_all()
            self.mask_list_panel.clear_masks()
            self.update_displays()
            self.status_label.setText("All masks cleared")
            self.clear_mask_button.setEnabled(False)
            self.intensity_slider.setEnabled(False)
    
    def on_mode_changed(self, button):
        if button == self.remove_mode_btn:
            self.mask_manager.set_mode(MaskMode.REMOVE)
            self.freq_canvas.set_mode(MaskMode.REMOVE)
            self.intensity_group.setEnabled(True)
            self.status_label.setText("Mode: Remove - Reduce frequency amplitudes")
        else:
            self.mask_manager.set_mode(MaskMode.HIGHLIGHT)
            self.freq_canvas.set_mode(MaskMode.HIGHLIGHT)
            self.intensity_group.setEnabled(False)
            self.status_label.setText("Mode: Highlight - Keep only selected frequencies")
        
        for mask in self.mask_manager.masks:
            self.mask_list_panel.update_mask_display(mask)
        
        self.update_displays()
    
    def on_tool_selected(self, button):
        if button == self.rect_tool_btn:
            self.current_tool = MaskType.RECTANGLE
        elif button == self.circle_tool_btn:
            self.current_tool = MaskType.CIRCLE
        elif button == self.freedraw_tool_btn:
            self.current_tool = MaskType.FREEDRAW
        
        self.freq_canvas.set_tool(self.current_tool)
        mode_name = self.mask_manager.current_mode.value
        self.status_label.setText(f"Tool: {self.current_tool.value}\nMode: {mode_name}\nDraw on frequency domain")
    
    def enable_interaction(self):
        if self.fft_engine.amplitude is not None:
            self.status_label.setText(f"Creating {self.current_tool.value} mask...")
    
    def on_mask_created(self, geometry):
        if self.fft_engine.amplitude is None:
            return
        
        mask = Mask(self.current_tool, self.fft_engine.amplitude.shape, self.mask_manager.current_mode)
        mask.set_geometry(geometry)
        
        self.mask_manager.add_mask(mask)
        self.mask_list_panel.add_mask(mask)
        
        self.update_displays()
        self.clear_mask_button.setEnabled(True)
        
        if self.mask_manager.current_mode == MaskMode.REMOVE:
            self.intensity_slider.setEnabled(True)
            self.intensity_slider.setValue(100)
        
        num_masks = len(self.mask_manager.masks)
        self.status_label.setText(f"Mask created! Total: {num_masks}")
    
    def on_intensity_changed(self, value):
        current_mask = self.mask_manager.current_mask
        if current_mask is not None and current_mask.mode == MaskMode.REMOVE:
            intensity = value / 100.0
            current_mask.set_intensity(intensity)
            
            self.intensity_label.setText(f"{value}%")
            self.update_displays()
    
    def on_mask_list_selected(self, mask):
        self.mask_manager.current_mask = mask
        
        if mask.mode == MaskMode.REMOVE:
            intensity_percent = int(mask.intensity * 100)
            self.intensity_slider.setValue(intensity_percent)
            self.intensity_slider.setEnabled(True)
        else:
            self.intensity_slider.setEnabled(False)
        
        self.clear_mask_button.setEnabled(True)
        self.status_label.setText(f"Selected: {mask.mask_type.value} ({mask.mode.value})")
    
    def on_mask_toggled(self, mask, enabled):
        mask.enabled = enabled
        self.update_displays()
    
    def on_mask_deleted(self, mask):
        self.mask_manager.remove_mask(mask)
        self.mask_list_panel.remove_mask(mask)
        self.update_displays()
        
        if not self.mask_manager.masks:
            self.clear_mask_button.setEnabled(False)
            self.intensity_slider.setEnabled(False)
        
        self.status_label.setText("Mask deleted")
    
    def clear_selected_mask(self):
        current_mask = self.mask_manager.current_mask
        if current_mask is not None:
            self.on_mask_deleted(current_mask)