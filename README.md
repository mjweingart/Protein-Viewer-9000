# Protein-Viewer-9000

Protein-Viewer-9000 is a lightweight Python app that fetches and displays AlphaFold-predicted protein structures in an interactive 3D viewer using 3Dmol.js from a user-entered UniProt ID.

## Features
- Input any UniProt ID (case-insensitive)
- Fetch AlphaFold-predicted 3D structures
- View in different 3D styles (cartoon, stick, etc.)
- Lightweight GUI with no console window

## Instructions
1. Launch the app
2. Enter a UniProt ID (e.g., Q15465)
3. Select the visualization style
4. Click "Submit" to view the structure

## Requirements
- Python 3.9+
- `tkinter`, `ttkbootstrap`, `py3Dmol`, `requests`, `ete3`

## Executable
An executable version is provided for convenience

To build your own using pyinstaller:

```bash
pyinstaller --onefile --hidden-import ete3 --hidden-import ttkbootstrap --noconsole main.py \
  --add-data "protein_icon.ico;." --add-data "Protein pic edited.png;."
