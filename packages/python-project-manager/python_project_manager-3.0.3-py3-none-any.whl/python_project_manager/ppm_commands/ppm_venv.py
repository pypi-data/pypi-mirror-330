import os
import shutil
import click
from python_project_manager.config import Config
from python_project_manager.run_command import run_command
from python_project_manager.venv_helper import is_venv_installed, _VENV_PATH

@click.command()
@click.option('--reset', '-r', is_flag=True, help='Reinitalize the virtual environment.')
@click.option('--install', '-i', is_flag=True, help='Installs dependencies in the virtual environment after initialization.')
def venv(reset, install) -> None:
    if is_venv_installed():
        if reset:
            shutil.rmtree(_VENV_PATH)
        else:
            print('Virtual environment already exists.')
            return
        
    # Create the virtual environment
    run_command('python -m venv venv', use_venv=False)

    if install:
        run_command('ppm install', use_venv=True)
        return

    user_input = input('Would you like to install the requirements now? (y/n): ')
    if user_input.lower() == 'y':
        run_command('ppm install', use_venv=True)
    elif user_input.lower() == 'n':
        print('To install the requirements later, run `ppm install`.')
    else:
        print('Invalid input. Please run `ppm install` to install the requirements.')