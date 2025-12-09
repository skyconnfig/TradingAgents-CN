import os
import subprocess
from pathlib import Path

project_root = Path(__file__).parent
app_path = project_root / "web" / "app.py"
port = os.getenv("STREAMLIT_PORT", "8501")
address = os.getenv("STREAMLIT_ADDR", "127.0.0.1")

subprocess.run([
    "streamlit",
    "run",
    str(app_path),
    "--server.port",
    str(port),
    "--server.address",
    str(address)
], check=True)