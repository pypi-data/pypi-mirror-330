# PyTools

PyTools is a collection of utility functions for automation, OCR, mouse interactions, and text manipulation.

## Installation
```
pip install pytoolsx
```

## Features
- Email sending
- Mouse movement and automation
- OCR (Optical Character Recognition)
- Screenshot capturing
- Text and list manipulation utilities
- Audio volume control

## Usage
```python
import pytools as pt

pt.send_mail("Subject", "Body", "receiver@example.com")
pt.moveClick(100, 200)
coords = pt.findOnPage("Target Text")
print(coords)
```

## Dependencies
- `pillow`
- `pytesseract`
- `pynput`
- `pyautogui`
- `beepy`
- `pycaw`
- `comtypes`

## License
This project is licensed under the MIT License.