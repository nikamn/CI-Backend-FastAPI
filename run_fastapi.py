import os
import subprocess
import sys
import platform


def create_virtualenv():
    # Determine the correct command to create a virtual environment
    if platform.system() == "Windows":
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])
    else:
        subprocess.check_call([sys.executable, "-m", "venv", "venv"])


def activate_virtualenv():
    # Determine the correct script to activate the virtual environment
    if platform.system() == "Windows":
        return os.path.join("venv", "Scripts", "activate.bat")
    else:
        return os.path.join("venv", "bin", "activate")


def install_requirements():
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"]
    )


def run_fastapi():
    host = os.getenv("HOST", "127.0.0.1")
    port = os.getenv("PORT", "8000")
    reload = os.getenv("RELOAD", "True").lower() in ("true", "1", "yes")

    command = [
        sys.executable,
        "-m",
        "uvicorn",
        "app.main:app",
        "--host",
        host,
        "--port",
        port,
    ]
    if reload:
        command.append("--reload")

    subprocess.check_call(command)


if __name__ == "__main__":
    if not os.path.exists("venv"):
        create_virtualenv()
    activate_script = activate_virtualenv()

    if platform.system() == "Windows":
        activate_command = f"{activate_script} && python -m pip install --upgrade pip && python -m pip install -r requirements.txt"
        subprocess.run(activate_command, shell=True, check=True)
        run_fastapi()
    else:
        activate_command = f"source {activate_script} && python -m pip install --upgrade pip && python -m pip install -r requirements.txt && python -m uvicorn app.main:app --host 0.0.0.0 --port 8000"
        if os.getenv("RELOAD", "True").lower() in ("true", "1", "yes"):
            activate_command += " --reload"
        subprocess.run(activate_command, shell=True, check=True)
