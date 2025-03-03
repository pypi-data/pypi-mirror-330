import os
import sys
import platform

PATH_IS_SETUP = False


def is_path_setup() -> bool:
    return PATH_IS_SETUP


def setup_path():
    print("Setting up PATH")
    # Get pyton scripts directory
    python_base_path = os.path.dirname(sys.executable)

    # Check if base path is in the Scripts directory
    # check if we are on macos
    if platform.system() == "Windows":
        if os.path.basename(os.path.normpath(python_base_path)) != "Scripts":
            scripts_dir = os.path.join(python_base_path, "Scripts")
        else:
            scripts_dir = python_base_path
    elif platform.system() == "Linux":
        if os.path.basename(os.path.normpath(python_base_path)) != "bin":
            scripts_dir = os.path.join(python_base_path, "bin")
        else:
            scripts_dir = python_base_path
    elif platform.system() == "Darwin":
        if os.path.basename(os.path.normpath(python_base_path)) != "bin":
            scripts_dir = os.path.join(python_base_path, "bin")
        else:
            scripts_dir = python_base_path
    else:
        raise NotImplementedError(f"{platform.system()} is not supported")

    # Add scripts directory to PATH if not already there
    if not os.path.exists(scripts_dir):
        raise SystemError(f"Scripts directory not found in {python_base_path}")

    # Add to path if not already there
    if scripts_dir not in os.environ["PATH"].split(os.pathsep):
        # Add the Scripts directory to the PATH
        os.environ["PATH"] += os.pathsep + scripts_dir
        print("Warn: Python/Scripts directory was not in PATH, added it.")

    global PATH_IS_SETUP
    PATH_IS_SETUP = True


if __name__ == "__main__":
    setup_path()
