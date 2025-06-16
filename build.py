"""Script de construcción del ejecutable."""

import os
import subprocess
import sys
from pathlib import Path

VENV = Path("venv")


def main() -> None:
    if VENV.exists():
        subprocess.run([sys.executable, "-m", "venv", "--clear", VENV.as_posix()])
    else:
        subprocess.run([sys.executable, "-m", "venv", VENV.as_posix()])
    pip = VENV / "Scripts" / "pip" if os.name == "nt" else VENV / "bin" / "pip"
    subprocess.run([pip, "install", "-r", "requirements.txt"])
    subprocess.run(
        [
            VENV / ("Scripts" if os.name == "nt" else "bin") / "pyinstaller",
            "pyinstaller.spec",
            "--onefile",
            "--noconsole",
            "--add-data",
            "assets{}assets".format(";" if os.name == "nt" else ":"),
            "--hidden-import",
            "pystan",
            "--hidden-import",
            "prophet",
        ]
    )


if __name__ == "__main__":
    main()
