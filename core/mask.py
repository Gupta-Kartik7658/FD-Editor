import numpy as np
from enum import Enum
from typing import Tuple, List


class MaskType(Enum):
    RECTANGLE = "Rectangle"
    CIRCLE = "Circle"
    FREEDRAW = "Free Draw"


class Mask:
    def __init__(self, mask_type: MaskType, shape: Tuple[int, int]):
        self.mask_type = mask_type
        self.shape = shape
        self.intensity = 1.0
        self.enabled = True
        self.geometry = None
        self.mask_matrix: np.ndarray = None
        
    def set_geometry(self, geometry) -> None:
        self.geometry = geometry
        self._generate_mask()
    
    def set_intensity(self, value: float) -> None:
        self.intensity = value
    
    def _generate_mask(self) -> None:
        h, w = self.shape
        self.mask_matrix = np.ones((h, w), dtype=np.float64)
        
        if self.geometry is None:
            return
        
        if self.mask_type == MaskType.RECTANGLE:
            x1, y1, x2, y2 = self.geometry
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)
            self.mask_matrix[y1:y2, x1:x2] = self.intensity
            
        elif self.mask_type == MaskType.CIRCLE:
            cx, cy, radius = self.geometry
            y, x = np.ogrid[:h, :w]
            mask_circle = (x - cx)**2 + (y - cy)**2 <= radius**2
            self.mask_matrix[mask_circle] = self.intensity
            
        elif self.mask_type == MaskType.FREEDRAW:
            points = self.geometry
            for y, x in points:
                if 0 <= y < h and 0 <= x < w:
                    self.mask_matrix[y, x] = self.intensity
        
        self._apply_symmetry()
    
    def _apply_symmetry(self) -> None:
        h, w = self.shape
        cy, cx = h // 2, w // 2
        
        for y in range(h):
            for x in range(w):
                if self.mask_matrix[y, x] != 1.0:
                    mirror_y = 2 * cy - y
                    mirror_x = 2 * cx - x
                    if 0 <= mirror_y < h and 0 <= mirror_x < w:
                        self.mask_matrix[mirror_y, mirror_x] = self.mask_matrix[y, x]
    
    def get_mask_matrix(self) -> np.ndarray:
        if not self.enabled or self.mask_matrix is None:
            return np.ones(self.shape, dtype=np.float64)
        return self.mask_matrix