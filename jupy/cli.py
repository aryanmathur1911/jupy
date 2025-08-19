import subprocess
import argparse
import os
import sys
import webbrowser
import time
import re


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
        path = os.path.abspath(args.folder_name)
        os.makedirs(path, exist_ok=True)
    else:
        path = os.getcwd()

    # Path to venv
    venv_path = os.path.join(path, "venv")

    # Create venv only if not already present
    if not os.path.exists(venv_path):
        print("⚡ Creating virtual environment...")
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
    else:
        python_bin = sys.executable

    editor = input(
        "\nDo you want to create a Jupyter Notebook or continue with VSCode? "
        "[j = Jupyter, c = VSCode] : "
    ).strip().lower()

    if editor == "c":
        print("🚀 Launching a Jupyter Notebook in Visual Studio Code ... ")
        index_file = os.path.join(path, "index.ipynb")
        if not os.path.exists(index_file):
            with open(index_file, "w") as f:
                f.write("")
        subprocess.run(["code", path])

    else:
        print("🚀 Launching Jupyter Notebook (auto-detecting port)...")

        proc = subprocess.Popen(
            [
                python_bin, "-m", "notebook",
                "--no-browser",
                "--NotebookApp.token=",
                "--NotebookApp.password="
            ],
            cwd=str(path),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            shell=(os.name == "nt")
        )

        url = None
        # Parse logs until we find the running URL
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line, end="")  # show logs in console
            match = re.search(r"(http://(?:localhost|127\.0\.0\.1)[^\s]*)", line)
            if match and not url:
                url = match.group(1)
                # Open detected URL
                time.sleep(2)
                webbrowser.open(url)
                print(f"🌐 Opening {url} in browser...")
                break

        # Keep process running
        proc.wait()


if __name__ == "__main__":
    print("⚡ CREATING A JUPYTER NOTEBOOK PROJECT...")
    main()
