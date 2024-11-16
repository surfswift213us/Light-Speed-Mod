import os
import subprocess
import sys
import shutil

# Set to the actual paths on your system
VCPKG_PATH = "C:\\Users\\MainFrame\\Mirror\\Pictures\\LightSpeed_GoDot_4\\vcpkg\\vcpkg.exe"  # Full path to vcpkg executable
GODOT_MASTER_PATH = "C:\\Users\\MainFrame\\Mirror\\Pictures\\LightSpeed_GoDot_4"
TRIPLET = "x64-windows"  # Modify as needed, e.g., x64-linux

# Initialize checklist to keep track of completed steps
checklist = []

def print_and_log(message):
    """Helper function to print and log the checklist message."""
    print(message)
    checklist.append(message)  # Add each step to the checklist
    with open("mod_check_log.txt", "a") as log_file:
        log_file.write(message + "\n")

def install_vcpkg_package(package_name):
    print_and_log(f"1. Checking and installing {package_name} with vcpkg...")
    
    # Check if the package is already installed
    try:
        result = subprocess.run([VCPKG_PATH, 'list'], capture_output=True, text=True, check=True)
        if package_name in result.stdout:
            print_and_log(f"{package_name} is already installed. Skipping installation.")
            return
    except FileNotFoundError as e:
        print_and_log(f"FileNotFoundError: {e}")
        sys.exit(1)
    except subprocess.CalledProcessError as e:
        print_and_log(f"Error checking installed packages: {e}")
        sys.exit(1)

    # Install the package using vcpkg
    try:
        subprocess.run([VCPKG_PATH, 'install', package_name], check=True)
        print_and_log(f"Successfully installed {package_name} with vcpkg.")
    except subprocess.CalledProcessError as e:
        print_and_log(f"Failed to install {package_name} with vcpkg. Error: {e}")
        sys.exit(1)

def setup_module_directory(module_name):
    print_and_log("2. Setting up module directory and subdirectories...")
    
    # Create the main module directory
    module_dir = os.path.join(GODOT_MASTER_PATH, "modules", module_name)
    os.makedirs(module_dir, exist_ok=True)
    print_and_log(f"Module directory created at: {module_dir}")

    # Create additional directories: class, doc_classes, icons, and tests
    subdirs = ["class", "doc_classes", "icons", "tests"]
    for subdir in subdirs:
        os.makedirs(os.path.join(module_dir, subdir), exist_ok=True)
        print_and_log(f"Created {subdir} directory.")

    # Prepare default files with correct naming
    header_filename = f"register_types_{module_name}.h"
    cpp_filename = f"register_types_{module_name}.cpp"
    
    # Create placeholder config.py (will update at end of script)
    with open(os.path.join(module_dir, "config.py"), "w") as f:
        f.write("# Placeholder for configuration, will update at the end\n")

    # Create register_types_<module_name>.cpp with dynamic naming
    with open(os.path.join(module_dir, cpp_filename), "w") as f:
        f.write(f"#include \"{header_filename}\"\n")
        f.write("#include \"core/object/class_db.h\"\n\n")
        f.write(f"void initialize_{module_name}_module(ModuleInitializationLevel p_level) {{\n")
        f.write("    if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {\n")
        f.write("        return;\n")
        f.write("    }\n")
        f.write("    // Register classes and functions here\n")
        f.write("}\n\n")
        f.write(f"void uninitialize_{module_name}_module(ModuleInitializationLevel p_level) {{\n")
        f.write("    if (p_level != MODULE_INITIALIZATION_LEVEL_SCENE) {\n")
        f.write("        return;\n")
        f.write("    }\n")
        f.write("    // Unregister classes and functions here\n")
        f.write("}\n")

    # Create register_types_<module_name>.h with dynamic naming
    with open(os.path.join(module_dir, header_filename), "w") as f:
        f.write(f"#ifndef {module_name.upper()}_REGISTER_TYPES_H\n")
        f.write(f"#define {module_name.upper()}_REGISTER_TYPES_H\n\n")
        f.write("#include \"modules/register_module_types.h\"\n\n")
        f.write(f"void initialize_{module_name}_module(ModuleInitializationLevel p_level);\n")
        f.write(f"void uninitialize_{module_name}_module(ModuleInitializationLevel p_level);\n\n")
        f.write(f"#endif // {module_name.upper()}_REGISTER_TYPES_H\n")

    print_and_log(f"Module directory and registration files ({header_filename}, {cpp_filename}) set up successfully.")
    return module_dir

