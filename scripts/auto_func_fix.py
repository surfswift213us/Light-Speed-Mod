import os
import re
import datetime
import sys

# Define paths
godot_root = os.getcwd()
modules_dir = os.path.join(godot_root, "modules")
log_file = os.path.join(godot_root, "auto_func_fix_log.txt")
processed_modules_file = os.path.join(godot_root, "processed_modules.txt")

# Log function
def log(message):
    with open(log_file, "a") as log_f:
        log_f.write(f"{datetime.datetime.now()}: {message}\n")
    print(message)

# Function to read processed modules from a file
def read_processed_modules():
    if os.path.exists(processed_modules_file):
        with open(processed_modules_file, "r") as f:
            return set(f.read().splitlines())
    return set()

# Function to save processed modules to a file
def save_processed_module(module_name):
    with open(processed_modules_file, "a") as f:
        f.write(module_name + "\n")

# Function to display progress in the terminal
def print_progress(current, total):
    progress = int((current / total) * 100)
    sys.stdout.write(f"\rProgress: {progress}% ({current}/{total})")
    sys.stdout.flush()

# Function to find all .h files recursively in a given directory
def find_header_files(directory):
    header_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".h"):
                header_files.append(os.path.join(root, file))
    return header_files

# Function to extract function signatures from a header file
def extract_functions(header_file):
    try:
        with open(header_file, "r", encoding="utf-8") as f:  # Specify utf-8 encoding
            content = f.read()
    except (FileNotFoundError, UnicodeDecodeError) as e:
        log(f"Error reading {header_file}: {e}")
        return []
    
    # Regular expression to match function declarations
    function_regex = re.compile(r'(\w[\w\s\*&]+)\s+(\w+)\(([^)]*)\)\s*;')
    functions = function_regex.findall(content)
    
    extracted_functions = []
    for return_type, func_name, params in functions:
        param_list = []
        for param in params.split(','):
            param = param.strip()
            if param:
                param_type = ' '.join(param.split()[:-1])  # Everything but the last word
                param_name = param.split()[-1] if len(param.split()) > 1 else None
                param_list.append((param_type, param_name))
        extracted_functions.append((return_type.strip(), func_name.strip(), param_list))
    
    return extracted_functions

# Function to generate C++ header and implementation bindings for functions
def generate_bindings(module_name, functions):
    header_content = f"#ifndef {module_name.upper()}_FUNC_H\n#define {module_name.upper()}_FUNC_H\n\n"
    header_content += f"// Auto-generated bindings for {module_name}\n\n"
    impl_content = f"#include \"{module_name}_func.h\"\n\n"
    
    for return_type, func_name, params in functions:
        param_str = ', '.join([f"{ptype} {pname}" for ptype, pname in params if pname])
        if not param_str:
            param_str = 'void'
        
        # Append to header content
        header_content += f"{return_type} {func_name}({param_str});\n"
        
        # Append to implementation content
        impl_content += f"{return_type} {module_name}_{func_name}({param_str}) {{\n"
        impl_content += f"    // TODO: Implement {func_name}\n"
        if return_type != "void":
            impl_content += f"    return {return_type}(); // Placeholder return\n"
        impl_content += "}\n\n"
        impl_content += f'ClassDB::bind_method(D_METHOD("{func_name}"), &{module_name}_{func_name});\n\n'

    header_content += "\n#endif\n"
    return header_content, impl_content

# Function to write bindings to .cpp and .h files
def write_bindings(module_name, header_content, impl_content):
    module_dir = os.path.join(modules_dir, module_name)
    header_file_path = os.path.join(module_dir, f"{module_name}_func.h")
    cpp_file_path = os.path.join(module_dir, f"{module_name}_func.cpp")
    
    with open(header_file_path, "w") as header_file:
        header_file.write(header_content)
    log(f"Created header file: {header_file_path}")
    
    with open(cpp_file_path, "w") as cpp_file:
        cpp_file.write(impl_content)
    log(f"Created implementation file: {cpp_file_path}")

# Main function
def main():
    log("Starting auto_func_fix script...")
    
    # Read already processed modules
    processed_modules = read_processed_modules()

    # Identify _integration modules
    integration_modules = [d for d in os.listdir(modules_dir) if d.endswith("_integration") and os.path.isdir(os.path.join(modules_dir, d))]
    total_modules = len(integration_modules)
    log(f"Found _integration modules: {integration_modules}")

    for index, module_name in enumerate(integration_modules, start=1):
        # Skip if the module was already processed
        if module_name in processed_modules:
            log(f"Skipping already processed module: {module_name}")
            print_progress(index, total_modules)
            continue

        module_path = os.path.join(modules_dir, module_name)
        include_path = os.path.join(module_path, "include")
        
        if not os.path.exists(include_path):
            log(f"Skipping {module_name} (no include directory found)")
            print_progress(index, total_modules)
            continue
        
        # Find all header files within this module's include directory
        header_files = find_header_files(include_path)
        log(f"Found {len(header_files)} header files in {module_name}")

        # Extract functions and generate bindings
        all_header_content = ""
        all_impl_content = ""
        for header in header_files:
            functions = extract_functions(header)
            log(f"Extracted {len(functions)} functions from {header}")
            if functions:
                header_content, impl_content = generate_bindings(module_name, functions)
                all_header_content += header_content
                all_impl_content += impl_content
        
        # Write or append bindings to integration_func.cpp and integration_func.h
        if all_header_content and all_impl_content:
            write_bindings(module_name, all_header_content, all_impl_content)
            save_processed_module(module_name)
            log(f"Processed and updated {module_name}")

        # Display progress
        print_progress(index, total_modules)

    log("auto_func_fix script completed.")
    print("\nCompleted processing all modules.")

if __name__ == "__main__":
    main()
