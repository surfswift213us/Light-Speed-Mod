import os
import tkinter as tk
from tkinter import filedialog, messagebox
import random
import subprocess

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
    if check_package_exists(pkg_name):
        log_message(f"Running auto_vcpkg.py on {module_path} with package name: {pkg_name}")
    else:
        log_message(f"Package '{pkg_name}' does not exist in vcpkg. Please check the package name.")

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

def run_auto_libraries_install(godot_path):
    log_message("Running auto_libraries_install.py...")
    os.system(f'python auto_libraries_install.py "{godot_path}"')

def run_auto_utilities_install(godot_path):
    log_message("Running auto_utilities_install.py...")
    os.system(f'python auto_utilities_install.py "{godot_path}"')

# Search for Package in vcpkg using subprocess
def search_package():
    package_name = vcpkg_pkg_var.get().strip()
    vcpkg_root = "C:/Users/MainFrame/Desktop/ls_mod/Light Speed Mod/vcpkg"

    if not package_name:
        log_message("Error: No package name provided!")
        return

    try:
        command = [
            'C:/Users/MainFrame/Desktop/ls_mod/Light Speed Mod/vcpkg/vcpkg.exe',
            'search', package_name,
            '--vcpkg-root', vcpkg_root
        ]
        result = subprocess.run(command, capture_output=True, text=True, check=True)

        if result.stdout:
            log_message(f"Search results for '{package_name}':\n{result.stdout}")
        else:
            log_message(f"No results found for '{package_name}'")

    except subprocess.CalledProcessError as e:
        log_message(f"Error occurred while searching for '{package_name}': {e.stderr}")
    except FileNotFoundError:
        messagebox.showerror("Error", "vcpkg executable not found. Please ensure vcpkg is installed in the correct directory.")

# Recommendations message
def show_recommendations():
    message = """Recommendations:
    1. Upgrade PhysX to the latest version for better GPU support.
    2. Consider using Eigen3 for advanced mathematical computations.
    3. Use Zylann's Godot Voxel for terrain generation.
    4. Upgrade SQLite to v5.0 for better performance.
    5. Test J.E.N.O.V.A for AI-based level generation."""
    log_message(message)
    messagebox.showinfo("Recommendations", message)

# Log message to GUI log box
def log_message(message):
    log_box.insert(tk.END, f"{message}\n")
    log_box.yview(tk.END)

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
        canvas.after(50, draw)

    draw()

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

    root = tk.Tk()
    root.title("Light Speed Mod Installer")
    root.geometry("1200x800")

    # Create Matrix Effect Canvas (Background)
    matrix_canvas = tk.Canvas(root, bg="black", highlightthickness=0)
    matrix_canvas.pack(fill="both", expand=True)
    start_matrix_effect(matrix_canvas, root.winfo_screenwidth(), root.winfo_screenheight())

    # Recommendations & Updates Section (Top Right)
    recommendations_frame = tk.Frame(matrix_canvas, bg="black")
    recommendations_frame.place(relx=0.95, rely=0.05, anchor="ne")
    tk.Label(recommendations_frame, text=" News &  Updates:", bg="black", fg="white").pack(pady=5)
    tk.Button(recommendations_frame, text="Expand", command=show_recommendations, bg="black", fg="white").pack(pady=5)

    # Main content frame
    frame = tk.Frame(matrix_canvas, bg="black")
    frame.place(relx=0.5, rely=0.5, anchor="center")

    # ASCII Art
    art_box = tk.Frame(frame, bg="green", bd=2)
    art_box.pack(padx=10, pady=10)
    tk.Label(art_box, text=ASCII_ART, bg="black", fg="green", font=("Courier", 12)).pack(pady=10)

    # Godot Folder Section
    tk.Label(frame, text="Select Your Godot Folder:", bg="black", fg="white").pack(pady=5)
    godot_folder_var = tk.StringVar()
    tk.Entry(frame, textvariable=godot_folder_var, width=50).pack(pady=5)
    tk.Button(frame, text="Browse", command=browse_godot_folder).pack(pady=5)

    # Libraries Section
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

    # Install Libraries Button
    def install_libraries():
        godot_path = godot_folder_var.get()
        if not godot_path:
            log_message("Error: No Godot path selected!")
            messagebox.showerror("Error", "Please select a valid Godot folder before installing.")
            return
        # Run the script for library installation
        run_auto_libraries_install(godot_path)
        log_message("Library installation completed.")

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

    # Install Utilities Button
    install_util_button = tk.Button(frame, text="Install Utilities", command=lambda: run_auto_utilities_install(godot_folder_var.get()), bg="black", fg="white")
    install_util_button.pack(pady=10)

    # Module Utilities Section
    tk.Label(frame, text="Module Utilities:", bg="black", fg="white").pack(pady=10)
    module_folder_var = tk.StringVar()
    tk.Entry(frame, textvariable=module_folder_var, width=50).pack(pady=5)
    tk.Button(frame, text="Browse Module Folder", command=browse_module_folder).pack(pady=5)

    # Search Package Button
    tk.Label(frame, text="Utility Scripts:", bg="black", fg="white").pack(pady=10)
    global vcpkg_pkg_var
    vcpkg_pkg_var = tk.StringVar()
    tk.Entry(frame, textvariable=vcpkg_pkg_var, width=30).pack(pady=5)
    tk.Button(frame, text="Search Package", command=search_package, bg="black", fg="white").pack(pady=5)
    tk.Button(frame, text="Run VCPKG", command=lambda: run_auto_vcpkg(module_folder_var.get(), vcpkg_pkg_var.get()), bg="black", fg="white").pack(pady=5)

    # Utility buttons arranged in a grid
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

    # Console Log Section
    global log_box
    log_frame = tk.Frame(matrix_canvas, bg="black")
    log_frame.place(relx=0, rely=0.5, anchor="w", relwidth=0.2)
    log_box = tk.Text(log_frame, height=30, width=40, bg="black", fg="green", wrap="word")
    log_box.pack(padx=10, pady=10)
    log_box.insert(tk.END, "Welcome to LightSpeed Mod Console Log...\nPreparing to go to Lightspeed...\n")
    log_box.yview(tk.END)

    # About Button (Bottom Right Corner)
    tk.Button(root, text="About", command=show_about, bg="black", fg="white").place(relx=0.95, rely=0.95, anchor="se")

    root.mainloop()

if __name__ == "__main__":
    create_gui()
