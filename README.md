# Protein-Viewer-9000
This is a lightweight Python application that fetches and displays Alphafold-predicted protein structures in an interactive 3Dmol.js viewer, from an entered UniProt ID.

## Instructions
- Enter any UniProt ID (case doesn't matter)
- Select the style
- Submit

## Executable
- An executable is uploaded for convenience
- To package it up yourself using pyinstaller use the following command:
- "pyinstaller --onefile --hidden-import ete3 --hidden-import ttkbootstrap --noconsole main.py --add-data "protein_icon.ico;." --add-data "Protein pic edited.png;.""
