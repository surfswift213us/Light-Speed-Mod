import os
import tkinter as tk
from tkinter import filedialog, messagebox
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

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

# Utility Script Functions
def run_auto_vcpkg(module_path, pkg_name):
    if check_package_exists(pkg_name):
        log_message(f"Running auto_vcpkg.py on {module_path} with package name: {pkg_name}")
    else:
        log_message(f"Package '{pkg_name}' does not exist in vcpkg. Please check the package name.")

# Check if package exists in vcpkg using Selenium
def check_package_exists(pkg_name):
    try:
        # Set up Selenium WebDriver (you can use ChromeDriver, EdgeDriver, etc.)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")  # Run in headless mode (no GUI)
        driver = webdriver.Chrome(service=ChromeService(), options=options)

        # Navigate to vcpkg packages page
        search_url = f"https://vcpkg.io/en/packages?query={pkg_name}"
        driver.get(search_url)

        # Wait for the package cards to be visible
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "package-card"))
        )

        # Get the page source after rendering
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        # Close the driver
        driver.quit()

        # Find all package cards on the page
        package_results = soup.find_all('div', class_='package-card')

        # If no results are found, log a warning
        if not package_results:
            log_message("Warning: No package cards found on the page. The webpage might have changed.")

        # Loop through the found packages and check if our package matches
        for package in package_results:
            package_text = package.get_text(strip=True).lower()
            if pkg_name.lower() in package_text:
                log_message(f"Package '{pkg_name}' found in vcpkg.")
                return True

        log_message(f"Package '{pkg_name}' not found in vcpkg.")
        return False

    except Exception as e:
        log_message(f"Unexpected error while checking package: {str(e)}")
        return False

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
    tk.Label(recommendations_frame, text="Recommendations & Updates:", bg="black", fg="white").pack(pady=5)
    tk.Button(recommendations_frame, text="Show Recommendations", command=show_recommendations, bg="black", fg="white").pack(pady=5)

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

    # Library Variables
    fftw3_var = tk.BooleanVar()

    # Library Checkboxes
    tk.Checkbutton(lib_frame, text="FFTW3", variable=fftw3_var, bg="black", fg="white", selectcolor="green").grid(row=0, column=2, padx=10)

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

    # Module Utilities Section
    tk.Label(frame, text="Module Utilities:", bg="black", fg="white").pack(pady=10)
    module_folder_var = tk.StringVar()
    tk.Entry(frame, textvariable=module_folder_var, width=50).pack(pady=5)
    tk.Button(frame, text="Browse Module Folder", command=browse_module_folder).pack(pady=5)

    tk.Label(frame, text="Utility Scripts:", bg="black", fg="white").pack(pady=10)
    vcpkg_pkg_var = tk.StringVar()
    tk.Entry(frame, textvariable=vcpkg_pkg_var, width=30).pack(pady=5)
    tk.Button(frame, text="Run VCPKG", command=lambda: run_auto_vcpkg(module_folder_var.get(), vcpkg_pkg_var.get()), bg="black", fg="white").pack(pady=5)

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
