import subprocess
import sys
from pathlib import Path

project_dir = Path(__file__).resolve().parent
app_file = project_dir / "app" / "streamlit_app.py"

if not app_file.exists():
    raise FileNotFoundError(f"App file not found: {app_file}")

subprocess.run(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        str(app_file),
    ],
    cwd=str(project_dir),
    check=False,
)