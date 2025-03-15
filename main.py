import os
import importlib.util
import customtkinter as ctk

# Create the main window
root = ctk.CTk()
root.title("Simulation")
root.geometry("800x500")
root.configure(bg="black")

# Excluded folders
excluded_folders = {".git", "venv", "child_","Simulation_web" }

# Get the list of folders dynamically
current_path = os.getcwd()
folders = [f for f in os.listdir(current_path) if os.path.isdir(f) and f not in excluded_folders]

# Store paths to child scripts
child_script_paths = {}

# Scan for child scripts in each folder
for folder in folders:
    folder_path = os.path.join(current_path, folder)
    py_files = [f for f in os.listdir(folder_path) if f.endswith(".py") and f != "__init__.py"]
    if py_files:
        script_name = py_files[0]  # Take the first Python file
        script_path = os.path.join(folder_path, script_name)
        child_script_paths[folder] = script_path

# Function to open a child window
def open_child(folder):
    if folder in child_script_paths:
        script_path = child_script_paths[folder]
        module_name = f"{folder}_{os.path.basename(script_path)[:-3]}"
        spec = importlib.util.spec_from_file_location(module_name, script_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        root.withdraw()  # Hide parent window
        
        if hasattr(module, "open_window"):
            module.open_window(root)

# Scrollable frame for buttons (if needed)
frame = ctk.CTkScrollableFrame(root, width=780, height=250)  # Half of window height
frame.pack(pady=10, padx=10, fill="both", expand=True)

columns = 4  # Fixed number of columns

# Configure grid layout
for i in range(columns):
    frame.columnconfigure(i, weight=1, uniform="col")

button_height = 250  # Half of window height

# Create buttons dynamically inside the grid
for index, folder_name in enumerate(folders):
    row = index // columns
    col = index % columns
    button = ctk.CTkButton(
        frame, 
        text=folder_name, 
        fg_color=("gray75", "gray20"),  
        hover_color=("gray60", "gray10"),  
        text_color="white",  
        corner_radius=5,
        border_width=1,
        border_color="black",
        height=button_height,  # Fixed height
        anchor="center",  # Center text
        command=lambda folder=folder_name: open_child(folder)
    )
    button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

# Run the application
root.mainloop()
