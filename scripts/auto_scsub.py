import os

def write_scsub(module_dir):
    scsub_path = os.path.join(module_dir, 'SCsub')
    src_dir = os.path.join(module_dir, 'src')
    lib_dir = os.path.join(module_dir, 'lib')

    with open(scsub_path, 'w') as scsub_file:
        scsub_file.write("Import('env')\n\n")
        
        # Add all .cpp files from src and its subdirectories
        scsub_file.write("# Adding source files\n")
        for root, _, files in os.walk(src_dir):
            for file in files:
                if file.endswith('.cpp'):
                    relative_path = os.path.join(root, file).replace("\\", "/")
                    scsub_file.write(f"env.add_source_files(env.modules_sources, '{relative_path}')\n")

        # Add lib directory for linking
        scsub_file.write("\n# Adding library paths\n")
        scsub_file.write(f"env.Append(LIBPATH=['{lib_dir.replace('\\', '/')}'])\n")

        # Placeholder for library names
        scsub_file.write("env.Append(LIBS=['lib_name_here'])\n")


def write_config_py(module_dir):
    config_path = os.path.join(module_dir, 'config.py')
    include_dir = os.path.join(module_dir, 'include')
    dependencies_dir = os.path.join(module_dir, 'dependencies')

    with open(config_path, 'w') as config_file:
        config_file.write("def can_build(env, platform):\n")
        config_file.write("    return True\n\n")
        config_file.write("def configure(env):\n")
        
        # Add include directories
        config_file.write("    env.Append(CPPPATH=[\n")
        config_file.write(f"        '{include_dir.replace('\\', '/')}',\n")
        config_file.write(f"        '{dependencies_dir.replace('\\', '/')}',\n")
        
        # Include all subdirectories of include and dependencies
        for root, dirs, _ in os.walk(include_dir):
            for directory in dirs:
                include_path = os.path.join(root, directory).replace("\\", "/")
                config_file.write(f"        '{include_path}',\n")
        
        for root, dirs, _ in os.walk(dependencies_dir):
            for directory in dirs:
                dependency_path = os.path.join(root, directory).replace("\\", "/")
                config_file.write(f"        '{dependency_path}',\n")
        
        config_file.write("    ])\n")


def generate_scons_files():
    # Get current directory
    module_dir = os.getcwd()

    print(f"Generating SCons files for module: {os.path.basename(module_dir)}")

    write_scsub(module_dir)
    write_config_py(module_dir)
    print("SCons files generated successfully.")


if __name__ == '__main__':
    generate_scons_files()
