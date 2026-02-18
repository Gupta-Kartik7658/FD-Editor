# Fourier Domain Interactive Image Editor (FD-Editor)

A real-time frequency-domain image editing application that allows direct manipulation of image frequency components through an intuitive visual interface.

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![PySide6](https://img.shields.io/badge/PySide6-6.6.1-green)
![License](https://img.shields.io/badge/license-MIT-blue)

---

# Overview

FD-Editor enables users to interactively edit images in the frequency domain by creating masks on the Fourier transform representation. Unlike traditional image filters, this application provides direct control over frequency amplitudes with real-time spatial domain reconstruction.

---

# Key Features

## Dual-Domain Visualization

- **Spatial Domain**: Original / reconstructed grayscale image
- **Frequency Domain**: Log-scale magnitude spectrum with DC component centered

## Interactive Masking Tools

- **Rectangle Tool**: Click and drag to select rectangular frequency regions
- **Circle Tool**: Click center and drag to define circular regions
- **Free Draw Tool**: Paint custom frequency selections

## Two Editing Modes

### 1. Remove Mode

- Reduces amplitude in selected frequency regions
- Adjustable intensity (0–200%)
- Perfect for frequency filtering and noise reduction

### 2. Highlight Mode

- Keeps only selected frequencies, zeros out everything else
- Ideal for frequency isolation and analysis

## Advanced Mask Management

- Multiple overlapping masks
- Layer system (enable/disable individual masks)
- Independent intensity control per mask
- Automatic conjugate symmetry enforcement (real-valued output)
- Persistent visual overlay on frequency canvas

## Real-Time Processing

- Instant spatial domain updates (<200 ms for 512×512 images)
- FFT computed once and reused
- Fully vectorized NumPy operations

---

# Installation

### Prerequisites

- Python 3.8+
- pip

### 1. Clone Repository

```bash
git clone <https://github.com/yourusername/fd-editor.git>
cd fd-editor 
```

### 2. Create Virtual Environment (Optional)

```bash
python -m venv <venv_name>
.\<venv_name>\Scripts\activate #On Windows
source /<venv_name>/bin/activate #On Linux/MacOS
```

### 3. Install all the dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the main file

```bash
python main.py
```

---

## Supported Formats

**Input**: JPG, PNG, BMP (grayscale conversion)

**Output**: PNG, JPG, BMP

---

## System Requirements

- Windows / macOS / Linux
- 4GB RAM minimum (8GB recommended)
- 1400×800 display minimum

---

## Future Enhancements

- Phase editing mode
- Color image support
- Undo / Redo
- Mask template library
- GPU acceleration
- Batch processing
- Export mask configurations

---

## License

Licensed under the MIT License.

