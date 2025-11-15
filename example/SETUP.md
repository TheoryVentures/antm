# Setup Instructions

## Prerequisites

- Python 3.11 or higher
- pip (comes with Python)

## Installation

### Recommended: Use a Virtual Environment

This prevents common issues with system Python installations (especially on macOS):

1. Clone the repository:
```bash
git clone https://github.com/theoryvc/modeler-hackathon-starter.git
cd modeler-hackathon-starter
```

2. Create and activate a virtual environment (from the repo root):
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Upgrade `pip` and install the notebook dependencies:
```bash
python -m pip install --upgrade pip
python -m pip install -r example/requirements.txt
```

4. (Optional) Inspect the dataset (already included at `dataset/` in the repo root):
```bash
ls dataset
```

5. Register the environment as a Jupyter kernel so VS Code/Jupyter can pick it automatically:
```bash
python -m ipykernel install --user --name "modeler-default" --display-name "Python 3 (Modeler Default)"
```

6. (Optional) Remove stale kernels that point to deleted Python installs:
```bash
jupyter kernelspec list
jupyter kernelspec uninstall python3
```

7. Launch the notebook (still from the repo root):
```bash
jupyter notebook example/tools_guide.ipynb
```
