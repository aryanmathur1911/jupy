import subprocess
import argparse
import os
import sys
import webbrowser
import time


def main():
    parser = argparse.ArgumentParser(description="Jupyter Project Creator")
    parser.add_argument(
        "folder_name",
        nargs="?",
        help="Name of source folder (default: current folder)"
    )
    args = parser.parse_args()

    # Use given folder or current directory
    if args.folder_name:
        path = args.folder_name
        os.makedirs(path, exist_ok=True)
    else:
        path = os.getcwd()

    # Create virtual environment
    venv_path = os.path.join(path, "venv")
    subprocess.run([sys.executable, "-m", "venv", venv_path])

    # Get python inside venv
    if os.name == "nt":
        python_bin = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        python_bin = os.path.join(venv_path, "bin", "python")

    # Install dependencies
    packages = ["numpy", "pandas", "matplotlib", "scikit-learn", "seaborn", "notebook"]
    print(f"📦 Installing dependencies into {venv_path} ...")
    subprocess.run([python_bin, "-m", "pip", "install", "--upgrade", "pip"])
    subprocess.run([python_bin, "-m", "pip", "install", *packages])

    # Launch Jupyter Notebook without token
    print("🚀 Launching Jupyter Notebook on http://localhost:8888/tree ...")

    subprocess.Popen([
        str(python_bin), "-m", "notebook",
        "--no-browser",
        "--port=8888",
        "--NotebookApp.token=''",
        "--NotebookApp.password=''"
    ], cwd=str(path))

    # Give Jupyter a few seconds to start
    time.sleep(3)
    webbrowser.open("http://localhost:8888/tree")


if __name__ == "__main__":
    print("⚡ CREATING A JUPYTER NOTEBOOK PROJECT...")
    main()
