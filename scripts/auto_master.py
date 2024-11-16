import os
import subprocess
import json
from termcolor import colored
import time

# JSON file to track installed modules
TRACK_FILE = "installed_modules.json"

# ASCII art
ASCII_LOGO = """
 /$$       /$$           /$$         /$$            /$$$$$$                                      /$$       /$$      /$$  /$$$$$$        /$$
| $$      |__/          | $$        | $$           /$$__  $$                                    | $$      | $$$    /$$$ /$$__  $$      | $$
| $$       /$$  /$$$$$$ | $$$$$$$  /$$$$$$        | $$  \__/  /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$$      | $$$$  /$$$$| $$  \ $$  /$$$$$$$
| $$      | $$ /$$__  $$| $$__  $$|_  $$_/        |  $$$$$$  /$$__  $$ /$$__  $$ /$$__  $$ /$$__  $$      | $$ $$/$$ $$| $$  | $$ /$$__  $$
| $$      | $$| $$  \ $$| $$  \ $$  | $$           \____  $$| $$  \ $$| $$$$$$$$| $$$$$$$$| $$  | $$      | $$  $$$| $$| $$  | $$| $$  | $$
| $$      | $$| $$  | $$| $$  | $$  | $$ /$$       /$$  \ $$| $$  | $$| $$_____/| $$_____/| $$  | $$      | $$\  $ | $$| $$  | $$| $$  | $$
| $$$$$$$$| $$|  $$$$$$$| $$  | $$  |  $$$$/      |  $$$$$$/| $$$$$$$/|  $$$$$$$|  $$$$$$$|  $$$$$$$      | $$ \/  | $$|  $$$$$$/|  $$$$$$$
|________/|__/ \____  $$|__/  |__/   \___/         \______/ | $$____/  \_______/ \_______/ \_______/      |__/     |__/ \______/  \_______/
               /$$  \ $$                                    | $$                                                                           
              |  $$$$$$/                                    | $$                                                                           
               \______/                                     |__/                                                                           
"""

def log(message, status="INFO"):
    """Log messages with color-coded status."""
    if status == "INFO":
        print(colored(f"[INFO] {message}", "cyan"))
    elif status == "SUCCESS":
        print(colored(f"[✔] {message}", "magenta"))
    elif status == "ERROR":
        print(colored(f"[✖] {message}", "red"))

def add_library(library_name):
    """Add a library to Godot using the series of scripts."""
    print(ASCII_LOGO)
    log(f"Starting setup for library: {library_name}")

    # Step 1: Install with vcpkg
    log("Installing library with vcpkg...", "INFO")
    if run_script("auto_vcpkg.py", library_name):
        log("Library installed successfully!", "SUCCESS")
    else:
        log("Failed to install library with vcpkg.", "ERROR")
        return

    # Step 2: Generate Wrappers with SWIG
    log("Generating wrappers with SWIG...", "INFO")
    if run_script("auto_wrapper.py", library_name):
        log("Wrappers generated successfully!", "SUCCESS")
    else:
        log("Failed to generate wrappers.", "ERROR")
        return

    # Step 3: Add Godot Bindings
    log("Adding bindings to Godot...", "INFO")
    if run_script("auto_bind.py", library_name):
        log("Bindings added successfully!", "SUCCESS")
    else:
        log("Failed to add bindings.", "ERROR")
        return

    # Step 4: Final Module Setup
    log("Finalizing module setup...", "INFO")
    if run_script("auto_mod_fix.py", library_name):
        log("Module setup complete!", "SUCCESS")
    else:
        log("Failed to finalize module setup.", "ERROR")
        return

    # Step 5: Update SCsub for Include Paths
    log("Updating SCsub with include paths...", "INFO")
    if run_script("auto_update_scsub.py", library_name):
        log("SCsub updated with include paths successfully!", "SUCCESS")
    else:
        log("Failed to update SCsub.", "ERROR")
        return

    # Update tracking file
    update_track_file(library_name, action="add")
    log("Library successfully added to Godot!", "SUCCESS")
    show_completion_bar()

def remove_library(library_name):
    """Remove a library from Godot."""
    print(ASCII_LOGO)
    log(f"Removing library: {library_name}")

    # Remove the library directory and any associated files
    module_dir = os.path.join("modules", library_name)
    if os.path.exists(module_dir):
        subprocess.run(["rm", "-rf", module_dir])
        log(f"Removed directory for {library_name}", "SUCCESS")
    else:
        log(f"No directory found for {library_name}.", "ERROR")

    # Update tracking file
    update_track_file(library_name, action="remove")
    log(f"Library {library_name} successfully removed from Godot.", "SUCCESS")
    show_completion_bar()

def run_script(script_name, library_name):
    """Run a helper script with the given library name."""
    try:
        result = subprocess.run(["python", script_name, library_name], check=True)
        return result.returncode == 0
    except subprocess.CalledProcessError:
        return False

def update_track_file(library_name, action="add"):
    """Update the JSON file tracking installed libraries."""
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, "r") as f:
            track_data = json.load(f)
    else:
        track_data = {}

    if action == "add":
        track_data[library_name] = "installed"
    elif action == "remove" and library_name in track_data:
        del track_data[library_name]

    with open(TRACK_FILE, "w") as f:
        json.dump(track_data, f, indent=4)
    log("Updated tracking file.", "INFO")

def show_completion_bar():
    """Show a completion bar to indicate progress."""
    for i in range(1, 101, 10):
        time.sleep(0.1)
        print(colored(f"\rProgress: [{'=' * (i // 10)}{' ' * (10 - (i // 10))}] {i}%", "green"), end="")
    print("\n" + colored("100% Complete!", "green"))

def main():
    print(ASCII_LOGO)
    print(colored("Welcome to Light Speed Mod Manager!", "yellow"))
    print("Commands:\n  add <library_name>    - Add a new library/module\n  remove <library_name> - Remove an existing library/module\n")

    command = input(colored("Enter command: ", "yellow"))
    args = command.split()
    if len(args) < 2:
        log("Invalid command. Use `add <library_name>` or `remove <library_name>`.", "ERROR")
        return

    action, library_name = args[0], args[1]

    if action == "add":
        add_library(library_name)
    elif action == "remove":
        remove_library(library_name)
    else:
        log("Unknown command. Use `add` or `remove`.", "ERROR")

if __name__ == "__main__":
    main()
