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

2. Create and activate a virtual environment:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Register the kernel for Jupyter/VS Code:
```bash
python -m ipykernel install --user --name "modeler-starter" --display-name "Python 3 (Modeler Starter)"
```

5. Open the notebook:
```bash
jupyter notebook tools_guide.ipynb
```

**In VS Code:** Select "Python 3 (Modeler Starter)" from the kernel picker (top right of notebook).

### Alternative: System-Wide Installation

If you prefer not to use a virtual environment:

```bash
pip install -r requirements.txt
python -m ipykernel install --user
jupyter notebook tools_guide.ipynb
```

**Note:** This may fail on macOS/Homebrew Python due to externally-managed environment restrictions. Use the virtual environment method above if you encounter errors.

## Troubleshooting

### "Running cells requires the ipykernel package" error

This is common on macOS with Homebrew Python. The fix:

1. Create a virtual environment (see "Recommended" section above)
2. Install ipykernel in that environment
3. Register it as a kernel
4. Select that kernel in VS Code/Jupyter

### "Kernel not found" error

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook tools_guide.ipynb
```

### Verifying installation

Test that everything works:
```bash
python -c "import duckdb, pandas, lancedb; print('All packages installed!')"
```

## Using Google Colab

Don't want to install locally? Open the notebook in Google Colab:
1. Go to [colab.research.google.com](https://colab.research.google.com)
2. File → Open Notebook → GitHub
3. Enter the repo URL
4. Select `tools_guide.ipynb`

The notebook will install dependencies automatically.
