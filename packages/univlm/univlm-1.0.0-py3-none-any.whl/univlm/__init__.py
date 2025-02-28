import atexit
import threading
from .scripts.install_and_test import run_script

_lock = threading.Lock()
_already_ran = False

def run_once():
    global _already_ran
    with _lock:
        if not _already_ran:
            run_script()
            _already_ran = True

atexit.register(run_once)
