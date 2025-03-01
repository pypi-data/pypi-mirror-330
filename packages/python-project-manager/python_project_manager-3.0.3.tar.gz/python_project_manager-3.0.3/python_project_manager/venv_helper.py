
import os
import sys

# Get working directory
_VENV_PATH = f'venv'
_VENV_SITE_PACKAGES = f'{_VENV_PATH}\\Lib\\site-packages'
_VENV_SCRIPTS = f'{_VENV_PATH}\\Scripts'
_ACTIVATE_VENV = f'{_VENV_SCRIPTS}\\activate' # Used to activate the virtual environment
_DEACTIVATE_VENV = f'{_VENV_SCRIPTS}\\deactivate' # Used to deactivate the virtual environment

# TODO: Automagically create the virtual environment if it does not exist
def activate_venv() -> str:
    # check if the virtual environment exists
    if not os.path.exists(_VENV_PATH):
        raise FileNotFoundError(f"Virtual environment not found at '{_VENV_PATH}'.\nRun 'ppm venv' to create a virtual environment.")
    return _ACTIVATE_VENV

def deactivate_venv() -> str:
    # check if the virtual environment exists
    if not os.path.exists(_VENV_PATH):
        return ""
    return _DEACTIVATE_VENV

def is_venv_installed() -> bool:
    return os.path.exists(_VENV_PATH)

def is_venv_active():
    # sys.prefix points to the virtual environment when it is active
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        return True
    return False