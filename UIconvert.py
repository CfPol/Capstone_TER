import os

# Define input and output file names
ui_file = "main.ui"
py_file = "main_ui.py"

# Convert UI to Python
os.system(f"pyuic6 -o {py_file} {ui_file}")

print(f"Conversion successful! {ui_file} → {py_file}")
