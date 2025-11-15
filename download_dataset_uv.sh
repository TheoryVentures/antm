#!/bin/bash

# Dataset Download Script for ANTM Hackathon
# This script downloads the complete dataset from GCP Cloud Storage

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

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    uv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate
echo "✓ Virtual environment activated"
echo ""

# Install required packages
echo "Installing required packages..."
uv pip install --quiet --upgrade pip
uv pip install --quiet google-cloud-storage
echo "✓ Packages installed"
echo ""

# Run the download script
echo "============================================================"
echo "Downloading dataset from GCP bucket..."
echo "============================================================"
echo ""

python3 << 'EOF'
from google.cloud import storage
from pathlib import Path
import sys

def download_bucket_contents(bucket_name, destination_directory="dataset"):
    """Download all files from the GCP bucket to local dataset directory."""
    
    print(f"Connecting to bucket: {bucket_name}")
    
    try:
        storage_client = storage.Client.create_anonymous_client()
        bucket = storage_client.bucket(bucket_name)
        
        Path(destination_directory).mkdir(parents=True, exist_ok=True)
        print(f"✓ Created directory: {destination_directory}/")
        print("")
        
        print("Fetching file list...")
        blobs = list(bucket.list_blobs())
        
        if not blobs:
            print("⚠️  No files found in bucket")
            return
        
        print(f"Found {len(blobs)} files to download")
        print("")
        
        # Download each blob
        success_count = 0
        for i, blob in enumerate(blobs, 1):
            try:
                local_path = Path(destination_directory) / blob.name

                local_path.parent.mkdir(parents=True, exist_ok=True)
                
                blob.download_to_filename(str(local_path))
                
                size_mb = blob.size / (1024 * 1024)
                print(f"  [{i}/{len(blobs)}] ✓ {blob.name} ({size_mb:.2f} MB)")
                
                success_count += 1
                
            except Exception as e:
                print(f"  [{i}/{len(blobs)}] ✗ Failed to download {blob.name}: {e}")
        
        print("")
        print("============================================================")
        print(f"Download complete: {success_count}/{len(blobs)} files")
        print(f"Dataset location: ./{destination_directory}/")
        print("============================================================")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("")
        print("If you see an authentication error, the bucket may not be public.")
        print("Run: gcloud auth application-default login")
        sys.exit(1)

if __name__ == "__main__":
    BUCKET_NAME = "antm-dataset"
    download_bucket_contents(BUCKET_NAME, "dataset")
EOF

echo ""
echo "============================================================"
echo "✅ Setup Complete!"
echo "============================================================"
echo ""
echo "Your dataset is ready in the ./dataset/ directory"
echo "You can now proceed with the hackathon!"
echo ""

