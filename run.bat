@echo off

set "PATH=C:\Program Files\NVIDIA GPU Computing Toolkit\CUDA\v13.3\bin\x64;%PATH%"
set "PATH=C:\Program Files\NVIDIA\CUDNN\v9.24\bin\13.3\x64;%PATH%"

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

call venv\Scripts\activate

echo Initializing setup...
python setup_env.py

python main.py

pause
