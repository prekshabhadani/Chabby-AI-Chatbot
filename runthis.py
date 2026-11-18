
import subprocess
import sys
from pathlib import Path

# Get the project folder
project_folder = Path(__file__).resolve().parent

# Run the Streamlit application
subprocess.run(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(project_folder / "app.py")
    ],
    cwd=project_folder
)
