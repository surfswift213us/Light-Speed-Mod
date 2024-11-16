import os
import tkinter as tk
from tkinter import filedialog, messagebox
import random
from tkinter import ttk

# ASCII Art
ASCII_ART = r"""
██╗     ██╗ ██████╗ ██╗  ██╗████████╗    ███████╗██████╗ ███████╗███████╗██████╗     ███╗   ███╗ ██████╗ ██████╗ 
██║     ██║██╔════╝ ██║  ██║╚══██╔══╝    ██╔════╝██╔══██╗██╔════╝██╔════╝██╔══██╗    ████╗ ████║██╔═══██╗██╔══██╗
██║     ██║██║  ███╗███████║   ██║       ███████╗██████╔╝█████╗  █████╗  ██║  ██║    ██╔████╔██║██║   ██║██║  ██║
██║     ██║██║   ██║██╔══██║   ██║       ╚════██║██╔═══╝ ██╔══╝  ██╔══╝  ██║  ██║    ██║╚██╔╝██║██║   ██║██║  ██║
███████╗██║╚██████╔╝██║  ██║   ██║       ███████║██║     ███████╗███████╗██████╔╝    ██║ ╚═╝ ██║╚██████╔╝██████╔╝
╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝       ╚══════╝╚═╝     ╚══════╝╚══════╝╚══════╝     ╚═╝     ╚═╝ ╚═════╝ ╚═════╝ 
"""

# Placeholder functions for utilities
def install_library(lib_name, godot_path):
    log_message(f"Installing {lib_name}... (Placeholder)")

def install_godot_module(module_name, godot_path):
    log_message(f"Installing {module_name}... (Placeholder)")

def install_utility(utility_name, godot_path):
    log_message(f"Installing {utility_name}... (Placeholder)")

def run_auto_vcpkg(module_path, pkg_name):
    log_message(f"Running auto_vcpkg.py on {module_path} with package name: {pkg_name}")

def run_auto_wrapper(module_path):
    log_message(f"Running auto_wrapper.py on {module_path}")

def run_auto_binding(module_path):
    log_message(f"Running auto_binding.py on {module_path}")

def run_auto_func_gen(module_path):
    log_message(f"Running auto_func_gen.py on {module_path}")

def run_auto_scsub(module_path):
    log_message(f"Running auto_scsub.py on {module_path}")

def run_auto_reg(module_path):
    log_message(f"Running auto_reg.py on {module_path}")

def run_auto_config(module_path):
    log_message(f"Running auto_config.py on {module_path}")

def run_auto_cleanup(module_path):
    log_message(f"Running auto_cleanup.py on {module_path}")

def run_auto_hmarry(module_path):
    log_message(f"Running auto_hmarry.py on {module_path}")

# Functions to run the auto library and utility installers
def run_auto_libraries_install(godot_path):
    log_message("Running auto_libraries_install.py...")
    # Placeholder: Actual implementation to run auto_libraries_install.py
    os.system(f'python auto_libraries_install.py "{godot_path}"')

def run_auto_utilities_install(godot_path):
    log_message("Running auto_utilities_install.py...")
    # Placeholder: Actual implementation to run auto_utilities_install.py
    os.system(f'python auto_utilities_install.py "{godot_path}"')

# Create Matrix Effect
def start_matrix_effect(canvas, width, height):
    characters = "01"
    font_size = 12
    columns = width // font_size
    drops = [0 for _ in range(columns)]

    def draw():
        canvas.delete("matrix")
        for i in range(len(drops)):
            char = random.choice(characters)
            x = i * font_size
            y = drops[i] * font_size
            canvas.create_text(
                x, y, text=char, fill="green", font=("Courier", font_size), tags="matrix"
            )
            if y > height and random.random() > 0.975:
                drops[i] = 0
            drops[i] += 1
        canvas.after(50, draw)  # Redraw every 50ms

    draw()

# Log message to GUI log box
def log_message(message):
    log_box.insert(tk.END, f"{message}\n")
    log_box.yview(tk.END)

