#!/bin/bash

# Dataset Download Script for ANTM Hackathon
# This script downloads antm.zip from the public GCP bucket

set -e  # Exit on error

echo "============================================================"
echo "ANTM Hackathon - Dataset Download"
echo "============================================================"
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python 3 is not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"
echo ""

# Run the download + extract script
echo "============================================================"
echo "Downloading antm.zip from GCP bucket..."
echo "============================================================"
echo ""

python3 << 'EOF'
from pathlib import Path
import shutil
import sys
import urllib.request
import zipfile

BUCKET_NAME = "antm-dataset"
ZIP_NAME = "antm.zip"
ZIP_URL = f"https://storage.googleapis.com/{BUCKET_NAME}/{ZIP_NAME}"
ZIP_PATH = Path(ZIP_NAME)
DEST_DIR = Path("dataset")
CHUNK_SIZE = 1024 * 1024  # 1 MiB

def download_zip() -> None:
    print(f"Fetching {ZIP_NAME} from bucket: {BUCKET_NAME}")
    try:
        with urllib.request.urlopen(ZIP_URL) as response, ZIP_PATH.open("wb") as fh:
            total = int(response.headers.get("Content-Length", 0))
            downloaded = 0
            while True:
                chunk = response.read(CHUNK_SIZE)
                if not chunk:
                    break
                fh.write(chunk)
                downloaded += len(chunk)
                if total:
                    percent = (downloaded / total) * 100
                    print(f"  -> {downloaded / 1_048_576:.2f} MiB / {total / 1_048_576:.2f} MiB ({percent:.1f}%)", end="\r")
        if total:
            print("")
        print(f"✓ Downloaded {ZIP_NAME} ({downloaded / 1_048_576:.2f} MiB)")
    except Exception as exc:
        print(f"❌ Error downloading {ZIP_URL}: {exc}")
        sys.exit(1)

def extract_zip() -> None:
    if DEST_DIR.exists():
        print("⚠️  Removing existing dataset/ directory to ensure a clean extract")
        shutil.rmtree(DEST_DIR)
    DEST_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Extracting into {DEST_DIR}/ ...")
    try:
        with zipfile.ZipFile(ZIP_PATH, "r") as zip_file:
            zip_file.extractall(DEST_DIR)
        print("✓ Extraction complete")
    except zipfile.BadZipFile as exc:
        print(f"❌ The downloaded ZIP appears to be corrupted: {exc}")
        sys.exit(1)

def main() -> None:
    download_zip()
    extract_zip()
    print("")
    print("============================================================")
    print(f"Dataset ready in ./{DEST_DIR}/")
    print("You can re-extract by running unzip again without re-downloading.")
    print("============================================================")

if __name__ == "__main__":
    main()
EOF

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "Your dataset is ready in the ./dataset/ directory"
echo "You can now proceed with the hackathon!"
echo ""