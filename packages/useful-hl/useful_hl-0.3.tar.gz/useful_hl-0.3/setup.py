from setuptools import setup, find_packages

import os
import subprocess
import sys
from setuptools import setup

def install_cmake():
    """Check if CMake is installed, and install it if missing."""
    try:
        subprocess.run(["cmake", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print("✅ CMake is already installed.")
    except FileNotFoundError:
        print("⚠️ CMake is not installed. Checking for Homebrew...")

        if sys.platform == "darwin":  # macOS
            try:
                subprocess.run(["brew", "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print("✅ Homebrew is installed. Installing CMake...")
            except FileNotFoundError:
                print("⚠️ Homebrew is not installed. Installing Homebrew first...")
                os.system('/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"')

            # Now install CMake
            os.system("brew install cmake")

        elif sys.platform == "linux":
            os.system("sudo apt update && sudo apt install -y cmake")
        elif sys.platform == "win32":
            os.system("choco install cmake -y")  # Requires Chocolatey
        else:
            print("❌ Unsupported OS. Please install CMake manually.")

# Run CMake installation check
install_cmake()


setup(
    name="useful--hl",
    version="0.3",
    packages=find_packages(),
    install_requires=[
    "numpy==2.1.1","pylibCZIrw==4.1.3","cmake==3.31.4"],
    author="ktsolakidis",
    description="A simple package with random functions",
    python_requires=">=3.10,<3.11",  
)