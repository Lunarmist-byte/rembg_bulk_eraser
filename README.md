# rembg-bulk-eraser

A fast, simple GUI app to bulk remove backgrounds from images. Built with `customtkinter` and `rembg`.

## Features
- **Bulk Processing:** Just select an input folder and an output folder. Handles `.png`, `.jpg`, `.jpeg`, and `.webp` files.
- **Hardware Acceleration:** Automatically checks for an NVIDIA GPU and sets up `onnxruntime-gpu` for much faster processing. Falls back to CPU if no GPU is found.
- **Clean UI:** No-nonsense dark mode interface with a progress tracker.

## Quick Start

1. Make sure you have Python installed.
2. Double-click `run.bat`.

The script handles the rest: it creates a virtual environment, checks your hardware, installs the right dependencies, and launches the app.

## Manual Run (if you prefer)
If you don't want to use the batch script, you can run it manually:

```bash
python -m venv venv
venv\Scripts\activate
python setup_env.py
python main.py
```

## Made by Lunarmist-byte
- [GitHub](https://github.com/Lunarmist-byte)
- [LinkedIn](https://www.linkedin.com/in/amal-s-kumar-ba69a1290/)
