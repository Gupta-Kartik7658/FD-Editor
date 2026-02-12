import numpy as np
from typing import List
from .mask import Mask, MaskMode


class MaskManager:
    def __init__(self):
        self.masks: List[Mask] = []
        self.current_mask: Mask = None
        self.current_mode: MaskMode = MaskMode.REMOVE
    
    def add_mask(self, mask: Mask) -> None:
        self.masks.append(mask)
        self.current_mask = mask
    
    def remove_mask(self, mask: Mask) -> None:
        if mask in self.masks:
            self.masks.remove(mask)
            if self.current_mask == mask:
                self.current_mask = None
    
    def set_mode(self, mode: MaskMode) -> None:
        self.current_mode = mode
        for mask in self.masks:
            mask.set_mode(mode)
    
    def get_masks_by_mode(self, mode: MaskMode) -> List[Mask]:
        return [m for m in self.masks if m.mode == mode]
    
    def get_combined_mask(self) -> np.ndarray:
        if not self.masks:
            return None
        
        active_masks = [m for m in self.masks if m.enabled and m.mode == self.current_mode]
        
        if not active_masks:
            return None
        
        if self.current_mode == MaskMode.REMOVE:
            combined = np.ones(self.masks[0].shape, dtype=np.float64)
            for mask in active_masks:
                combined *= mask.get_mask_matrix()
        else:  # HIGHLIGHT mode
            combined = np.zeros(self.masks[0].shape, dtype=np.float64)
            for mask in active_masks:
                mask_matrix = mask.get_mask_matrix()
                combined = np.maximum(combined, mask_matrix)
        
        return combined
    
    def clear_all(self) -> None:
        self.masks.clear()
        self.current_mask = None