import subprocess
from typing import Any, Generator
from python_project_manager.config import Config
from python_project_manager.venv_helper import activate_venv, deactivate_venv
from contextlib import contextmanager

IS_SILENT = False # If True, the command will not print anything to the console
OUTPUT_LIST = None # If not None, the output of the command will be appended to this list
TIME_OUT = None # The time out for the command

@contextmanager
def command_context(*, is_silent: bool = False, output_list: list = None, time_out: int = None) -> Generator[Any, Any, Any]:
    '''
    A context manager that allows you to change the global settings of the run_command function.

    Args:
        is_silent (bool): If True, the command will not print anything to the console.
        output_list (list): If not None, the output of the command will be appended to this list. (Note: will also activate is_silent)
        time_out (int): The time out for the command.
    '''
    try:
        global IS_SILENT, OUTPUT_LIST, TIME_OUT
        IS_SILENT = is_silent
        TIME_OUT = time_out
        if output_list is not None:
            IS_SILENT = True
            OUTPUT_LIST = output_list
        yield
    finally:
        IS_SILENT = False
        OUTPUT_LIST = None

def run_command(command: str, *, use_venv: bool) -> None:
    '''
    Runs a command in the shell.

    Args:
        command (str): The command to run.
        cwd (str): The current working directory to run the command in.
        use_venv (bool): If True, the command will be run in the virtual environment.
    '''

    if use_venv:
        command = [activate_venv(), command]
    else:
        command = [deactivate_venv(), command]
    
    python_paths = Config.get('include_paths', [])
    python_path = f'set PYTHONPATH={';'.join(python_paths)}' if len(python_paths) > 0 else ''
    command = [python_path, *command]
    
    command = [c for c in command if c] # Remove any empty strings from the
    command = ' && '.join(command)
    
    with subprocess.Popen(
        command,
        stdout=subprocess.PIPE if IS_SILENT else None,
        shell=True) as process:
        process.wait(TIME_OUT)

        if OUTPUT_LIST is not None:
            OUTPUT_LIST.append(process.stdout.read().decode(errors='replace'))

        exitcode = process.returncode
        if exitcode != 0: exit(exitcode)