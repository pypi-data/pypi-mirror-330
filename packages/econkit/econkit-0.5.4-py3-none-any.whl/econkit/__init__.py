import subprocess
import sys
import importlib
import os
from distutils.version import LooseVersion
import requests

# Version Check and Update Function
def check_and_install_libraries():
    required_packages = [
        'pandas', 'numpy', 'scipy', 'statsmodels', 
        'yfinance', 'requests', 'tabulate', 'warnings'
    ]
    
    def check_and_install(package):
        try:
            importlib.import_module(package)
        except ImportError:
            print(f"{package} is not installed.")
            response = input(f"Do you want to install {package}? (yes/no): ").strip().lower()
            if response == 'yes':
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"{package} has been installed.")
            else:
                print(f"{package} is required for this library to work properly.")

    for package in required_packages:
        check_and_install(package)

def check_for_latest_version():
    try:
        from .version import __version__
        current_version = __version__
        response = requests.get('https://pypi.org/pypi/econkit/json')
        latest_version = response.json()['info']['version']
        
        if LooseVersion(current_version) < LooseVersion(latest_version):
            print(f"A new version of econkit is available: {latest_version}")
            update = input("Do you want to update now? (yes/no): ").strip().lower()
            if update == 'yes':
                subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "econkit"])
                print("Library updated. Please restart your application.")
    except Exception as e:
        print(f"Error checking for library update: {e}")

# Check and install required libraries
check_and_install_libraries()

# Import Version
from .version import __version__

# Import Other Modules
from . import econometrics, finance

# Initialize the version check at the end of the file
check_for_latest_version()
