import os
import importlib.util
import customtkinter as ctk

# Create the main window
root = ctk.CTk()
root.title("Simulation")
root.geometry("800x500")
root.configure(bg="black")

# Excluded folders
excluded_folders = {".git", "venv", "child_"}

# Get the list of folders dynamically
current_path = os.getcwd()
folders = [f for f in os.listdir(current_path) if os.path.isdir(f) and f not in excluded_folders]

# Store paths to child scripts
child_script_paths = {}

# Scan for child scripts in each folder
for folder in folders:
    folder_path = os.path.join(current_path, folder)
    # Find a Python file inside the folder
    py_files = [f for f in os.listdir(folder_path) if f.endswith(".py") and f != "__init__.py"]
    if py_files:
        script_name = py_files[0]  # Take the first Python file
        script_path = os.path.join(folder_path, script_name)
        # Store the path only, don't import yet
        child_script_paths[folder] = script_path

# Function to open a child window
def open_child(folder):
    if folder in child_script_paths:
        script_path = child_script_paths[folder]
        # Dynamically import the child module now
        module_name = f"{folder}_{os.path.basename(script_path)[:-3]}"
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Hide parent window
        root.withdraw()
        
        # Call the open_window() function from the child
        if hasattr(module, "open_window"):
            module.open_window(root)

# Define grid settings
columns = 4  # Fixed number of columns
rows = (len(folders) // columns) + (1 if len(folders) % columns else 0)  # Calculate required rows

# Configure grid layout for equal spacing
for i in range(rows):
    root.rowconfigure(i, weight=1, uniform="row")
for j in range(columns):
    root.columnconfigure(j, weight=1, uniform="col")

# Create buttons dynamically for each folder
for index, folder_name in enumerate(folders):
    row = index // columns
    col = index % columns
    button = ctk.CTkButton(
        root, 
        text=folder_name, 
        fg_color="gray", 
        corner_radius=5,
        command=lambda folder=folder_name: open_child(folder)
    )
    button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

# Run the application
root.mainloop()