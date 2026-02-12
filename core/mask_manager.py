import numpy as np
from typing import List
from .mask import Mask


class MaskManager:
    def __init__(self):
        self.masks: List[Mask] = []
        self.current_mask: Mask = None
    
    def add_mask(self, mask: Mask) -> None:
        self.masks.append(mask)
        self.current_mask = mask
    
    def remove_mask(self, mask: Mask) -> None:
        if mask in self.masks:
            self.masks.remove(mask)
            if self.current_mask == mask:
                self.current_mask = None
    
    def get_combined_mask(self) -> np.ndarray:
        if not self.masks:
            return None
        
        combined = np.ones(self.masks[0].shape, dtype=np.float64)
        for mask in self.masks:
            if mask.enabled:
                combined *= mask.get_mask_matrix()
        return combined
    
    def clear_all(self) -> None:
        self.masks.clear()
        self.current_mask = None