import os
import platform
import sys
import shutil


class PathManager:
    def __init__(self):
        pass

    def get_scripts_dir(self) -> str:
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

        return scripts_dir

    def is_path_setup(self) -> bool:
        return self.get_scripts_dir() in sys.path

    def setup_path(self) -> None:
        print("Configuring PATH")
        scripts_dir = self.get_scripts_dir()

        # Add to path if not already there
        if scripts_dir not in sys.path:
            # Add the Scripts directory to the PATH
            sys.path.insert(0, scripts_dir)
            print("Warn: Python/Scripts directory was not in PATH, added it.")

    def find_executable(self, executable_name: str) -> str | None:
        return shutil.which(executable_name, path=self.get_scripts_dir())

    def find_executable_variants(self, variants: list[str]) -> str | None:
        for executable_name in variants:
            executable = self.find_executable(executable_name)

            if executable:
                return executable

        return None


manager = PathManager()