def create_placeholder_files(module_dir):
    """Creates placeholder files in icons, tests, and doc_classes directories."""

    # Create a placeholder icon
    icon_path = os.path.join(module_dir, "icons", "icon_placeholder.svg")
    with open(icon_path, "w") as f:
        f.write("<svg xmlns='http://www.w3.org/2000/svg' width='100' height='100'>\n")
        f.write("  <rect width='100' height='100' style='fill:blue'/>\n")
        f.write("</svg>\n")
    print_and_log("Created placeholder icon in icons directory.")

    # Create a sample documentation file
    doc_path = os.path.join(module_dir, "doc_classes", "SampleClass.xml")
    with open(doc_path, "w") as f:
        f.write("<class>\n")
        f.write("  <name>SampleClass</name>\n")
        f.write("  <brief_description>This is a sample class for documentation.</brief_description>\n")
        f.write("</class>\n")
    print_and_log("Created sample documentation file in doc_classes directory.")

    # Create a simple unit test in tests directory
    test_path = os.path.join(module_dir, "tests", "test_sample.h")
    with open(test_path, "w") as f:
        f.write("#ifndef TEST_SAMPLE_H\n")
        f.write("#define TEST_SAMPLE_H\n\n")
        f.write("#include \"tests/test_macros.h\"\n\n")
        f.write("namespace TestSample {\n")
        f.write("    TEST_CASE(\"[Modules][Sample] Sample Test\") {\n")
        f.write("        CHECK(true);\n")
        f.write("    }\n")
        f.write("}\n\n")
        f.write("#endif // TEST_SAMPLE_H\n")
    print_and_log("Created sample unit test in tests directory.")

def copy_vcpkg_files(package_name, module_dir):
    print_and_log("3. Copying vcpkg files...")

    # Path to the vcpkg installed package
    vcpkg_dir = os.path.dirname(VCPKG_PATH)
    package_path = os.path.join(vcpkg_dir, "installed", TRIPLET)

    # Directories to copy
    source_include = os.path.join(package_path, "include", package_name)
    source_lib = os.path.join(package_path, "lib")
    source_bin = os.path.join(package_path, "bin")

    # Destination directories in the module
    dest_include = os.path.join(module_dir, "include")
    dest_lib = os.path.join(module_dir, "lib")
    dest_bin = os.path.join(module_dir, "bin")

    # Copy include files for the specific package only
    if os.path.exists(source_include):
        shutil.copytree(source_include, dest_include, dirs_exist_ok=True)
        print_and_log(f"Copied include files for {package_name} to {dest_include}")

    # Copy library files and create Godot-specific names
    if os.path.exists(source_lib):
        os.makedirs(dest_lib, exist_ok=True)
        for lib_file in os.listdir(source_lib):
            if lib_file.startswith(package_name) and lib_file.endswith(".lib"):
                original_lib_path = os.path.join(source_lib, lib_file)
                target_lib_path = os.path.join(dest_lib, lib_file)
                shutil.copy2(original_lib_path, target_lib_path)
                print_and_log(f"Copied {lib_file} to {target_lib_path}")

                # Create a duplicate with Godot-specific naming convention
                godot_lib_name = f"{package_name}.windows.template_debug.x86_64.lib"
                godot_lib_path = os.path.join(dest_lib, godot_lib_name)
                shutil.copy2(original_lib_path, godot_lib_path)
                print_and_log(f"Created Godot-specific library {godot_lib_name}")

    # Copy DLLs to Godot's bin directory for runtime access
    if os.path.exists(source_bin):
        godot_bin_dir = os.path.join(GODOT_MASTER_PATH, "bin")
        os.makedirs(godot_bin_dir, exist_ok=True)
        for file_name in os.listdir(source_bin):
            if file_name.startswith(package_name) and file_name.endswith(".dll"):
                shutil.copy2(os.path.join(source_bin, file_name), godot_bin_dir)
                print_and_log(f"Copied {file_name} to Godot bin directory: {godot_bin_dir}")

# Other function definitions (update_sconstruct, create_scsub_for_module, update_config_py, print_checklist)

def integrate_library(package_name):
    print_and_log("Starting integration process...")
    install_vcpkg_package(package_name)
    module_dir = setup_module_directory(f"{package_name}_integration")
    create_placeholder_files(module_dir)  # Create placeholders for icons, docs, and tests
    copy_vcpkg_files(package_name, module_dir)
    update_sconstruct(package_name, module_dir)
    create_scsub_for_module(package_name, module_dir)

    # Collect all generated classes for documentation
    classes = ["ExampleClass"]  # Replace with actual class detection if needed
    update_config_py(module_dir, classes)

    print_and_log(f"{package_name} has been successfully integrated and configured for Godot.")

    # Print the final checklist
    print_checklist()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: auto_vcpkg_integration.py <package_name>")
        sys.exit(1)
    package_name = sys.argv[1]
    integrate_library(package_name)
