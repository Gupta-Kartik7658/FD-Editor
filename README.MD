# 📘 SOFTWARE REQUIREMENTS SPECIFICATION (SRS)

# **Fourier Domain Interactive Image Editor (FD-Editor v2)**

*A Multi-Mask, Real-Time Frequency Amplitude Editing System*

---

# 1. Introduction

## 1.1 Purpose

This document specifies the requirements for the **Fourier Domain Interactive Image Editor (FD-Editor)**.

The system allows users to:

* Upload an image
* View spatial and frequency domain representations
* Interactively edit the amplitude spectrum
* Apply multiple masks
* Modify frequency amplitudes in real-time
* Observe immediate spatial-domain reconstruction

The system is fully UI-driven with **no manual parameter entry**.

---

## 1.2 Scope

Unlike traditional filtering systems, this application:

* Allows direct amplitude manipulation of selected frequency regions
* Supports multiple overlapping masks
* Supports Photoshop-style selection tools
* Applies real-time inverse FFT reconstruction

This is not limited to binary masking.
Users can assign intensity scaling interactively.

---

# 2. Overall System Description

---

## 2.1 Product Perspective

The system is a standalone desktop application built using:

* Python
* PySide6
* NumPy
* OpenCV

Architecture:

```
UI Layer
   ↓
Mask Management Layer
   ↓
Frequency Editing Engine
   ↓
Inverse FFT Reconstruction
```

---

# 3. Core Functional Model

Let:

[
F(u,v) = A(u,v)e^{j\phi(u,v)}
]

Where:

* ( A(u,v) ) = amplitude
* ( \phi(u,v) ) = phase

Your system modifies:

[
A'(u,v)
]

while keeping phase intact unless extended.

Reconstruction:

[
f'(x,y) = \mathcal{F}^{-1}(A'(u,v)e^{j\phi(u,v)})
]

This ensures realistic image reconstruction.

---

# 4. Functional Requirements

---

# 4.1 Image Upload

* FR1.1 System shall allow image upload via file dialog.
* FR1.2 Supported formats: JPG, PNG, BMP.
* FR1.3 Image shall automatically convert to grayscale.
* FR1.4 FFT shall compute automatically.
* FR1.5 Log magnitude spectrum shall display.

---

# 4.2 Dual View Display

* FR2.1 Spatial image displayed on left.
* FR2.2 Frequency amplitude spectrum displayed on right.
* FR2.3 FFT shall be shifted (DC centered).
* FR2.4 Frequency display shall support overlay rendering.

---

# 4.3 Masking Tools (Photoshop-Style)

The system shall support:

## 1️⃣ Rectangle Mask Tool

* Click-drag rectangular selection.

## 2️⃣ Circle Mask Tool

* Click center, drag to set radius.

## 3️⃣ Free Draw Mask Tool

* Mouse painting selection.
* Continuous brush-based mask creation.

---

### Mask Requirements

* FR3.1 Masks shall be created via mouse interaction.
* FR3.2 No numeric input fields allowed.
* FR3.3 Masks shall visually overlay frequency image.
* FR3.4 Masks shall be editable after creation.
* FR3.5 Masks shall automatically mirror for FFT symmetry.
* FR3.6 Multiple masks shall be supported simultaneously.
* FR3.7 Each mask shall have independent intensity control.

---

# 4.4 Multiple Mask System

The system shall allow:

* FR4.1 Creation of multiple masks.
* FR4.2 Each mask stored as a separate layer.
* FR4.3 Masks may overlap.
* FR4.4 Combined mask effect shall be cumulative.
* FR4.5 User shall enable/disable masks.
* FR4.6 User shall delete individual masks.
* FR4.7 Mask stacking order shall not break reconstruction.

Mathematically:

[
A'(u,v) = A(u,v) \cdot \prod_{i=1}^{n} M_i(u,v)
]

Where:

* ( M_i(u,v) ) = mask i effect

---

# 4.5 Amplitude Editing Behavior

When a mask is selected:

* User adjusts intensity using slider
* Slider modifies amplitude scaling

Slider Range:

* 0% → zero amplitude
* 100% → original
* 200% → amplified

Formula:

[
A'(u,v) = \alpha_i A(u,v)
]

No numeric entry required.

---

# 4.6 Real-Time Reconstruction

* FR5.1 Spatial image shall update in real-time.
* FR5.2 Update latency shall be < 200ms for 512×512 images.
* FR5.3 Live preview toggle shall be available.

---

# 4.7 Mask Softness (Optional Enhancement)

Gaussian edge smoothing:

[
M(u,v) = e^{-\frac{d^2}{2\sigma^2}}
]

Controlled via softness slider.

No typing allowed.

---

# 4.8 Symmetry Handling

* FR6.1 System shall enforce conjugate symmetry automatically.
* FR6.2 Selected regions shall be mirrored.
* FR6.3 User shall not manually manage symmetry.

---

# 4.9 Reset and Save

* FR7.1 Reset button restores original FFT.
* FR7.2 Save button exports reconstructed image.
* FR7.3 Clear mask removes selected mask only.

---

# 5. Non-Functional Requirements

---

## 5.1 Performance

* NFR1 FFT computed only once.
* NFR2 Only amplitude modified after initial FFT.
* NFR3 Inverse FFT optimized using NumPy vectorization.
* NFR4 UI must remain responsive.

---

## 5.2 Usability

* NFR5 No text parameter fields.
* NFR6 All controls via UI widgets.
* NFR7 Interface intuitive and visual.

---

## 5.3 Reliability

* NFR8 System shall handle overlapping masks correctly.
* NFR9 Invalid selections shall not crash program.

---

## 5.4 Maintainability

* NFR10 Separate mask management from FFT engine.
* NFR11 Modular architecture.

---

# 6. System Architecture

---

## 6.1 Modules

### 1. UI Module

* Buttons
* Sliders
* Canvas
* Mask list panel

### 2. Mask Manager

* Stores mask layers
* Applies intensity
* Combines masks

### 3. FFT Engine

* Compute FFT
* Extract amplitude & phase
* Reconstruct modified image

### 4. Rendering Engine

* Convert arrays to displayable images
* Update views

---

# 7. Acceptance Criteria

The system is accepted if:

* Multiple masks can be applied
* Rectangle, Circle, Free Draw tools function correctly
* Intensity slider changes amplitude in real time
* Spatial image updates instantly
* No text-based parameter entry exists
* System maintains symmetry
* Overlapping masks behave correctly

---

# 8. Future Extensions

* Phase editing mode
* Color channel frequency editing
* Undo/Redo stack
* Mask opacity blending
* GPU acceleration

---

# 9. Conclusion

The FD-Editor v2 is a real-time, multi-mask, frequency amplitude editing system.

Unlike simple filtering tools, this system enables:

* Direct amplitude manipulation
* Photoshop-style masking
* Layered frequency editing
* Interactive reconstruction
* Pure UI-based operation

It integrates:

* Fourier Transform theory
* Software engineering
* UI/UX design
* Real-time numerical computation

This qualifies as an advanced image processing and interactive systems project.

---