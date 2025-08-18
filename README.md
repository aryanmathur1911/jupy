# Jupyt 📝⚡

A simple CLI tool to **create Jupyter Notebook projects with virtual environments** automatically.  

It sets up:  
- A new project folder (or uses current folder).  
- A Python virtual environment.  
- Installs common data science packages.  
- Launches **Jupyter Notebook** automatically in the environment.  

---

## 🚀 Installation

NOTE : This tool is not currently published to PyPI, so you can't install it through pip directly. Therefore clone the repo as suggested below.

You can install this package directly from PyPI:

```bash
pip install jupy
```

⚡ Usage

Create a  jupyter project in current working directory :

```bash
jupy
```

or if creating a new folder : 

```bash
jupy <folder_name>
```

##If you are cloning the repo locally:

```bash
git clone https://github.com/aryanmathur1911/jupy.git

cd jupy

pip install -e .
```
Then follow the same steps as mentioned earlier.

