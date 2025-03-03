import subprocess
import sys
import shutil

def pyside_uic_run(command: str):
    EXECUTABLE = ["pyside6-uic", "pyside2-uic"]

    # Try to find the pyside-uic executable
    for executable_name in EXECUTABLE:
        executable = shutil.which(executable_name, path=";".join(sys.path))

        if executable:
            subprocess.run(f"{executable} {command}", shell=True)
            return    
        
    raise SystemError("pyside-uic executable not found")


def pyside_designer_run(command: str):
    EXECUTABLE = ["pyside6-designer", "pyside2-designer"]

    # Try to find the pyside-uic executable
    for executable_name in EXECUTABLE:
        executable = shutil.which(executable_name, path=";".join(sys.path))
        if executable:
            subprocess.run(f"{executable} {command}", shell=True)
            return

    raise SystemError("pyside-designer executable not found")
