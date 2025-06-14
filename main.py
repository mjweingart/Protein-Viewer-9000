import requests
import tempfile
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as bootstrap
from PIL import Image, ImageTk
import os
import sys

STYLE_OPTIONS = ["cartoon", "stick", "sphere", "line", "cross"]


# Function to handle file paths in PyInstaller for icon and background pic
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    base_path = os.path.abspath(os.path.dirname(__file__))
    return os.path.join(base_path, relative_path)



# Retrieves structure from alphafold. Creates temp file with data
def get_structure(uniprot_id):
    url = f"https://alphafold.ebi.ac.uk/files/AF-{uniprot_id}-F1-model_v4.pdb"
    response = requests.get(url)

    if response.status_code == 200:
        pdb_path = os.path.join(tempfile.gettempdir(), f"{uniprot_id}.pdb")
        with open(pdb_path, "wb") as f:
            f.write(response.content)
        return pdb_path
    else:
        raise Exception(
            f"Failed to download structure: HTTP {response.status_code}\n\nPlease check that the ID you have entered is correct.")


# Opens the temp file (from get_structure()) in user browser
def open_in_browser(pdb_file_path, style_choice):
    with open(pdb_file_path, 'r') as f:
        pdb_data = f.read()

    pdb_js_str = pdb_data.replace('\\', '\\\\').replace('\n', '\\n').replace('"', '\\"')

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <script src="https://3Dmol.org/build/3Dmol-min.js"></script>
    </head>
    <body>
    <div style="width: 100vw; height: 100vh;" id="viewer"></div>
    <script>
        let element = document.getElementById("viewer");
        let config = {{ backgroundColor: "white" }};
        let viewer = $3Dmol.createViewer(element, config);
        let pdbData = "{pdb_js_str}";
        viewer.addModel(pdbData, "pdb");
        viewer.setStyle({{}}, {{ {style_choice}: {{ color: "spectrum" }} }});
        viewer.zoomTo();
        viewer.render();
    </script>
    </body>
    </html>
    """

    html_path = os.path.join(tempfile.gettempdir(), "3Dmol_viewer.html")
    with open(html_path, "w") as f:
        f.write(html)

    webbrowser.open(f"file://{html_path}")


# Submit button
def on_submit():
    uniprot_id = user_input.get().strip().upper()
    if not uniprot_id:
        messagebox.showerror("Error", "Please enter a UniProt ID.")
        return

    selected_style = style_var.get()
    try:
        pdb_path = get_structure(uniprot_id)
        open_in_browser(pdb_path, selected_style)
    except Exception as e:
        messagebox.showerror("Error", str(e))


# GUI
# main window
app = bootstrap.Window(themename="cosmo")
app.title("Protein Viewer 9000 - Ultimate Edition")
app.iconbitmap(resource_path("protein_icon.ico"))
# overall layout
frame = ttk.Frame(app, padding=20)
frame.grid(columnspan=3)
# layout of buttons etc
elements_frame = ttk.Frame(frame)
elements_frame.grid(column=1, row=0, columnspan=2, pady=10)
# uniprot # user entry
ttk.Label(elements_frame, text="Enter UniProt ID:   ").grid(column=0, row=0, sticky="e")
user_input = ttk.Entry(elements_frame, width=12)
user_input.grid(column=1, row=0, sticky="ew")
# style dropdown menu
ttk.Label(elements_frame, text="Choose style:   ").grid(column=0, row=1, pady=10, sticky="e")
style_var = tk.StringVar(value=STYLE_OPTIONS[0])
style_menu = ttk.OptionMenu(elements_frame, style_var, STYLE_OPTIONS[0], *STYLE_OPTIONS)
style_menu.grid(column=1, row=1, sticky="ew", pady=10)
style_menu.config(width=10)
# protein image
img = Image.open(resource_path("Protein pic edited.png"))
img = img.resize((100, 140), Image.Resampling.LANCZOS)
img_tk = ImageTk.PhotoImage(img)
img_label = ttk.Label(elements_frame, image=img_tk)
img_label.image = img_tk
img_label.grid(row=3, column=0, columnspan=2, pady=10)
# view structure button
view_button = bootstrap.Button(elements_frame, text="View Structure", command=on_submit, bootstyle="success-outline")
view_button.grid(row=4, column=0, columnspan=2, pady=5)


app.mainloop()