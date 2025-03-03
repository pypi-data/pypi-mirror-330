from .convert_ui import cli
import sys
import os
from shutil import which

if __name__ == "__main__":
    # Add exectuables scripts folder to path
    python_path = os.path.dirname(sys.executable)

    # Insert the path to the beginning of the path
    sys.path.insert(0, python_path)
        
    cli()

