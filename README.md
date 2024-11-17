# LightSpeed Mod Installer 🚀 [WIP]

LightSpeed Mod Installer is a GUI-based application designed to simplify the management and installation of libraries, modules, and utilities for Godot Engine projects. Featuring a sleek Matrix-style interface and dynamic script execution, it’s the ultimate tool for Godot developers who want to accelerate their workflow like never before.
How Does It Work?

The tool integrates and extends two powerful open-source projects: VCPKG and SWIG. By combining their functionalities, it provides scripts that make initializing and setting up modules easier than ever.

Here’s a quick example:
Let’s say you want to add a C++ library to your Godot Engine project.

    Add your Godot project folder to LightSpeed.
    Specify the Godot modules folder.
    Use the VCPKG search functionality to find and select the desired library.

Once you’ve made your selection, VCPKG will handle the compilation and building process. The necessary starting files are automatically placed in the correct Godot directories under the modules folder, and the module is added by name for easy integration.

Additional utilities included in LightSpeed provide extended functionality to your modules, enabling further customization and enhancement.
Prebuilt Libraries and Utilities

LightSpeed also comes with prebuilt libraries and utilities to supercharge your workflow. Don’t forget to check them out!
LS_Boost_Mod (TBA)

This utility will bootstrap Godot with the Boost library, providing an additional layer of functionality and power to your Godot projects.

![Light Speed Mod GUI](assets/AppGUI.png "Light Speed Mod GUI")

## 🎨 Features

- **Matrix-Style Background**: A visually appealing animated effect to make your experience more futuristic.
- **ASCII Art Integration**: Eye-catching logos for your application.
- **Godot Module Management**:
  - Browse and select your Godot engine folder.
  - Install libraries like PhysX, TensorFlow, and geometry3.
  - Execute utility scripts dynamically from within the GUI.
- **Dynamic Console Logging**: View logs directly in the application console.
- **Utility Scripts**:
  - Automatically handle bindings, wrappers, SCsub configurations, and much more.

## 📂 Project Structure

```plaintext
project_root/
├── swig/                # Additional SWIG components (if required)
├── vcpkg/               # vcpkg package manager
├── scripts/             # Python scripts for utilities
│   ├── auto_bind.py
│   ├── auto_func_fix.py
│   ├── auto_master.py
│   ├── auto_pyconfig.py
│   ├── auto_register.py
│   ├── auto_scsub.py
│   ├── auto_vcpkg.py
│   ├── auto_wrapper.py
│   ├── auto_cleanup.py
├── main/                # Main GUI application and build configuration
│   ├── mod_GUI.py       # Main GUI script
│   ├── SConstruct       # SCons build script
├── assets/              # Fonts, images, and other assets
│   └── fonts/
├── .sconsign.dblite     # SCons metadata file
├── README.md            # Project README file
└── requirements.txt     # Python dependencies

