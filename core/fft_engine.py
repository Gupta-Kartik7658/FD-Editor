import numpy as np
from typing import Tuple


class FFTEngine:
    def __init__(self):
        self.original_image: np.ndarray = None
        self.fft_shifted: np.ndarray = None
        self.amplitude: np.ndarray = None
        self.phase: np.ndarray = None
        
    def compute_fft(self, image: np.ndarray) -> None:
        self.original_image = image.copy()
        fft = np.fft.fft2(image)
        self.fft_shifted = np.fft.fftshift(fft)
        self.amplitude = np.abs(self.fft_shifted)
        self.phase = np.angle(self.fft_shifted)
    
    def get_log_magnitude_spectrum(self) -> np.ndarray:
        if self.amplitude is None:
            return None
        return np.log1p(self.amplitude)
    
    def reconstruct_image(self, modified_amplitude: np.ndarray) -> np.ndarray:
        modified_fft = modified_amplitude * np.exp(1j * self.phase)
        fft_ishifted = np.fft.ifftshift(modified_fft)
        reconstructed = np.fft.ifft2(fft_ishifted)
        return np.real(reconstructed)
    
    def reset(self) -> np.ndarray:
        return self.original_image.copy()