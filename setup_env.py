import os
import sys
import subprocess

def has_gpu():
    try:
        # Hide the console window on Windows when checking for nvidia-smi
        startupinfo = None
        if os.name == 'nt':
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            
        subprocess.check_output("nvidia-smi", stderr=subprocess.STDOUT, startupinfo=startupinfo)
        return True
    except:
        return False

def get_installed():
    try:
        reqs = subprocess.check_output([sys.executable, "-m", "pip", "freeze"])
        return reqs.decode('utf-8').lower()
    except:
        return ""

def main():
    gpu_available = has_gpu()
    installed = get_installed()
    
    pkgs = ["customtkinter", "Pillow"]
    needs_install = False
    
    if gpu_available:
        if "onnxruntime-gpu" not in installed:
            print("Found an NVIDIA GPU. Setting up hardware acceleration...")
            if "onnxruntime==" in installed or "onnxruntime@" in installed:
                subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", "onnxruntime"])
            pkgs.append("rembg[gpu]")
            needs_install = True
    else:
        if "onnxruntime-gpu" in installed:
            print("No NVIDIA GPU detected. Switching to CPU processing...")
            subprocess.call([sys.executable, "-m", "pip", "uninstall", "-y", "onnxruntime-gpu"])
            pkgs.append("rembg")
            needs_install = True
        elif "rembg" not in installed:
            pkgs.append("rembg")
            needs_install = True
            
    if "customtkinter" not in installed or "pillow" not in installed:
        needs_install = True
        
    if needs_install:
        print("Installing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + pkgs)
        print("All done!")

if __name__ == "__main__":
    main()

