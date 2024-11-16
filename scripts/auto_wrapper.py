import os
import subprocess
import logging
import sys
import shutil

# Setup logging
logging.basicConfig(filename='integration_log.txt', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Paths (Modify these paths as per your setup)
SWIG_PATH = "C:\\Users\\MainFrame\\Mirror\\Pictures\\LightSpeed_GoDot_4\\swigwin\\swig.exe"
GODOT_MASTER_PATH = "C:\\Users\\MainFrame\\Mirror\\Pictures\\LightSpeed_GoDot_4"
MODULE_NAME = "eigen3_integration"
INCLUDE_PATH = os.path.join(GODOT_MASTER_PATH, "modules", MODULE_NAME, "include")

def create_swig_interface(header_file, module_name):
    """Creates a SWIG interface file for a specific header file."""
    interface_file = header_file.replace(".h", ".i")
    with open(interface_file, "w") as f:
        f.write(f"%module {module_name}\n%{{\n#include \"{header_file}\"\n%}}\n\n")
        f.write(f"%include \"{header_file}\"\n")
    logging.info(f"Created SWIG interface file {interface_file}")
    return interface_file

def generate_swig_wrapper(header_file, module_dir, module_name):
    """Generates a SWIG wrapper for a single header file."""
    # Define paths for wrapper file and interface file
    wrapper_filename = f"{os.path.basename(header_file).replace('.h', '_wrap.cxx')}"
    wrapper_file = os.path.join(module_dir, wrapper_filename)
    interface_file = create_swig_interface(header_file, module_name)

    # Run SWIG to generate the wrapper
    try:
        subprocess.run([
            SWIG_PATH, "-c++", "-python", f"-I{module_dir}/include", 
            "-o", wrapper_file, interface_file
        ], check=True)
        logging.info(f"SWIG wrapper generated for {header_file} at {wrapper_file}")
        
        # Move the generated .cxx file to the src directory
        src_dir = os.path.join(module_dir, "src")
        os.makedirs(src_dir, exist_ok=True)
        shutil.move(wrapper_file, os.path.join(src_dir, wrapper_filename))
        logging.info(f"Moved {wrapper_filename} to {src_dir}")

    except subprocess.CalledProcessError as e:
        logging.error(f"SWIG failed to generate wrapper for {header_file}. Error: {e}")

def scan_include_directory_and_generate_wrappers(include_path, module_dir, module_name):
    """Scan the include directory and subdirectories, generating SWIG wrappers for each header file."""
    for root, _, files in os.walk(include_path):
        for file in files:
            if file.endswith(".h"):
                header_file = os.path.join(root, file)
                logging.info(f"Processing header file: {header_file}")
                generate_swig_wrapper(header_file, module_dir, module_name)

def main():
    module_dir = os.path.join(GODOT_MASTER_PATH, "modules", MODULE_NAME)
    os.makedirs(module_dir, exist_ok=True)
    scan_include_directory_and_generate_wrappers(INCLUDE_PATH, module_dir, MODULE_NAME)

if __name__ == "__main__":
    main()
