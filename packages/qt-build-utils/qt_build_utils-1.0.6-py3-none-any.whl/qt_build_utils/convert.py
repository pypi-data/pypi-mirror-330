import os

from .path_manager import manager
import glob
import subprocess


def pyside_convert_uic(input, output):
    print(f"Converting '{input}' to '{output}'")

    uic_path = manager.find_executable_variants(["pyside6-uic", "pyside2-uic"])
    subprocess.run(f"{uic_path} {input} -o {output}", shell=True)


# icon filename to use
def convert_ui(ui_file: str, inplace: bool, target: str | None = None):
    if inplace:
        pyside_convert_uic(ui_file, ui_file.replace(".ui", ".py"))
    else:
        assert target is not None, "Target directory must be specified when not converting in place"
        assert os.path.exists(target), f"Target directory {target} does not exist"
        pyside_convert_uic(ui_file, os.path.join(target, os.path.basename(ui_file).replace(".ui", ".py")))


def convert_ui_glob(ui_file: str, inplace: bool, target: str | None = None):
    print(f"Converting glob pattern {ui_file}")
    targets = glob.glob(ui_file)
    assert len(targets) > 0, f"No files found for pattern {ui_file}"
    for file in targets:
        convert_ui(file, inplace, target)
