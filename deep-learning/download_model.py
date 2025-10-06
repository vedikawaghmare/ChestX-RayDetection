#!/usr/bin/env python3
"""
Model Download Script for Chest X-Ray Analysis System
"""

import os
import requests
from tqdm import tqdm
import hashlib

def download_file(url, filename, expected_size=None, chunk_size=8192):
    """Download file with progress bar"""
    print(f"📥 Downloading {filename}...")
    
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        if expected_size and total_size != expected_size:
            print(f"⚠️  Warning: Expected size {expected_size}, got {total_size}")
        
        with open(filename, 'wb') as file, tqdm(
            desc=filename,
            total=total_size,
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
        ) as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    file.write(chunk)
                    pbar.update(len(chunk))
        
        print(f"✅ Downloaded {filename} successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Download failed: {e}")
        return False

def verify_file(filename, expected_hash=None):
    """Verify downloaded file"""
    if not os.path.exists(filename):
        return False
    
    file_size = os.path.getsize(filename)
    print(f"📊 File size: {file_size / (1024*1024):.1f} MB")
    
    if expected_hash:
        print("🔍 Verifying file integrity...")
        sha256_hash = hashlib.sha256()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
        
        file_hash = sha256_hash.hexdigest()
        if file_hash == expected_hash:
            print("✅ File integrity verified!")
            return True
        else:
            print(f"❌ Hash mismatch! Expected: {expected_hash}, Got: {file_hash}")
            return False
    
    return True

def main():
    """Main download function"""
    print("🏥 Chest X-Ray Model Download Utility")
    print("=" * 50)
    
    model_filename = "densenet.hdf5"
    
    # Check if model already exists
    if os.path.exists(model_filename):
        if verify_file(model_filename):
            print(f"✅ Model file {model_filename} already exists and is valid!")
            return
        else:
            print(f"⚠️  Existing model file appears corrupted, re-downloading...")
            os.remove(model_filename)
    
    # Model download options
    download_options = [
        {
            "name": "GitHub Releases (Recommended)",
            "url": "https://github.com/yourusername/chest-xray-diagnosis/releases/download/v1.0/densenet.hdf5",
            "size": 29291464,  # ~27.9 MB
            "hash": None  # Add actual hash when available
        },
        {
            "name": "Google Drive",
            "url": "https://drive.google.com/uc?id=YOUR_GOOGLE_DRIVE_FILE_ID",
            "size": 29291464,
            "hash": None
        },
        {
            "name": "Hugging Face Hub",
            "url": "https://huggingface.co/yourusername/chest-xray-densenet/resolve/main/densenet.hdf5",
            "size": 29291464,
            "hash": None
        }
    ]
    
    print("📦 Available download sources:")
    for i, option in enumerate(download_options, 1):
        print(f"   {i}. {option['name']}")
    
    print(f"   {len(download_options) + 1}. Manual download instructions")
    print()
    
    try:
        choice = input("Select download source (1-4): ").strip()
        choice_idx = int(choice) - 1
        
        if choice_idx == len(download_options):
            # Manual instructions
            print("\n📋 Manual Download Instructions:")
            print("=" * 40)
            print("1. Visit: https://github.com/yourusername/chest-xray-diagnosis/releases")
            print("2. Download: densenet.hdf5 from the latest release")
            print("3. Place the file in this directory (deep-learning/)")
            print("4. Run this script again to verify")
            return
        
        if 0 <= choice_idx < len(download_options):
            option = download_options[choice_idx]
            print(f"\n📥 Downloading from: {option['name']}")
            
            success = download_file(
                option['url'], 
                model_filename, 
                option['size']
            )
            
            if success:
                if verify_file(model_filename, option['hash']):
                    print("\n🎉 Model download completed successfully!")
                    print("🚀 You can now run: python3 run_system.py")
                else:
                    print("\n❌ Model verification failed!")
            else:
                print(f"\n❌ Download from {option['name']} failed!")
                print("💡 Try another source or manual download")
        else:
            print("❌ Invalid choice!")
            
    except ValueError:
        print("❌ Invalid input! Please enter a number.")
    except KeyboardInterrupt:
        print("\n\n🛑 Download cancelled by user")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()