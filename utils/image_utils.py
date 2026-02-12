import numpy as np
from PIL import Image
import cv2


def load_image_as_grayscale(filepath: str) -> np.ndarray:
    img = Image.open(filepath).convert('L')
    return np.array(img, dtype=np.float64)


def numpy_to_qimage(array: np.ndarray):
    from PySide6.QtGui import QImage
    
    if array.dtype != np.uint8:
        array = np.clip(array, 0, 255).astype(np.uint8)
    
    height, width = array.shape
    bytes_per_line = width
    array = np.ascontiguousarray(array)
    return QImage(array.data, width, height, bytes_per_line, QImage.Format_Grayscale8)


def normalize_for_display(array: np.ndarray) -> np.ndarray:
    array_min = array.min()
    array_max = array.max()
    if array_max - array_min == 0:
        return np.zeros_like(array, dtype=np.uint8)
    normalized = (array - array_min) / (array_max - array_min) * 255
    return normalized.astype(np.uint8)