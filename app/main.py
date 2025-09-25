import subprocess
import threading
import time
import os
import socket
import signal
from dotenv import load_dotenv
from app.common.logger import get_logger
from app.common.custom_exception import CustomException

logger = get_logger(__name__)
load_dotenv()

# -------------------------
# Utility Functions
# -------------------------

def find_free_port(start_port=9999, max_tries=20):
    """Find a free port, starting from start_port"""
    port = start_port
    for _ in range(max_tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", port)) != 0:
                return port
        port += 1
    raise RuntimeError("No free ports found!")

def kill_process_on_port(port):
    """Kill process using a specific port (macOS/Linux only)."""
    try:
        result = subprocess.run(
            ["lsof", "-ti", f":{port}"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=False,
        )
        if result.stdout.strip():
            pid = result.stdout.strip()
            logger.warning(f"Killing process {pid} running on port {port}")
            os.kill(int(pid), signal.SIGKILL)
            time.sleep(1)
    except Exception as e:
        logger.error(f"Failed to kill process on port {port}: {e}")

# -------------------------
# Backend + Frontend Launchers
# -------------------------

def run_backend(port):
    try:
        logger.info(f"Starting backend service on port {port}..")
        subprocess.run(
            ["uvicorn", "app.backend.api:app", "--host", "127.0.0.1", "--port", str(port)],
            check=True,
        )
    except subprocess.CalledProcessError as e:
        logger.error("Problem with backend service")
        raise CustomException("Failed to start backend", e)

def run_frontend(backend_port):
    try:
        logger.info("Starting frontend service..")
        # Pass backend port as env var so Streamlit knows where to connect
        env = os.environ.copy()
        env["BACKEND_PORT"] = str(backend_port)
        subprocess.run(
            ["streamlit", "run", "app/frontend/ui.py", "--server.port", "8501"],
            check=True,
            env=env,
        )
    except subprocess.CalledProcessError as e:
        logger.error("Problem with frontend service")
        raise CustomException("Failed to start frontend", e)

# -------------------------
# Main Runner
# -------------------------

if __name__ == "__main__":
    try:
        desired_port = 9999
        kill_process_on_port(desired_port)  # Kill any old stuck process
        backend_port = find_free_port(desired_port)  # Pick available port

        threading.Thread(target=run_backend, args=(backend_port,), daemon=True).start()
        time.sleep(2)  # give backend time to boot

        run_frontend(backend_port)

    except CustomException as e:
        logger.exception(f"CustomException occurred: {str(e)}")
    except KeyboardInterrupt:
        logger.info("Shutting down services gracefully...")
