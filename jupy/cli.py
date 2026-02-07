import subprocess
import argparse
import os
import webbrowser
import time
import re


def main():
    parser = argparse.ArgumentParser(description="Jupyter Project Creator (uv powered)")
    parser.add_argument(
        "folder_name",
        nargs="?",
        help="Name of source folder (default: current folder)"
    )
    args = parser.parse_args()

    # Determine project path
    if args.folder_name:
        path = os.path.abspath(args.folder_name)
        os.makedirs(path, exist_ok=True)
    else:
        path = os.getcwd()

    pyproject = os.path.join(path, "pyproject.toml")
    venv_dir = os.path.join(path, ".venv")

    # Initialize uv project if not exists
    if not os.path.exists(pyproject):
        print("⚡ Initializing uv project...")
        subprocess.run(["uv", "init", "--bare"], cwd=path, check=True)

    # Explicitly create venv if missing (most reliable)
    if not os.path.exists(venv_dir):
        print("⚡ Creating virtual environment...")
        subprocess.run(["uv", "venv"], cwd=path, check=True)

    packages = [
        "numpy",
        "pandas",
        "matplotlib",
        "scikit-learn",
        "seaborn",
        "notebook",
        "ipykernel"
    ]

    print("📦 Ensuring dependencies are installed...")
    subprocess.run(["uv", "add", *packages], cwd=path, check=True)

    editor = input(
        "\nDo you want to create a Jupyter Notebook or continue with VSCode? "
        "[j = Jupyter, c = VSCode] : "
    ).strip().lower()

    if editor == "c":
        print("🚀 Launching project in VS Code...")
        index_file = os.path.join(path, "index.ipynb")
        if not os.path.exists(index_file):
            subprocess.run(["uv", "run", "python", "-m", "ipykernel", "install", "--user"], cwd=path)
            open(index_file, "w").close()
        subprocess.run(["code", path])

    else:
        print("🚀 Launching Jupyter Notebook (auto-detecting port)...")

        proc = subprocess.Popen(
            [
                "uv", "run", "jupyter", "notebook",
                "--no-browser",
                "--NotebookApp.token=",
                "--NotebookApp.password="
            ],
            cwd=path,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )

        url = None
        while True:
            line = proc.stdout.readline()
            if not line:
                break
            print(line, end="")
            match = re.search(r"(http://(?:localhost|127\.0\.0\.1)[^\s]*)", line)
            if match and not url:
                url = match.group(1)
                time.sleep(2)
                webbrowser.open(url)
                print(f"🌐 Opening {url} in browser...")
                break

        proc.wait()


if __name__ == "__main__":
    print("⚡ CREATING A JUPYTER NOTEBOOK PROJECT (uv edition)...")
    main()