# Create GUI
def create_gui():
    def browse_godot_folder():
        path = filedialog.askdirectory(title="Select Godot Folder")
        godot_folder_var.set(path)

    def browse_module_folder():
        path = filedialog.askdirectory(title="Select Module Folder")
        module_folder_var.set(path)

    def show_about():
        messagebox.showinfo("About", "LightSpeed Mod Installer v1.0\n\nThis mod allows you to manage and install various Godot modules and utilities.")

    def install_libraries():
        godot_path = godot_folder_var.get()
        run_auto_libraries_install(godot_path)

    def install_utilities():
        godot_path = godot_folder_var.get()
        run_auto_utilities_install(godot_path)

    root = tk.Tk()
    root.title("Light Speed Mod Installer")
    root.geometry("1200x800")

    # Create Matrix Effect Canvas (Background)
    matrix_canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    matrix_canvas.pack(fill="both", expand=True)  # Make the canvas fill the entire window dynamically
    start_matrix_effect(matrix_canvas, root.winfo_screenwidth(), root.winfo_screenheight())

    # Main content frame (on top of the Matrix effect)
    frame = tk.Frame(matrix_canvas, bg="black")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # Box around ASCII Art
    art_box = tk.Frame(frame, bg="green", bd=2)  # Adding border around the ASCII art
    art_box.pack(padx=10, pady=10)
    tk.Label(art_box, text=ASCII_ART, bg="black", fg="green", font=("Courier", 12)).pack(pady=10)

    # Godot Folder Section
    tk.Label(frame, text="Select Your Godot Folder:", bg="black", fg="white").pack(pady=5)
    godot_folder_var = tk.StringVar()
    tk.Entry(frame, textvariable=godot_folder_var, width=50).pack(pady=5)
    tk.Button(frame, text="Browse", command=browse_godot_folder).pack(pady=5)

    # About Button (on the far right side)
    tk.Button(root, text="About", command=show_about, bg="black", fg="white").place(relx=0.95, rely=0.95, anchor="se")  # About button positioned to the bottom-right corner

    # LIB Section
    tk.Label(frame, text="Libraries (LIB):", bg="black", fg="white").pack(pady=10)
    lib_frame = tk.Frame(frame, bg="black")
    lib_frame.pack()
    physx_var = tk.BooleanVar()
    geometry3_var = tk.BooleanVar()
    fftw3_var = tk.BooleanVar()
    directxmath_var = tk.BooleanVar()
    tensorflow_var = tk.BooleanVar()
    tk.Checkbutton(lib_frame, text="PhysX", variable=physx_var, bg="black", fg="white", selectcolor="green").grid(row=0, column=0, padx=10)
    tk.Checkbutton(lib_frame, text="geometry3", variable=geometry3_var, bg="black", fg="white", selectcolor="green").grid(row=0, column=1, padx=10)
    tk.Checkbutton(lib_frame, text="FFTW3", variable=fftw3_var, bg="black", fg="white", selectcolor="green").grid(row=0, column=2, padx=10)
    tk.Checkbutton(lib_frame, text="DirectXMath", variable=directxmath_var, bg="black", fg="white", selectcolor="green").grid(row=0, column=3, padx=10)
    tk.Checkbutton(lib_frame, text="TensorFlow", variable=tensorflow_var, bg="black", fg="white", selectcolor="green").grid(row=0, column=4, padx=10)

    # Install Button for Libraries
    install_lib_button = tk.Button(frame, text="Install Libraries", command=install_libraries, bg="black", fg="white")
    install_lib_button.pack(pady=10)

    # Utilities Section
    tk.Label(frame, text="Utilities:", bg="black", fg="white").pack(pady=10)
    utility_frame = tk.Frame(frame, bg="black")
    utility_frame.pack()
    profiler_var = tk.BooleanVar()
    debugger_var = tk.BooleanVar()
    ls_boost_mod_var = tk.BooleanVar()
    tk.Checkbutton(utility_frame, text="Godot Profiler", variable=profiler_var, bg="black", fg="white", selectcolor="green").grid(row=0, column=0, padx=10)
    tk.Checkbutton(utility_frame, text="Godot Debugger", variable=debugger_var, bg="black", fg="white", selectcolor="green").grid(row=0, column=1, padx=10)
    tk.Checkbutton(utility_frame, text="LS_Boost_Mod", variable=ls_boost_mod_var, bg="black", fg="white", selectcolor="green").grid(row=0, column=2, padx=10)

    # Install Button for Utilities
    install_util_button = tk.Button(frame, text="Install Utilities", command=install_utilities, bg="black", fg="white")
    install_util_button.pack(pady=10)

    # Module Utilities Section
    tk.Label(frame, text="Module Utilities:", bg="black", fg="white").pack(pady=10)
    tk.Label(frame, text="Select Module Folder:", bg="black", fg="white").pack(pady=5)
    module_folder_var = tk.StringVar()
    tk.Entry(frame, textvariable=module_folder_var, width=50).pack(pady=5)
    tk.Button(frame, text="Browse", command=browse_module_folder).pack(pady=5)

    tk.Label(frame, text="Utility Scripts:", bg="black", fg="white").pack(pady=10)
    vcpkg_frame = tk.Frame(frame, bg="black")
    vcpkg_frame.pack(pady=5)
    vcpkg_pkg_var = tk.StringVar()
    tk.Entry(vcpkg_frame, textvariable=vcpkg_pkg_var, width=30).grid(row=0, column=0, padx=5)
    tk.Button(vcpkg_frame, text="Libs Name [vcpkg]", command=lambda: run_auto_vcpkg(module_folder_var.get(), vcpkg_pkg_var.get())).grid(row=0, column=1, padx=5)

    # Utility buttons arranged in a 2x4 grid
    utility_buttons_frame = tk.Frame(frame, bg="black")
    utility_buttons_frame.pack(pady=10)
    tk.Button(utility_buttons_frame, text="Wrapper", command=lambda: run_auto_wrapper(module_folder_var.get()), bg="black", fg="white").grid(row=0, column=0, padx=10, pady=5)
    tk.Button(utility_buttons_frame, text="Binding", command=lambda: run_auto_binding(module_folder_var.get()), bg="black", fg="white").grid(row=0, column=1, padx=10, pady=5)
    tk.Button(utility_buttons_frame, text="Functions", command=lambda: run_auto_func_gen(module_folder_var.get()), bg="black", fg="white").grid(row=0, column=2, padx=10, pady=5)
    tk.Button(utility_buttons_frame, text="SCsub", command=lambda: run_auto_scsub(module_folder_var.get()), bg="black", fg="white").grid(row=0, column=3, padx=10, pady=5)
    tk.Button(utility_buttons_frame, text="Register", command=lambda: run_auto_reg(module_folder_var.get()), bg="black", fg="white").grid(row=1, column=0, padx=10, pady=5)
    tk.Button(utility_buttons_frame, text="PYconfig", command=lambda: run_auto_config(module_folder_var.get()), bg="black", fg="white").grid(row=1, column=1, padx=10, pady=5)
    tk.Button(utility_buttons_frame, text="Cleanup", command=lambda: run_auto_cleanup(module_folder_var.get()), bg="black", fg="white").grid(row=1, column=2, padx=10, pady=5)
    tk.Button(utility_buttons_frame, text="HMarry", command=lambda: run_auto_hmarry(module_folder_var.get()), bg="black", fg="white").grid(row=1, column=3, padx=10, pady=5)

    # Console Log Section (on the left side with welcome message)
    global log_box
    log_frame = tk.Frame(matrix_canvas, bg="black")
    log_frame.place(relx=0, rely=0.5, anchor="w", relwidth=0.2)
    log_box = tk.Text(log_frame, height=30, width=40, bg="black", fg="green", wrap="word")
    log_box.pack(padx=10, pady=10)
    log_box.insert(tk.END, "Welcome to LightSpeed Mod Console Log...\nPreparing to go to Lightspeed...\n")
    log_box.yview(tk.END)

    root.mainloop()

if __name__ == "__main__":
    create_gui()
